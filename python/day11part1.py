#!/usr/bin/python3
# Python solution for AOC 2021 Day 11, Part 1
#
# Work out octopus flashes in a grid according to Some Rules.
# EVERY ITERATION:
#   1) Increase val of each Octopus by 1
#   2) Each Octopus with l > 9 Flashes. 
#   3) Each Octopus adjacent to flash (with diagonals) increases by 1
#   4) Repeat from 2 with constraint that a given Octopus can only 
#      flash once per iteration; flashed octopii clamp to zero

#inputfile = "data/day11test.txt"
inputfile = "data/day11part1.txt"


#Today is a setup & iterate so it pays to pre-load
# ---------------------------------------------------------------
def readOctoGrid(file) :
    octogrid=[]
    with open(file,'r') as octofile :
        for l in octofile :
            row=[int(x) for x in l.strip()]
            octogrid.append(row)
    return octogrid

# ---------------------------------------------------------------
# visualisation tool
def printGrid(grid) :
    for y in range(len(grid)) :
        line=""
        for x in range(len(grid[0])) :
            if grid[y][x]>9 :
                line += "*"
            else :
                line += str(grid[y][x])
        print(line)
    print("-" * 20)
# ---------------------------------------------------------------
# simple increment (step 1)
def incrementGrid(grid) :
    outGrid=grid
    for y in range(len(grid)) :
        for x in range(len(grid[0])) :
            outGrid[y][x]=grid[y][x]+1
    return outGrid
# ---------------------------------------------------------------
# This is the initialiser of the (step 2) algorithm
# ASSUME: *every* octopus at l>9 flashes BEFORE the increment stage
#         (supported by the 1-in-9s scenario)
def findFlashing(grid) :
    nowFlashing=[]
    for y in range(len(grid)) :
        for x in range(len(grid[y])) :
            if grid[y][x]>9 :
                nowFlashing.append([x,y])
    return nowFlashing
# ---------------------------------------------------------------
def getNeighbourCoords(point,xMax,yMax) :
    ncoords=[]
    for y in [point[1]-1,point[1],point[1]+1] :
        if y>=0 and y <=yMax :
            for x in [point[0]-1,point[0],point[0]+1] :
                if x>=0 and x<=xMax and not(x==point[0] and y==point[1]) :
                    ncoords.append([x,y])
    return ncoords
# ---------------------------------------------------------------
# And this is the crux of the iterator. Handle each flashing Octopus'
# effects on it's neighbours
def processFlashQueue(grid,flashList) :
    newGrid=grid
    xMax=len(grid[0])-1
    yMax=len(grid)-1
    for f in flashList :
        x=f[0]
        y=f[1]
        newGrid[y][x]=0
        nList=getNeighbourCoords(f,xMax,yMax)
        for n in nList :
            if grid[n[1]][n[0]]>0 : #don't upgrade already-flashed octopii
                newGrid[n[1]][n[0]] += 1

    return newGrid

# ---------------------------------------------------------------
# Apply the rules above to the grid
def iterateGrid(grid) :
    cumFlashCount=0
    newGrid=incrementGrid(grid)
    #Not sure this is needed, but acts as a useful guard
    nowFlashing=findFlashing(newGrid)
    iterCount=0
    while len(nowFlashing)>0 :
        cumFlashCount += len(nowFlashing)
        newGrid=processFlashQueue(newGrid,nowFlashing)
        nowFlashing=findFlashing(newGrid)
        iterCount+=1

    print(f"Iterative grid update finished after {iterCount} cycles")
    return [newGrid,cumFlashCount]
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    grid = readOctoGrid(inputfile)
    printGrid(grid)
    #This needs an iterator for the required number of steps
    cumFlashCounter=0
    for n in range(1,101) :
        upd=iterateGrid(grid)
        grid=upd[0]
        cumFlashCounter+=upd[1]
        print(f"Step {n}; {cumFlashCounter} flashes so far")
        printGrid(grid)
