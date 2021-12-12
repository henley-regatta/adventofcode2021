#!/usr/bin/python3
# Python solution for AOC 2021 Day 11, Part 2
#
# Work out octopus flashes in a grid according to Some Rules.
# EVERY ITERATION:
#   1) Increase val of each Octopus by 1
#   2) Each Octopus with l > 9 Flashes.
#   3) Each Octopus adjacent to flash (with diagonals) increases by 1
#   4) Repeat from 2 with constraint that a given Octopus can only
#      flash once per iteration; flashed octopii clamp to zero
#
# Challenge is now to find the first day on which they all flash
# this is a simple extension of the part 1 answer waiting for convergence
# which we can detect by a day when the updatedFlash counter is equal
# to the size of the grid (x * y)
#
# This is the "extra credit" version for visualisaton, as with Day 5 this
# looks best as an animation. Convert each stage's grid into a PNG, then
# assemble using:
#    ffmpeg -framerate 25 -f image2 -i day11part2_%d.png -c:v libvpx-vp9 -pix_fmt yuva420p movie/day11part2.webm


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
    return [newGrid,cumFlashCount]
# ----------------------------------------------------------------------------
def writeGridAsPNG(grid,pngfile) :
    import png
    img = []
    colourLUT={0 : [0,0,0],
               1 : [0,76,153],
               2 : [0,0,255],
               3 : [0,102,204],
               4 : [0,153,0],
               5 : [0,128,255],
               6 : [204,0,0],
               7 : [255,0,255],
               8 : [255,204,153],
               9 : [255,255,204] }
    scale = 20
    height=len(grid) * scale
    width=len(grid[0]) * scale
    for y in range(height) :
        for x in range(width) :
            img.extend(colourLUT[grid[y//scale][x//scale]])
    print(f"writing image {pngfile}")
    with open(pngfile, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=False)
        w.write_array(f,img)
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    grid = readOctoGrid(inputfile)
    printGrid(grid)
    gridSize=len(grid) * len(grid[0])
    haveSyncFlashed=False
    step=0
    synchroFlashStep=-1
    maxFrames=500
    while step < maxFrames :
        upd=iterateGrid(grid)
        grid=upd[0]
        step+=1
        if upd[1]==gridSize :
            haveSyncFlashed=True
            synchroFlashStep=step
        print(f"Step {step} had {upd[1]} of {gridSize} flashes")
        writeGridAsPNG(grid,"visualisation/day11part2_" + str(step) + ".png")

    print(f"First Synchronised Flash occurred after {synchroFlashStep} Iterations")
