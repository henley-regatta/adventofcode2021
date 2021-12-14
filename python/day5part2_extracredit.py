#!/usr/bin/python3
# Python solution for AOC 2021 Day 5, Part 2
#
# Given a set of line-definition inputs, find the number of points of
# intersection of those lines.  Lines can now be diagonal
# (Blah blah something about geothermal vents)
#
# NOTE: Extended to generate a PNG of the grid after adding every vent.
# This can be assembled into a movie (webm) using:
#    ffmpeg -framerate 25 -f image2 -i day5part2_%d.png -c:v libvpx-vp9 -pix_fmt yuva420p movie/day5part2.webm

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
def writeGridAsPNG(grid,pngfile) :
    import png
    img = []
    height=len(grid)
    width=len(grid[0])
    for y in range(height) :
        for x in range(width) :
            p = grid[y][x]
            if p == 1 :
                img.extend([128,128,128,255])
            elif p > 1 :
                img.extend([128+(10*p),32,32,255])
            else :
                img.extend([0,0,0,0])
    print(f"writing image {pngfile}")
    with open(pngfile, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=True)
        w.write_array(f,img)

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
if __name__ == "__main__" :
    vents = readFileToLineDefinitions(inputfile)
    gridSize=calcExtents(vents)
    grid = [[0 for i in range(gridSize[0]+1)] for j in range(gridSize[1]+1)]
    for i in range(len(vents)) :
        grid = plotVentLineOntoGrid(grid,vents[i])
        png = "visualisation/day5part2_" + str(i) + ".png"
        writeGridAsPNG(grid,png)

    print(f"Found {countIntersections(grid)} Intersection Points on grid")
