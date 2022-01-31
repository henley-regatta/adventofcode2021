#!/usr/bin/python3
# Python solution for AOC 2021 Day 22 Part 1
#
# Given input as a series of cubic volume descriptors and an "on" or "off"
# instruction, work out how many units are "on" at the end of the instructions.
#
# Part one restriction says "only consider the central -50..50 volume".
# (This is an obvious trap for part 2.)
#
# Half of the functions here are entirely superfluous for part 1 and written
# in anticipation of a part2 shocker.

#inputfile = "data/day22trivial.txt"
#inputfile = "data/day22test.txt"
inputfile = "data/day22part1.txt"

import sys
#-----------------------------------------------------------------------
def readInstructionsFromFile(filename) :
    instructions=[]
    #------------------------------------------------
    def grokDimension(dimSpec) :
        (dim,range)=dimSpec.split('=')
        (d1,d2)=range.split('..')
        id1=int(d1)
        id2=int(d2)
        if id1<id2 :
            return [dim,id1,id2]
        else :
            return [dim,id2,id1]
    #------------------------------------------------

    with open(filename,'r') as insfile :
        for ins in insfile :
            (cmd,dims)=ins.strip().split(' ')
            instruction=[cmd,[],[],[]]
            xyz=dims.split(',')
            dimensions={}
            for d in dims.split(',') :
                dim=grokDimension(d)
                if dim[0] == 'x' :
                    instruction[1]=dim[1:]
                elif dim[0] == 'y' :
                    instruction[2]=dim[1:]
                elif dim[0] == 'z' :
                    instruction[3]=dim[1:]
                else :
                    print(f"Invalid dimension {dim[0]} returned in {dim}")
                    exit()
            instructions.append(instruction)
    return instructions

#-----------------------------------------------------------------------
#silly little thing to return min/max on dimension
def cmdDim(d1,d2) :
    bDim=d1
    if d2[0] < d1[0] :
        bDim[0] = d2[0]
    if d2[1] > d1[1] :
        bDim[1] = d2[1]
    return bDim

#-----------------------------------------------------------------------
#return the cube that's the intersection of two passed cubes (if any)
def cubicIntersection(c1,c2) :
    intersection=[]
    #-------------------------------
    #intersection of a given dimension
    def dimIntersection(d1,d2) :
        intersection=[None,None]
        if d2[0]>d1[1] or d1[0] > d2[1] :
            return intersection #no intersection found
        else :
            intersection = [d2[0],d1[1]]
            if d1[0] > d2[0] :
                intersection[0] = d1[0]
            if d2[1] < d1[1] :
                intersection[1] = d2[1]
        return intersection
    #-------------------------------
    intersection=[[0,0] for x in range(len(c1))]
    for x in range(len(c1)) :
        dimInt = dimIntersection(c1[x],c2[x])
        if dimInt[0] != None and dimInt[1] != None :
            intersection[x] = dimIntersection(c1[x],c2[x])
        else :
            return None
    return intersection
#-----------------------------------------------------------------------
# real simple now
def cubicVolume(cube) :
    ranges=[]
    for x in range(len(cube)) :
        r = cube[x][1] - cube[x][0]
        if r==0 : # intger arith hack
            r=1
        ranges.append(r)
    return ranges[0] * ranges[1] * ranges[2]

#-----------------------------------------------------------------------
# just to make the indexing easier, really:
def offsetCubeBy(offset,cube) :
    offCube=cube
    for d in range(len(cube)) :
        for p in range(len(cube[d])) :
            offCube[d][p]+=offset[d-1]
    return offCube
#-----------------------------------------------------------------------
def countOnNodes(cube) :
    sum=0
    for x in range(len(cube)) :
        for y in range(len(cube[0])) :
            for z in range(len(cube[0][0])) :
                sum+=cube[x][y][z]
    return sum
#-----------------------------------------------------------------------
def flipNodeState(newState,region,sourceGrid) :
    v=1
    if newState == "off" :
        v=0
    destGrid=sourceGrid
    for x in range(region[0][0],region[0][1]+1) :
        for y in range(region[1][0],region[1][1]+1) :
            for z in range(region[2][0],region[2][1]+1) :
                destGrid[x][y][z] = v
    print()
    return destGrid
#-----------------------------------------------------------------------
def getBoundingCube(instructionSet) :
    boundingCube=[[sys.maxsize,-1*sys.maxsize] for d in range(3)]
    for ins in instructionSet :
        dims=ins[1:]
        for x in range(len(dims)) :
            boundingCube[x] = cmdDim(boundingCube[x],dims[x])
    return boundingCube

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    reactorInstructions=readInstructionsFromFile(inputfile)
    print(f"Read {len(reactorInstructions)} instructions from {inputfile}")

    boundingCube=getBoundingCube(reactorInstructions)
    print(f"Actual Bounding cube {boundingCube} has total volume {cubicVolume(boundingCube)}")
    offsets=[-1*boundingCube[0][0],-1*boundingCube[1][0],-1*boundingCube[2][0]]

    #PART ONE constraint - -50 to +50 in each dimension, which offsets to 0-100
    #with a 50 offset.
    offsets=[50,50,50]
    boundingCube=[[0,100],[0,100],[0,100]]
    reactorGrid=[[[0 for x in range(boundingCube[0][1]+1)] for y in range(boundingCube[1][1]+1)] for x in range(boundingCube[2][1]+1)]
    print(f"Constraining commands to grid of volume {cubicVolume(boundingCube)}")

    for i in range(len(reactorInstructions)) :
        ins=reactorInstructions[i]
        affCube=offsetCubeBy(offsets,ins[1:])
        tCube = cubicIntersection(affCube,boundingCube)
        if tCube is not None :
            op=ins[0]
            reactorGrid = flipNodeState(op,affCube,reactorGrid)
            print(f"Step {i+1} turning {op}  {cubicVolume(affCube)} points in {affCube}; {countOnNodes(reactorGrid)} total nodes lit")
        else :
            print(f"Step {i+1}'s boundary {tCube} is outside the bounding cube")

    print(f"At the end, {countOnNodes(reactorGrid)} nodes are lit")
