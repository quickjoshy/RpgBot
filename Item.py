typeArmor = 1
typeWeapon = 2

class Item:
    def __init__(self, name, value):
        self.value = value
        self.name = name
        pass



class Equippable(Item):
    def __init__(self, name, value, itemType, statIndices, bonuses):
        super().__init__(name, value)
        self.itemType = itemType
        self.statIndices = statIndices
        self.bonuses = bonuses
        



class Consumable(Item):
    def __init__(self):
        super().__init__()

    def use(self):
        pass