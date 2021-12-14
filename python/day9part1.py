#!/usr/bin/python3
# Python solution for AOC 2021 Day 9, Part 1
#
# Given an input heightmap, find the "low points" - points where adjacent
# numbers have a bigger number (nb: number of sides reduces at edges/corners; There
# is no wrap-around). Adjacent means up/down/left/right; no diagonals
#
# Then do a bit of math on the points to get an answer

#inputfile = "data/day9test.txt"
inputfile = "data/day9part1.txt"

#-----------------------------------------------------------------------
def readHeightMapFromFile(file) :
    map=[]
    with open(file,'r') as hmfile:
        for l in hmfile:
            mapLine=[int(n) for n in l.strip()]
            if len(mapLine)>0 :
                map.append(mapLine)
    return map
#-----------------------------------------------------------------------
def validateMap(heightmap) :
    height=len(heightmap)
    width=len(heightmap[0])
    for r in heightmap :
        print(r)

    for l in heightmap :
        if len(l) != width :
            print(f"Map isn't straight!")
    print(f"Heightmap has dimensions {height} rows by {width} columns")
#-----------------------------------------------------------------------
def findLowPointsOnMap(heightmap) :
    maxX=len(heightmap[0])-1  # zero-indexing
    maxY=len(heightmap)-1     # zero-indexing
    lowPoints=[]

    for y in [y for y in range(len(heightmap))] :
        for x in [x for x in range(len(heightmap[0]))] :
            p = heightmap[y][x]
            #Work out the adjacent numbers according to the rules above and
            #accounting for edges:
            adjacents=[]
            for dY in [y-1,y,y+1] :
                for dX in [x-1,x,x+1] :
                    #print(f"p=[{x},{y}] dPos=[{dX},{dY}]",end=" ")
                    #selector is a boundary condition test (line 1) and a
                    #non-diagonal test (line 2)
                    if (dX>=0 and dX<=maxX and dY>=0 and dY<=maxY and
                        ((dX==x and dY!=y) or (dX!=x and dY==y)) ):
                        adjacents.append(heightmap[dY][dX])
                        #print(heightmap[dY][dX])
                    #else :
                    #    print("(reject)")
            #print(f"point at [{x},{y}] is {p} with adjacent vals: {adjacents}")
            #Makes the comparison so much easier:
            isSmallest=True
            for t in adjacents:
                if p >= t :
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
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    heightmap = readHeightMapFromFile(inputfile)
    #validateMap(heightmap)
    lowPoints = findLowPointsOnMap(heightmap)

    print(lowPoints)
    print(f"Overall Risk Score of Low Points: {calcLowPointScore(lowPoints)}")
