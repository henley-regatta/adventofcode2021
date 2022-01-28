#!/usr/bin/python3
#
# Play "Dirac Dice". A Game For Two Players.
#
# Play occurs on a circular track with 10 spots. Starting position is
# arbitrary. A turn consists of 3D3 (summed 3 rolls) moving clockwise (upwards)
# wrapping around 10->1 as required. Score is increased by the value landed on.
# Winning is first player to 21 points.
#
# Part 2 uses a "Dirac Dice". *every* combination is scored on *every* roll.
# Calculate how many times each player wins.
#
# Every possible rollscore (3d3 = range 3->9 across 3*3*3 = 27 combinations) is
# derived at each turn. This is high-order deterministic, first thing to do is
# work out just how high-order.
#
# This is my umpteenth attempt to solve this problem. I knew the naieve "keep
# track of every game possible" approach wouldn't work but I hadn't appreciated
# just how quickly it goes bonkers - here's a log of the first 5 moves; it crashed
# on the 6th with >20GB memory allocated :
# Turn 1 has 27 games in progress; games completed by player: [0, 0]
# Turn 2 has 729 games in progress; games completed by player: [0, 0]
# Turn 3 has 19683 games in progress; games completed by player: [0, 0]
# Turn 4 has 531441 games in progress; games completed by player: [0, 0]
# Turn 5 has 10989675 games in progress; games completed by player: [3359232, 0]
#
# The approach I've taken relies on the following insights to the problem:
#  * Although each turn consists of 3 dice rolls, we only update state after
#    all 3 have been rolled. We have a montecarlo distribution across the 7
#    possible outcomes.
#  * As we're playing on a fixed board 1-10 we can pre-calculate, from the
#    rolls and distribution, where we'll land and how many times we'll land
#    there from a given start position.
#  * From these two observations we no longer need to keep track of individual
#    games, instead we only need to track the number of games in-flight that
#    reside on a given "space"
#  * As we iterate, every game where a player meets or exceeds the target score
#    is dropped. If we've done the accounting properly, those games "disappear"
#    from the state vector *for both players*.
#  * Because turns are iterative p0->p1->p0, we need to track BOTH players scores
#    for a given state.
#  * This leads us to a 4-dimensional state vector. Since I'm mostly interested
#    in scores, the higher-order dimensions track those for both players. The inner
#    dimensions track the piece positions for each player, and the innermost
#    value within those 4 dimensions is a simple counter of the number of games
#    that state exists in at the current turn.
#    This state "hypercube" has dimensions s0=[0-20], s1=[0-20], p0=[1-10], p1=[1-10]
#    (although in practice p0/p1 are 0-9 and we fiddle the maths to make it work for
#     scoring)
#
# The core of the algorithm is thus:
#   * Work out all the end-states and score deltas from a given start position
#   * Initialise a state-hypercube with the starting game (put a "1" as the value
#     in the plot of scores = 0,0 at the x/y coordinates corresponding to the
#     start positions)
#   * Set the player-of-interest to the first player
#   * Play turns until there are no more games in progress:
#       + Initialise an unoccupied "nextState" hypercube
#       + For each occupied position on the state-hypercube :
#          - Calculate the resulting states for all moves possible from that state
#          - If the resulting states have scores over the threshold, count those
#            up, add them to player-of-interest's games won counter.
#          - Apply resulting states under the score threshold to the "nextState"
#            structure. Update a counter of games-in-progress with the occurrences
#            found.
#       + if the final value of games-in-progress is > 0, move "nextState" to
#         "currentState" and swap the player-of-interest over. Iterate.
#    * Work out who won the most games. The number of times they won is the
#      puzzle answer.
#TEST:
#positions=[4,8]
#LIVE DATA:
positions=[9,6]

targetScore=21
#-----------------------------------------------------------------------
# DONE:
def calcScoreCombos() :
    scoreCombos=[]
    for a in range(1,4) :
        for b in range(1,4) :
            for c in range(1,4) :
                scoreCombos.append(a+b+c)
    return scoreCombos
#-----------------------------------------------------------------------
# DONE:
def calcFinishPositions(scoreCombos) :
    finishPositions=[]
    for f in range(1,11) :
        pos=[]
        for s in scoreCombos :
            t=(f+s)%10
            if t==0 :
                t=10
            pos.append(t)
        finishPositions.append(pos)
    return finishPositions
#-----------------------------------------------------------------------
# DONE:
def calcFromToCounters(finishPositions) :
    fromToCounters={}
    for f in range(len(finishPositions)) :
        tCounts={}
        for t in range(1,11) :
            if t in finishPositions[f] :
                tCounts[t] = finishPositions[f].count(t)
        fromToCounters[f+1]=tCounts
    return fromToCounters

#-----------------------------------------------------------------------
def calcUpdateFromPosition(iterators,fromScore,fromPosition,fromOccurrences) :
    toPositions={}
    for tPos in iterators[fromPosition] :
        nScore = fromScore + tPos
        toOccurrences = fromOccurrences * iterators[fromPosition][tPos]
        if nScore in toPositions :
            toPositions[nScore][tPos] = toOccurrences
        else :
            toPositions[nScore]={tPos:toOccurrences}
    return toPositions

#-----------------------------------------------------------------------
def initTurnStruct() :
    return [[[[0 for y in range(1,11)] for x in range(1,11) ] for s1 in range(21)] for s0 in range(21)]
#-----------------------------------------------------------------------
def countGamesInProgress(turnStruct) :
    inProgress=0
    for s in turnStruct :
        for p0 in s :
            for p1 in p0 :
                inProgress += p1
    return inProgress
#-----------------------------------------------------------------------
def dumpTurnStruct(turnStruct) :
    for s1 in range(len(turnStruct[s0])) :
        for p0 in range(len(turnStruct[s0][s1])) :
            for p1 in range(len(turnStruct[s0][s1][p0])) :
                if turnStruct[s0][s1][p0][p1] > 0 :
                    print(f"score [{s0},{s1}] at position [{p0},{p1}] occurs {turnStruct[s0][s1][p0][p1]} times")
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# Key insight driving this re-write: As games end, the number of games
# underway is pruned for *both* players, not just the winning one. How to
# represent this?
# Also, we've been massively over-counting the number of games in progress -
# a given game for player X "only" has 1 set of ancestor games for player Y not
# *all* games for that player. r
if __name__ == "__main__" :
    posIterators=calcFromToCounters(calcFinishPositions(calcScoreCombos()))
    tThis = initTurnStruct()
    tThis[0][0][positions[0]-1][positions[1]-1] = 1
    gamesWon=[0,0]
    stillGamesToPlay=True
    p=0
    i=0
    while stillGamesToPlay :
        tNext = initTurnStruct()
        gamesInProgress=0
        for s0 in range(len(tThis)) :
            for s1 in range(len(tThis[s0])) :
                for p0 in range(len(tThis[s0][s1])) :
                    for p1 in range(len(tThis[s0][s1][p0])) :
                        #Only play from this position if there's a game in progress
                        #from here:
                        if tThis[s0][s1][p0][p1] > 0 :
                            cPos=p1+1
                            s=s1
                            if p == 0 :
                                cPos=p0+1
                                s=s0
                            toPos=calcUpdateFromPosition(posIterators,s,cPos,tThis[s0][s1][p0][p1])
                            for tS in toPos.keys() :
                                for tP in toPos[tS].keys() :
                                    tS1=tS
                                    tS0=s0
                                    tP0=p0
                                    tP1=tP-1
                                    if p == 0 :
                                        tS1=s1
                                        tS0=tS
                                        tP0 = tP-1
                                        tP1 = p1
                                    if tS < targetScore :
                                        if tNext[tS0][tS1][tP0][tP1] > 0 :
                                            tNext[tS0][tS1][tP0][tP1] += toPos[tS][tP]
                                        else :
                                            tNext[tS0][tS1][tP0][tP1] = toPos[tS][tP]
                                        gamesInProgress += tNext[tS0][tS1][tP0][tP1]
                                    else :
                                        gamesWon[p] += toPos[tS][tP]
        #end of turn, update counters
        if gamesInProgress > 0 :
            p=(p+1)%2
            tThis=tNext
        else :
            stillGamesToPlay=False
        i+=1
        totGames = gamesInProgress + gamesWon[0] + gamesWon[1]
        print(f"After {i} turns, {gamesInProgress} games underway; won {gamesWon}. Total = {totGames}.")

    #And the little bit of "give me the answer" magic the problem demands
    winner="Player 1"
    winningScore = gamesWon[1]
    if gamesWon[0]>gamesWon[1] :
        winner="Player 0"
        winningScore = gamesWon[0]
    print(f"\nThe winner was {winner} and they won {winningScore} times.")
