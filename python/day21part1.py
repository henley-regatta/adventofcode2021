#!/usr/bin/python3
# Python solution for AOC 2021 Day 21 Part 1
#
# Play "Dirac Dice". A Game For Two Players.
#
# Play occurs on a circular track with 10 spots. Starting position is
# arbitrary. A turn consists of 3D6 (summed 3 rolls) moving clockwise (upwards)
# wrapping around 10->1 as required. Score is increased by the value landed on.
# Winning is first player to 1000 points.
#
# Part 1 uses a "Deterministic Dice". This rolls 1, then 2, then 3 etc up to
# 100 (at which point it wraps around)

#globs
lastDieValue=100
rollCounter=0
#TEST:
#positions=[4,8]
#LIVE DATA:
positions=[9,6]
scores=[0,0]
#-----------------------------------------------------------------------
def calcRollScore() :
    global lastDieValue
    global rollCounter
    def rollDice(fromValue) :
        val=fromValue+1
        if val>100 :
            val=val%100
        return val
    v1=rollDice(lastDieValue)
    v2=rollDice(v1)
    v3=rollDice(v2)
    lastDieValue=v3
    rollCounter+=3
    return v1+v2+v3
#-----------------------------------------------------------------------
def takeTurn(player) :
    global positions
    global scores
    roll=calcRollScore()
    oldPos=positions[player]
    positions[player] = (oldPos+roll)%10
    if positions[player]==0 :
        positions[player] = 10
    scores[player] += positions[player]
    print(f"{player} rolled {roll}, moves from {oldPos} to {positions[player]}, score now {scores[player]}")
    return scores[player]
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    gameWon=False
    nextPlayer=0
    turns=0
    while not gameWon :
        turns+=1
        score=takeTurn(nextPlayer)
        if score>=1000 :
            gameWon=True
            print(f"Player {nextPlayer} won with a score of {score} after {turns} turns")
        nextPlayer=(nextPlayer+1)%2


    print(f"Losing player had score of {scores[nextPlayer]} and the dice was thrown {rollCounter} times")
    print(f"Part 1 answer is therefore {scores[nextPlayer] * rollCounter}")
