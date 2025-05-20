from Item import Item, Equippable, Consumable
import Item as ItemMod
import Profile

LeatherTunic = Equippable("Leather Tunic", 10, ItemMod.typeArmor, [Profile.endStat], [2])

WolfHide = Item("Wolf Hide", 30)
Dagger = Equippable("Dagger", 15, ItemMod.typeWeapon, [Profile.spdStat], [2])
HumanSkull = Item("Human Skull", 15)