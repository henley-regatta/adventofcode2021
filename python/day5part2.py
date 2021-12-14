#!/usr/bin/python3
# Python solution for AOC 2021 Day 5, Part 2
#
# Given a set of line-definition inputs, find the number of points of
# intersection of those lines.  Lines can now be diagonal
# (Blah blah something about geothermal vents)

#inputfile="data/day5test.txt"
inputfile="data/day5part1.txt"

# ----------------------------------------------------------------------------
def readFileToLineDefinitions(filename) :
    ventlines = []
    with open(filename,'r') as linedefs :
        for linedef in linedefs:
            #format is <x1>,<y1> -> <x2>,<y2>
            words=linedef.strip().split()
            if words[1] != '->' :
                continue # not a valid line
            p1=words[0].split(',')
            pos1=[int(p1[0]),int(p1[1])]
            p2=words[2].split(',')
            pos2=[int(p2[0]),int(p2[1])]
            ventlines.append([pos1,pos2])
    return ventlines

# ----------------------------------------------------------------------------
def calcExtents(vents) :
    maxX=0
    maxY=0
    for vent in vents :
        for pos in vent :
            if pos[0] > maxX : maxX = pos[0]
            if pos[1] > maxY : maxY = pos[1]
    return [maxX,maxY]

# ----------------------------------------------------------------------------
def printGrid(grid) :
    for row in grid :
        r=''
        for col in row :
            if col > 0 :
                r+=str(col)
            else :
                r+='.'
        print(r)

# ----------------------------------------------------------------------------
def plotVentLineOntoGrid(grid,ventLine) :
    #ventLine is [[x1,y1],[x2,y2]]
    dx=ventLine[1][0] - ventLine[0][0]
    dy=ventLine[1][1] - ventLine[0][1]
    length=abs(dy)
    if abs(dx) >= abs(dy) : length=abs(dx)
    deltaX=dx/length
    deltaY=dy/length
    pX = ventLine[0][0]
    pY = ventLine[0][1]
    #print(f"plot from {ventLine[0]}]to {ventLine[1]}")
    #print(f"dx={dx} dy={dy}, length={length}, deltaX={deltaX}, deltaY={deltaY}, gridSize=[{len(grid)},{len(grid[0])}]")
    i=0
    while i <= length :
        grid[pY][pX] += 1
        pX = int(pX + deltaX)
        pY = int(pY + deltaY)
        i+=1
    return grid

# ----------------------------------------------------------------------------
def countIntersections(grid) :
    intersections=0
    for row in grid :
        for col in row :
            if col>1 :
                intersections += 1
    return intersections

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
if __name__ == "__main__" :
    vents = readFileToLineDefinitions(inputfile)
    gridSize=calcExtents(vents)
    grid = [[0 for i in range(gridSize[0]+1)] for j in range(gridSize[1]+1)]
    for vent in vents :
        #YES Anticipation IS GREAT NOW I HAVE DIAGONALS:
        grid = plotVentLineOntoGrid(grid,vent)

    #screendump gets silly with big grids
    #but would look lovely as a bitmap.....
    if(len(grid[0]) < 90) :
        printGrid(grid)
    print(f"Found {countIntersections(grid)} Intersection Points on grid")
