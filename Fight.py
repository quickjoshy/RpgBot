import random
import EnemyList
import Move as MoveMod
from Fighter import Fighter
class Fight:
    def __init__(self, fighters, team1, team2, channel):
        self.fighters = fighters
        self.team1 = team1
        self.team2 = team2
        self.turnCount = 0
        self.graveyard = []
        self.channel = channel
        self.mode = ''
        self.targetCount = 0
        self.selectedMove = None
    
    def orderFight(self):
        self.fighters.sort(key=lambda fighter: fighter.profile.spd, reverse = True)
    
    def checkFinished(self):
        if(len(self.team1) == 0 or len(self.team2) == 0):
            return True
        else:
            return False

    async def nextTurn(self):
        self.turnCount += 1
        if(self.turnCount >= len(self.fighters)):
                self.turnCount = 0
        #while fighter.player == False fighter.sim()
        currentFighter = self.currentFighter()
        while currentFighter.player == False:
            #go through his moves starting with the highest. For each target in its target count, pick a random enemy
            enemyTeam = None
            if currentFighter in self.team2:
                enemyTeam = self.team1
            else:
                enemyTeam = self.team2
            for i in reversed(range(len(currentFighter.moves))):
                if currentFighter.cooldowns[i] == 0:
                    move = currentFighter.moves[i]
                    for j in range(move.targetCount):
                        target = None
                        if move.type == MoveMod.typeDmg:
                            target = random.choice(enemyTeam)
                            move.use(self, target)
                            if self.checkFinished() == True:
                                await self.channel.send("FIGHT OVER! Players lose!")
                                return
                        elif move.type == MoveMod.typeHeal:
                            target = self.prioHealTarget(currentFighter)
                            move.use(self, target)
                        await self.channel.send(f"{currentFighter.name} used {move.name} on {target.name}")
            self.turnCount += 1
            currentFighter.updateCooldowns()
            if(self.turnCount >= len(self.fighters)):
                self.turnCount = 0
            currentFighter = self.currentFighter()
        if self.checkFinished() == False:
            await self.channel.send(f"{currentFighter.name}'s turn\n{self.display()}")

    def getTeam(self, fighter):
        if fighter in self.team2:
            return self.team2
        else:
            return self.team1

    def prioHealTarget(self, fighter):
        team = self.getTeam(fighter)
        percentHp = team[0].hp / team[0].maxHp
        for ally in team:
            percentHp = min(ally.hp / ally.maxHp, percentHp)


    def promptNextTarget(self):
        msg = ''
        for i in range(len(self.fighters)):
            #print(f"{i}: {self.fighters[i].name} ; Hp: {self.fighters[i].hp}")
            msg += "{}: {} ; Hp: {}\n".format(i, self.fighters[i].name, self.fighters[i].hp)
        return msg
    
    def promptSelectMove(self):
        currFighter = self.fighters[self.turnCount]
        msg = ''
        for i in range(len(currFighter.moves)):
            if currFighter.cooldowns[i] == 0:
                msg += "{}: {}\n".format(i, currFighter.moves[i].name)
        return msg

    def kill(self, caster, target):
        self.graveyard.append(target)
        self.fighters.remove(target)
        if(target in self.team1):
            self.team1.remove(target)
        else:
            self.team2.remove(target)
        if(caster == target):
            self.turnCount -= 1
            return
        self.turnCount = self.fighters.index(caster)
        self.checkFinished()
    
    def currentFighter(self):
        return self.fighters[self.turnCount]
    

    def spawnEnemies(self, minRatio, maxRatio):
        for p in range(len(self.team1)):
            enemyCount = random.randint(minRatio, maxRatio)
            for i in range(enemyCount):
                enemyPro = random.choice(EnemyList.Tier1)
                enemyF = Fighter(enemyPro)
                self.fighters.append(enemyF)
                self.team2.append(enemyF)

    
    def display(self):
        msg = ''
        for fighter in self.fighters:
            msg += "{} hp: {}\n".format(fighter.name, fighter.hp)

        return msg

    async def endFight(self):
        goldSum = 0
        players = []
        itemPool = []
        for deadGuy in self.graveyard:
            if deadGuy.player == False:
                goldSum += deadGuy.inventory.gold
                for item in deadGuy.inventory.allItems:
                    itemPool.append(item)
        for fighter in self.fighters:
            if fighter.player == True:
                players.append(fighter.profile)
        for fighter in self.graveyard:
            if fighter.player == True:
                players.append(fighter.profile)
        
        looterPool = players.copy()
        for item in itemPool:
            if len(looterPool) == 0:
                looterPool = players.copy()
            winner = random.choice(looterPool)
            winner.inventory.allItems.append(item)
            looterPool.remove(winner)
            await self.channel.send(f"{winner.name} gains {item.name}")
        
        perPlayer = int(goldSum / len(players))
        for player in players:
            player.inventory.gold += perPlayer
        
        await self.channel.send(f"Each player gains {perPlayer} gold")