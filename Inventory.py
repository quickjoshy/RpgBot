import Item as ItemMod
class Inventory:
    def __init__(self, allItems, armor, weapon, gold):
        self.allItems = allItems
        self.armor = armor
        self.weapon = weapon
        self.gold = gold
    

    def addItem(self, item):
        self.allItems.append(item)

    def equipItem(self, item):
        if(item.itemType == ItemMod.typeWeapon):
            self.weapon = item
        elif(item.itemType == ItemMod.typeArmor):
            self.armor = item
    
    def addGold(self, amount):
        self.gold += amount