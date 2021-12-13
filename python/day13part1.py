#!/usr/bin/python3
# Python solution for AOC 2021 Day 13, Part 1
#
# Given input in the form of a series of "dots" on a grid,
# and a list of fold instructions for the grid,
# determine the resulting pattern
# (well part 1 says "count the dots visible after 1 fold")
#inputfile = "data/day13test.txt"
inputfile = "data/day13part1.txt"

# ---------------------------------------------------------------
def loadGridAndFoldInstructions(file) :
    gridPoints=[]
    foldInstructions=[]
    finishedGrid=False
    with open(file,'r') as indata :
        for l in indata :
            if not finishedGrid :
                xy=l.strip().split(',')
                if len(xy)==2 :
                    gridPoints.append([int(xy[0]),int(xy[1])])
                else :
                    finishedGrid=True
            else :
                fIns=l.strip().split('=')
                dir=fIns[0][-1]
                foldInstructions.append([dir,int(fIns[1])])

    return [gridPoints,foldInstructions]
# ---------------------------------------------------------------
def buildInitialGrid(gridPoints) :
    #Work out the dimensions of the grid first:
    maxX=0
    maxY=0
    for p in gridPoints :
        if p[0]>maxX :
            maxX = p[0]
        if p[1]>maxY :
            maxY = p[1]
    print(f"grid has dimensions {maxX} x {maxY}")
    grid=[[False for x in range(maxX+1)] for y in range(maxY+1)]
    #Second pass through the points to set each x,y:
    for p in gridPoints :
        grid[p[1]][p[0]]=True

    return grid
# ---------------------------------------------------------------
def printGrid(grid) :
    for row in grid :
        line=''
        for point in row :
            if point :
                line+="#"
            else :
                line+='.'
        print(line)
# ---------------------------------------------------------------
def countGridPointsSet(grid) :
    count=0
    for row in grid :
        for point in row :
            if point :
                count+=1
    return count

# ---------------------------------------------------------------
# a "foldUp" transformation at {line} means the output grid is
# {line} rows long, and all points on lines from the input grid >{line}
# are moved up to {line-n} where n is the number of lines GREATER than {line}
# HANDY SIMPLIFICATION: the "fold line" will always be empty.
def foldUp(grid,line) :
    #TODO this guard condition prevents "short folds"
    if line < (len(grid)//2) :
        print(f"SHORT FOLD detected for y={line}")
        exit()
    outGrid = [[False for x in range(len(grid[0])-1)] for y in range(line)]
    print(f"grid after foldUp {line} will be {len(outGrid[0])} x {len(outGrid)}")
    #Start by copying the grid UP TO {line}
    for y in range(line) :
        outGrid[y] = grid[y]

    #Now "reflect" lines after {line} back onto the grid
    for y in range(line+1,len(grid)) :
        rY=line - y
        for x in range(len(grid[rY])) :
            if outGrid[rY][x]==False :
                outGrid[rY][x]=grid[y][x]

    return outGrid

# ---------------------------------------------------------------
# a "foldLeft" transformation at {column} means the output grid becomes
# {column} columns wide, and all points from the input grid after {column}
# are reflected back.
# AGAIN: We're told that folds won't take place on an occupied column
def foldLeft(grid,column) :
    #TODO this guard condition prevents "short folds"
    if column < (len(grid[0])//2) :
        print(f"SHORT FOLD detected for x={column}")

    outGrid=[]
    #Since we're line oriented we do this over and over....
    for line in grid :
        outLine=line[0:column:]
        for x in range(column+1,len(line)) :
            rX = column - x
            if outLine[rX] == False :
                outLine[rX] = line[x]
        outGrid.append(outLine)

    print(f"grid after foldLeft {column} is {len(outGrid[0])} x {len(outGrid)}")
    return outGrid

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    d=loadGridAndFoldInstructions(inputfile)
    grid=buildInitialGrid(d[0])
    print(f"There are {countGridPointsSet(grid)} points visible")
    for fold in d[1] :
        if fold[0] == 'y' :
            grid = foldUp(grid,fold[1])
        else :
            grid = foldLeft(grid,fold[1])
        printGrid(grid)
        print(f"There are {countGridPointsSet(grid)} points visible")
        break
