#!/usr/bin/python3
# Python solution for AOC 2021 Day 7, Part 1
# Given an input of horizontal positions work out the optimum position to
# move to given each move costs (1). It's something about crabs blah blah

#inputfile = "data/day7test.txt"
inputfile = "data/day7part1.txt"

# ------------------------------------------------------------------------
def getCrabs(inputfile) :
    crabpos=[]
    with open(inputfile,'r') as crabs :
        for l in crabs:
            w=l.split(',')
            for c in w:
                crabpos.append(int(c))
    return sorted(crabpos)

# ------------------------------------------------------------------------
def uniquePos(crabs) :
    uniquePositions = []
    for c in crabs :
        if c not in uniquePositions :
            uniquePositions.append(c)
    return uniquePositions

# ------------------------------------------------------------------------
def costToConverge(crabs,pos) :
    cost = 0
    for c in crabs:
        cost += abs(pos-c)
    return cost

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
if __name__ == "__main__" :
    crabs = getCrabs(inputfile)
    eigenCrabs = uniquePos(crabs)
    print(f"There are {len(crabs)} crabs in {len(eigenCrabs)} positions strewn from {crabs[0]} to {crabs[-1]}")
    convergeCosts=[]
    for p in eigenCrabs :
        convergeCosts.append([p,costToConverge(crabs,p)])
    #The answer is just the array element with the smallest cost-to-converge:
    minCost=9999999999
    minCostPos=99999999999
    for cVec in convergeCosts :
        if cVec[1] < minCost :
            minCost = cVec[1]
            minCostPos = cVec[0]

    print(f"The Crabs should converge to position {minCostPos} at a total fuel cost of {minCost}")
