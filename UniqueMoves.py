from Move import Move



class LifeDrainMove(Move):
    
    def __init__(self, name, targetCount, type, baseVal, relStatIndex, statRatio, reqStats, reqAmounts, cooldown):
        super().__init__(name, targetCount, type, baseVal, relStatIndex, statRatio, reqStats, reqAmounts, cooldown)


    def use(self, fight, target):
        currFighter = fight.currentFighter()
        damageNum = self.dmgMove(currFighter, target)
        if(target.hp <= 0):
            fight.kill(currFighter, target)
        self.heal(currFighter, currFighter, .5 * damageNum)
        if currFighter.hp > currFighter.maxHp:
            currFighter.hp = currFighter.maxHp
        moveIndex = currFighter.moves.index(self)
        currFighter.cooldowns[moveIndex] = self.cooldown + 1



class Consumables(Move):

    def __init__(self, name, targetCount, type, baseVal, relStatIndex, statRatio, reqStats, reqAmounts, cooldown):
        super().__init__(name, targetCount, type, baseVal, relStatIndex, statRatio, reqStats, reqAmounts, cooldown)

    def use(self, fight):
        currFighter = fight.currentFighter()
        #prompt items
        #call .use on item