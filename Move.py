import random
typeDmg = 1
typeHeal = 2
class Move:
    def __init__(self, name, targetCount, type, baseVal, relStatIndex, statRatio, reqStats, reqAmounts, cooldown):
        self.name = name
        self.targetCount = targetCount
        self.type = type
        self.baseVal = baseVal
        self.relStatIndex = relStatIndex
        self.statRatio = statRatio
        self.reqStats = reqStats
        self.reqAmounts = reqAmounts
        self.cooldown = cooldown

    def heal(self, caster, target, amount):
        target.hp += amount
        if(target.hp > target.maxHp):
            target.hp = target.maxHp

    def dmg(self, caster, target, amount):
        target.hp -= amount


    def healMove(self, caster, target):
        healNum = (self.baseVal + (self.statRatio * caster.stats[self.relStatIndex]))
        self.heal(caster, target, healNum)
        print(f"Healed {target.name}! They have {target.hp} hp remaining!")

    def dmgMove(self, caster, target):
        damageNum = (self.baseVal + (self.statRatio * caster.stats[self.relStatIndex]))
        self.dmg(caster, target, damageNum)
        print(f"Hit {target.name}! They have {target.hp} hp remaining!")
        return damageNum
    

    def use(self, fight, target):
        currFighter = fight.currentFighter()
        print(f"CurrFighter: {currFighter.name}; Move: {self.name}; Target: {target.name}")
        if(self.type == typeDmg):
                self.dmgMove(caster = currFighter ,target=target)
                if target.hp <= 0:
                    caster = fight.currentFighter()
                    fight.kill(caster, target)
        if(self.type == typeHeal):
                self.healMove(caster = currFighter ,target=target)
        moveIndex = currFighter.moves.index(self)
        currFighter.cooldowns[moveIndex] = self.cooldown + 1