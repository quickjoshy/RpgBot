import Profile as CharStat
class Fighter:
    def __init__(self, profile, player = False):
        self.profile = profile
        self.inventory = profile.inventory
        self.name = profile.name
        self.moves = profile.moves
        self.stats = profile.stats.copy()
        armor = self.inventory.armor
        wep = self.inventory.weapon
        if armor is not None:
            for i in range(len(armor.statIndices)):
                statIndex = armor.statIndices[i]
                self.stats[statIndex] += armor.bonuses[i]
        if wep is not None:
            for i in range(len(wep.statIndices)):
                statIndex = wep.statIndices[i]
                self.stats[statIndex] += wep.bonuses[i]
        self.maxHp = 5 + (2 * self.stats[CharStat.endStat])
        self.hp = self.maxHp
        self.cooldowns = [0] * len(self.moves)
        self.player = player

    def updateCooldowns(self):
        for i in range(len(self.moves)):
            if self.cooldowns[i] > 0:
                self.cooldowns[i] -= 1