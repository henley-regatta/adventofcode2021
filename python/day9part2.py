#!/usr/bin/python3
# Python solution for AOX 2021 Day 9, Part 2
#
# Given an input heightmap, find the "low points" - points where adjacent
# numbers have a bigger number (nb: number of sides reduces at edges/corners; There
# is no wrap-around). Adjacent means up/down/left/right; no diagonals
#
# Then, extend the low points into "basins" (areas bounded by 9s) such that
# each point other than a 9 is in one and one only basin. Count the size of each
# basin.

#inputfile = "data/day9test.txt"
inputfile = "data/day9part1.txt"

#Not great code but we do end up re-using these a lot
maxX=0
maxY=0
heightmap=[]
shadowmap=[]

#-----------------------------------------------------------------------
def readHeightMapFromFile(file) :
    global heightmap
    with open(file,'r') as hmfile:
        for l in hmfile:
            mapLine=[int(n) for n in l.strip()]
            if len(mapLine)>0 :
                heightmap.append(mapLine)

    global maxX
    maxX=len(heightmap[0]) -1
    global maxY
    maxY=len(heightmap) -1

#-----------------------------------------------------------------------
def getAdjacents(point) :
    global maxX
    global maxY
    x=point[0]
    y=point[1]
    adjacents=[]
    for dY in [y-1,y,y+1] :
        for dX in [x-1,x,x+1] :
            #selector is a boundary condition test (line 1) and a
            #non-diagonal test (line 2)
            if (dX>=0 and dX<=maxX and dY>=0 and dY<=maxY and
                ((dX==x and dY!=y) or (dX!=x and dY==y)) ):
                adjacents.append([dX,dY])
    return adjacents
#-----------------------------------------------------------------------
def findLowPointsOnMap() :
    global heightmap
    global maxX
    global maxY
    lowPoints=[]

    for y in [y for y in range(len(heightmap))] :
        for x in [x for x in range(len(heightmap[0]))] :
            p = heightmap[y][x]
            #Work out the adjacent numbers according to the rules above and
            #accounting for edges:
            adjacents=getAdjacents([x,y])

            isSmallest=True
            for t in adjacents:
                if p >= heightmap[t[1]][t[0]] :
                    isSmallest=False
            if isSmallest :
                lowPoints.append({'low' : p, 'pos' : [x,y]})

    return lowPoints
#-----------------------------------------------------------------------
def calcLowPointScore(lowPoints) :
    riskScore=0
    for p in lowPoints :
        #risk score is 1 + height of lowpoint:
        riskScore += p['low'] +1
    return riskScore
#-----------------------------------------------------------------------
#Ah recursive procedures my favourite
def growBasin(point) :
    global shadowmap
    #extend search dimensions from point
    x=point[0]
    y=point[1]
    subBasin=[]
    #build list of next points to check
    adjacents=getAdjacents(point)
    for p in adjacents:
        if heightmap[p[1]][p[0]] != 9 and shadowmap[p[1]][p[0]] == False :
            shadowmap[p[1]][p[0]] = True
            subBasin.append(heightmap[p[1]][p[0]])
            subBasin.extend(growBasin(p))
    return subBasin
#-----------------------------------------------------------------------
def findBasins(lowPoints) :
    #This is just a recursive "growth" algorithm that stops at an edge
    #or a 9 *provided we trust the input*. If we have a global "shadow map" showing
    #which points are already in a basin, we can avoid that trap.
    # (nb pythonic behaviour: we inherit heightmap from our caller - main, and
    #     pass shadowmap down the tree)
    global shadowmap
    basins=[]
    for p in lowPoints :
        basin = [p['low']]
        shadowmap[p['pos'][1]][p['pos'][0]] = True
        basin.extend(growBasin(p['pos']))
        basins.append({'start' : p['low'], 'startPos' : p['pos'],
                       'size' : len(basin), 'members' : basin})
    return basins
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    readHeightMapFromFile(inputfile)
    #validateMap(heightmap)
    lowPoints = findLowPointsOnMap()

    print(lowPoints)
    print(f"Overall Risk Score of Low Points: {calcLowPointScore(lowPoints)}")

    #Initialise the shadowmap we use to track inclusion in a basin
    shadowmap=[[False for x in range(len(heightmap[0]))] for y in range(len(heightmap))]
    basins=findBasins(lowPoints)
    print(basins)
    #The Exam Question is now "Find the biggest 3 basins and multiple their size together"
    bsizes=[]
    for b in basins :
        bsizes.append(b['size'])
    bsizes = sorted(bsizes)
    big3=bsizes[-3:]
    print(f"all basin sizes: {bsizes}")
    print(f"The biggest 3 basins have size: {big3}")
    sum=big3[0] * big3[1] * big3[2]
    print(f"basin product (answer) = {sum}")
