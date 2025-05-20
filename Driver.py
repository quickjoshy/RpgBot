from Profile import Profile
from Fighter import Fighter
from Party import Party
import Fight
from Inventory import Inventory
import MoveList
import ItemList
import discord
from discord import app_commands
from discord.ext import commands
import os

def find_item_by_property(item_list, property_name, property_value):
    for item in item_list:
      if hasattr(item, property_name) and getattr(item, property_name) == property_value:
        return item
    return None

tokenFile = open('token', 'r')
token = tokenFile.read()
tokenFile.close()

fights = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def ProfileFromDiscord(id, name):
    profiles = open('Profiles', 'r')
    lines = profiles.readlines()

    profileData = ''
    for line in lines:
        if(line.find(str(id)) != -1):
            profileData = line
            break
    profiles.close()

    data = profileData.split(sep=',')

    profile = Profile(name, int(data[1]), int(data[2]), int(data[3]), int(data[4]), [], Inventory([], None, None, 0))
    return profile

def UpdateProfile(id, strength, int, end, spd):
    temp = open('Temp', 'w')
    profiles = open('Profiles', 'r')
    lines = profiles.readlines()
    existingProfile = False
    for line in lines:
        tokens = line.split(sep=',')
        print(f"{tokens[0]} vs {id}")
        lineId = str(tokens[0])
        id = str(id)
        if (lineId == id):
            print("MATCH FOUND")
            existingProfile = True
            temp.write(f"{id},{strength},{int},{end},{spd}\n")
        else:
            temp.write(f"{line}")
    
    if existingProfile == False:
        temp.write(f"{id},{strength},{int},{end},{spd}\n")
    
    temp.close()
    profiles.close()

    os.replace("Temp", "Profiles")



bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is up and running")

@bot.tree.command(name = "start_fight")
async def start_f(interaction: discord.Interaction, min : int, max : int):
    profile = ProfileFromDiscord(interaction.user.id, interaction.user.name)
    profile.moves = MoveList.allValidMoves(profile)
    profile.display()
    playerParty = []
    hostParty = find_item_by_property(parties, "host", interaction.user.name)
    fight = Fight.Fight([], [], [], interaction.channel)
    if hostParty is None:
         playerParty.append(profile)
    else:
        playerParty = hostParty.members
    
    for player in playerParty:
        fighter = Fighter(player, True)
        fight.fighters.append(fighter)
        fight.team1.append(fighter)

    #fighter = Fighter(profile)
    #fight = Fight.Fight([fighter], [fighter], [], interaction.channel)
    fight.spawnEnemies(min, max)
    fight.orderFight()
    fights.append(fight)
    fight.turnCount = len(fight.fighters) - 1
    await fight.nextTurn()
    await interaction.response.send_message(f"Fight started. First Fighter: {fight.currentFighter().name}\n{fight.display()}")
    if fight.checkFinished():
        fights.remove(fight)
        print("Fight removed from memory")

@bot.tree.command(name = "profile", description="Input your stat points. You have 10 points!")
async def create_profile(interaction: discord.Interaction, str : int, int : int, end : int, spd : int):
    sum = str + int + spd + end
    if sum > 10:
        await interaction.response.send_message("Too many points allotted! Try again using 10 points!")
        return
    elif sum < 10:
        await interaction.response.send_message("Too few points allotted! Try again using 10 points!")
        return
    UpdateProfile(interaction.user.id, str, int, end, spd)
    await interaction.response.send_message("Profile saved.")



@bot.tree.command(name = "do")
async def do(interaction: discord.Interaction, input : int):
    user = interaction.user
    for fight in fights:
        for fighter in fight.fighters:
            if fighter.name == user.name and fight.currentFighter().name == user.name: #it's the user's turn for a fight
                print("User's turn for a fight")
                if fight.mode == '':
                    await interaction.response.send_message(fight.promptSelectMove()) #can be empty?
                    fight.mode = 'move'
                    return
                if fight.mode == 'move':
                    fight.selectedMove = fight.currentFighter().moves[input]
                    fight.mode = 'target'
                    targetList = fight.promptNextTarget()
                    await interaction.response.send_message(f"Selected Move: {fight.selectedMove.name}\n{targetList}")
                    return
                if fight.mode == 'target':
                    fight.targetCount += 1
                    target = fight.fighters[input]
                    fight.selectedMove.use(fight, target)
                    await fight.channel.send(f"{fighter.name} used {fight.selectedMove.name} on {target.name}")
                    if fight.targetCount >= fight.selectedMove.targetCount:
                        fight.mode = ''
                        fight.targetCount = 0
                        fight.currentFighter().updateCooldowns()
                        fight.selectedMove = None
                        await fight.nextTurn()
                        if fight.checkFinished() == True:
                            await interaction.response.send_message(f"FIGHT OVER!")
                            await fight.endFight()
                            fights.remove(fight)
                            print("Fight removed from memory")
                        else:
                            await interaction.response.send_message(f"{fight.display()}\n{fight.currentFighter().name}'s Turn. Do /do" )
                    else:
                        if fight.checkFinished() == True:
                            await interaction.response.send_message(f"FIGHT OVER!")
                            await fight.endFight()
                            fights.remove(fight)
                            return
                        targetList = fight.promptNextTarget()
                        await interaction.response.send_message(f"Selected Move: {fight.selectedMove.name}\n{targetList}")
                    
    
duelGivers = []
duelTakers = []
@bot.tree.command(name = "duel_invite")
async def duelInvite(interaction: discord.Interaction, name: str):
    duelGivers.append(interaction.user.name)
    duelTakers.append(name)
    await interaction.response.send_message(f"{interaction.user.name} challenges {name} to a duel!")

@bot.tree.command(name = "duel_accept")
async def duelAccept(interaction: discord.Interaction, name: str):
    takerName = interaction.user.name
    giverName = name
    duelTakers.remove(takerName)
    duelGivers.remove(giverName)
    
    taker = interaction.guild.get_member_named(takerName)
    giver = interaction.guild.get_member_named(giverName)

    takerPro = ProfileFromDiscord(taker.id, taker.name)
    takerPro.moves = MoveList.allValidMoves(takerPro)
    giverPro = ProfileFromDiscord(giver.id, giver.name)
    giverPro.moves = MoveList.allValidMoves(giverPro)

    takerF = Fighter(takerPro)
    giverF = Fighter(giverPro)

    duel = Fight.Fight([takerF, giverF], [takerF], [giverF], None)
    duel.orderFight()
    fights.append(duel)
    await interaction.response.send_message(f"Duel started! First Turn: {duel.currentFighter().name}")

parties = []
partyGivers = []
partyTakers = []
@bot.tree.command(name = "party_invite")
async def partyInvite(interaction: discord.Interaction, name: str):
    partyGivers.append(interaction.user.name)
    partyTakers.append(name)
    await interaction.response.send_message(f"{interaction.user.name} has invited {name} to a party!")


@bot.tree.command(name = "party_accept")
async def partyAccept(interaction: discord.Interaction, name: str):
    takerName = interaction.user.name
    giverName = name
    partyGivers.remove(name)
    partyTakers.remove(takerName)

    taker = interaction.guild.get_member_named(takerName)
    giver = interaction.guild.get_member_named(giverName)

    takerPro = ProfileFromDiscord(taker.id, taker.name)
    takerPro.moves = MoveList.allValidMoves(takerPro)
    giverPro = ProfileFromDiscord(giver.id, giver.name)
    giverPro.moves = MoveList.allValidMoves(giverPro)
    hostParty = find_item_by_property(parties, "host", giverName)
    if hostParty is None:
        hostParty = Party([takerPro, giverPro], giverName)
        parties.append(hostParty)
    else:
        hostParty.members.append(takerPro)

    await interaction.response.send_message(f"{interaction.user.name} has joined {name}'s party!")

    







bot.run(token)

#add 3+ team support and display team names next to targets ?
#break out of multi-target spells if the fight is over