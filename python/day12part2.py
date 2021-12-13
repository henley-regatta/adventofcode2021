#!/usr/bin/python3
# Python solution for AOC 2021 Day 12, Part 2
#
# Given input in the form of a series of connections between
# caves, enumerate all paths from "start" to "end".
# A valid path can go through "big" (upper-case) caves multiple times,
# but can only pass through "small" (lower-case) caves at most once.
# PART TWO RULE CHANGE: a *single* "small" cave (with the exception of "start"
# and "end") can be visited twice in a given path. This is quite annoying.
#inputfile = "data/day12test.txt"
#inputfile = "data/day12test2.txt"
#inputfile = "data/day12test3.txt"
inputfile = "data/day12part1.txt"

#Yes I know you shouldn't use Global Variables. Probably ought to define a class
#instead. But they're so handy and this is such a toy problem....

smallCaves={}
connections={}
validRoutes=[]

# ---------------------------------------------------------------
def loadCavesAndConnections(file) :
    global smallCaves
    global connections
    with open(file,'r') as spelunky :
        for c in spelunky:
            conn=c.strip().split('-')
            if len(conn)==2 :
                for cave in conn :
                    if cave not in smallCaves :
                        if cave=="start" or cave=="end" or cave.islower() :
                            smallCaves[cave]=True
                        else :
                            smallCaves[cave]=False
                if conn[0] not in connections :
                    connections[conn[0]] = [conn[1]]
                else :
                    connections[conn[0]].append(conn[1])
                if conn[1] not in connections :
                    connections[conn[1]] = [conn[0]]
                else :
                    connections[conn[1]].append(conn[0])

# ---------------------------------------------------------------
def findRouteToEnd(routeSoFar,hasVisitedASmallCaveTwice) :
    global smallCaves
    global connections
    global validRoutes
    #From cave "x", all possible destinations are given in it's
    #connections. Route is complete IF it connects to "end"
    #Connection is valid IF: connection is a big cave OR connection
    #has not already been visited (isn't in the route) OR no other small
    #cave has been visited twice either
    depth=len(routeSoFar)
    print(f"Looking for paths from {routeSoFar}. Possibilities: {connections[routeSoFar[-1]]}")
    for nextCave in connections[routeSoFar[-1]] :
        nextPath = routeSoFar + [nextCave]
        #nextPath.append(nextCave) # Might not be valid, but shouldn't matter because:
        print(f"\t{depth} Checking {nextCave}",end=":")
        #terminus if we've ended up next to end:
        if nextCave == "end" :
            print("finished path")
            print(f"Route: {nextPath}")
            validRoutes.append(nextPath)
        #valid if next step is big:
        elif not smallCaves[nextCave] :
            print("ok because big")
            findRouteToEnd(nextPath,hasVisitedASmallCaveTwice)
        #valid if next step is small BUT hasn't been visited:
        elif nextCave not in routeSoFar :
            print("ok because small but unvisited")
            findRouteToEnd(nextPath,hasVisitedASmallCaveTwice)
        #Part2 rule extension. If it's not "start" AND no other small cave
        #has been visited twice, it can be visited again.
        elif nextCave != "start" and not hasVisitedASmallCaveTwice :
            print("ok because small, but no other small has been visited twice")
            findRouteToEnd(nextPath,True)
        #And that's all the valid moves we can make. nextPath gets discarded here.
        else :
            print("invalid.")
    return

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    loadCavesAndConnections(inputfile)
    print(smallCaves)
    print(connections)
    findRouteToEnd(["start"],False)
    for r in validRoutes :
        print(f"Valid route: {r}")
    print(f"Found {len(validRoutes)} valid routes from start->end")
