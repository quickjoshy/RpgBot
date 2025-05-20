from Move import Move
import Move as MoveMod
import Profile
import UniqueMoves
Punch = Move("Punch", 1, MoveMod.typeDmg, 2, Profile.strStat, 1, [None], [None], 0)
TwinDaggers = Move("Twin Daggers", 2, MoveMod.typeDmg, 1, Profile.spdStat, .5, [Profile.spdStat], [2], 0)
AcidSplash = Move("Acid Splash", 3, MoveMod.typeDmg, 3, Profile.intStat, 0, [Profile.intStat], [3], 2)
Restoration = Move("Restoration", 1, MoveMod.typeHeal, 3, Profile.intStat, 1, [Profile.intStat], [3], 2)
GroupRestoration = Move("Group Restoration", 3, MoveMod.typeHeal, 3, Profile.intStat, 1, [Profile.intStat], [5], 3)
Bite = Move("Bite", 1, MoveMod.typeDmg, 1, Profile.strStat, 1, [None], [None], 0)
LifeDrain = UniqueMoves.LifeDrainMove("Life Drain", 1, MoveMod.typeDmg, 3, Profile.intStat, 1, [Profile.intStat], [3], 1)
MoveList = [Punch, TwinDaggers, AcidSplash, Restoration, LifeDrain, GroupRestoration]

def allValidMoves(profile):
    validMoves = []
    for move in MoveList:
        valid = True
        if(move.reqStats[0] is None):
            validMoves.append(move)
            continue
        for i in range(len(move.reqStats)):
            if(profile.stats[move.reqStats[i]] < move.reqAmounts[i]):
                valid = False
                break
        if valid == True:
            validMoves.append(move)
    return validMoves