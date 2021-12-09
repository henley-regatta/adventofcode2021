#!/usr/bin/python3
# Python solution for AOX 2021 Day 7, Part 2
# Given an input of horizontal positions work out the optimum position to
# move to given each move costs n(x). It's something about crabs blah blah

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
def getCrabClusters(crabs) :
    clusterList={}
    for c in crabs :
        if c in clusterList:
            clusterList[c]+=1
        else :
            clusterList[c] = 1
    return clusterList

# ------------------------------------------------------------------------
# optimisation to pre-calculate costs ONCE
def calcStepCosts(maxStepSize) :
    stepCosts=[]
    for d in range(maxStepSize+1) :
        cost=0
        stepc=1
        for s in range(d) :
            cost += stepc
            stepc += 1
        stepCosts.append(cost)
    return stepCosts

# ------------------------------------------------------------------------
def costToConverge(crabClusters,stepCosts,pos) :
    cost = 0
    for c,n in crabClusters.items() :
        dist=abs(pos-c)
        cost += stepCosts[dist] * n
    return cost

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
if __name__ == "__main__" :
    crabs = getCrabs(inputfile)
    eigenCrabs = uniquePos(crabs)
    print(f"There are {len(crabs)} crabs in {len(eigenCrabs)} positions strewn from {crabs[0]} to {crabs[-1]}")
    #Under Part2 rules we need to consider ALL positions. But an optimisation is
    #to work out combined costs by counting all crabs as clusters.
    clusters=getCrabClusters(crabs)
    #And also to pre-calculate the costs to move X steps given it's an iterative
    #series....
    stepCosts = calcStepCosts(crabs[-1])
    print(f"sense check: found {len(clusters)} clusters")
    print(f"cost per stepDistance: {stepCosts}")

    convergeCosts=[]
    # WE GOT LUCKY in part 1 that the answer fell on an existing crab's position
    # for part 2 we can't assume that - the hint is in the sample data. We must
    # search the whole "range" regardless of whether a spot holds a crab or not
    for p in range(crabs[-1]) :
        convergeCosts.append([p,costToConverge(clusters,stepCosts,p)])

    #The answer is just the array element with the smallest cost-to-converge:
    minCost=9999999999
    minCostPos=99999999999
    for cVec in convergeCosts :
        if cVec[1] < minCost :
            minCost = cVec[1]
            minCostPos = cVec[0]

    print(f"The Crabs should converge to position {minCostPos} at a total fuel cost of {minCost}")
