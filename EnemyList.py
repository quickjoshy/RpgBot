from Profile import Profile
import MoveList
from Inventory import Inventory
import ItemList
Bandit = Profile("Bandit", 2, 0, 2, 3, [MoveList.TwinDaggers], Inventory([ItemList.Dagger], None, None, 10))
Wolf = Profile("Wolf", 5, 3, 0, 4, [MoveList.Bite], Inventory([ItemList.WolfHide], None, None, 0))
Zombie = Profile("Zombie", 0,0,0,0, [MoveList.Bite], Inventory([ItemList.HumanSkull], None, None, 5))
#NoviceWitch = Profile()
#Phantom = Profile()


Tier1 = [Bandit, Wolf, Zombie]




#Gorilla = Profile("Gorilla", )
#KillerRabbit = Profile()
#SentientArmor = Profile()


Tier2 = []


BossPro = Profile("Sillular", 3, 5, 10, 1, [MoveList.AcidSplash], Inventory(gold = 10, allItems = [], armor = None, weapon = None))



Tier3 = []





Tier4 = []




