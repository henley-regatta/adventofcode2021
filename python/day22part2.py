#!/usr/bin/python3
# Python solution for AOC 2021 Day 22 Part 1
#
# Given input as a series of cubic volume descriptors and an "on" or "off"
# instruction, work out how many units are "on" at the end of the instructions.
#
# So the thing is we can't just do a bounding-cube and check stats, the
# grid would be many, many gigabytes (range is of order ~petabit). Instead
# what we'll have to do is calculate the range of cubes resulting from the
# commands - using "Union" (ON) and "Subtraction" (OFF) operations to generate
# a big set of non-intersecting cuboids and calculate the volume of each.
#
# Note that we don't actually need to do offsets or calculate bounding cubes
# for this; that's just leftovers from the first part.

# My solution wass crap in that, er, it doesn't work and it takes forever. Because
# at every opportunity I was adding both the compared blocks AND the intersection.
# It took a good read of some example solutions to work out why I was wrong.
# This code here is the closest I can get to understanding the actual algorithm
# required :
#  https://github.com/tbpaolini/Advent-of-Code/blob/master/2021/Day%2022/cubes2.py
# explained here: https://www.reddit.com/r/adventofcode/comments/rlxhmg/2021_day_22_solutions/hpv4sjl/
#
# And now what I'm left with is an algorithm that somehow (at step 7 on the part 1
# test data, possibly earlier/later on other data) manages to append cuboids that
# intersect with each other but not the cuboid being inserted. How, I do not yet
# know.
#  UPDATE: AH YES THE RARE OH-GOD-I-USED-THE-WRONG-COORDINATE. How I managed to
#          get away with the wrong bMin dimension in a bunch of test cases on
#          corner cuboids I will never know. Silly, very very silly.



#inputfile = "data/day22trivial.txt"
#inputfile = "data/day22test2.txt"
#inputfile = "data/day22test.txt"
inputfile = "data/day22part1.txt"

colourlist=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']

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
    intersection=[[0,0] for x in range(3)]
    for x in range(3) :
        dimInt = dimIntersection([c1[0][x],c1[1][x]],[c2[0][x],c2[1][x]])
        if dimInt[0] != None and dimInt[1] != None :
            intersection[x] = dimInt
        else :
            return None

    return toXYZCoords(intersection)
#-----------------------------------------------------------------------
# Some dimension hacks required to deal with integer arithmetic
# (a cube with same dimensions has volume 1, not 0. A cube with x-dimension 1,2 has length=2 not 1)
def cubicVolume(cube) :
    return (abs(cube[1][0]-cube[0][0])+1) * (abs(cube[1][1]-cube[0][1])+1) * (abs(cube[1][2]-cube[0][2])+1)
    ranges=[]
    for x in range(len(cube[0])) :
        r = cube[1][x] - cube[0][x] +1
        ranges.append(r)
    return ranges[0] * ranges[1] * ranges[2]

#-----------------------------------------------------------------------
def calcTotalVolOfCuboids(cuboids) :
    totalVol=0
    for c in cuboids :
        totalVol += cubicVolume(c)
    return totalVol

#-----------------------------------------------------------------------
#Having trouble visualising / working with dimension sets, convert to
#[x,y,z],[x,y,z] tuple instead
def toXYZCoords(cuboid) :
    try :
        return [[cuboid[0][0],cuboid[1][0],cuboid[2][0]],
                [cuboid[0][1],cuboid[1][1],cuboid[2][1]]]
    except IndexError :
        print(f"ERROR: Expected range of 6 values but got {cuboid}")
        exit(1)

#-----------------------------------------------------------------------
def toDimRangeCoords(xyzCoords) :
    return [[xyzCoords[0][0],xyzCoords[1][0]],[xyzCoords[0][1],xyzCoords[1][1]],[xyzCoords[0][2],xyzCoords[1][2]]]

#-----------------------------------------------------------------------
def isUniqueVert(possDup,vertList) :
    #Vertice is duplicate if the start and end points are the same
    #EVEN IF REVERSED.
    for cand in vertList :
        if ((cand[0]==possDup[0] and cand[1]==possDup[1]) or
           (cand[0]==possDup[1] and cand[1]==possDup[0])) :
           return False
    return True
#-----------------------------------------------------------------------
def getCuboidVertices(c) :
    #A cuboid consists of 12 vertices bounding the min,max points.
    dimRanges=toDimRangeCoords(c)
    #For drawing purposes extend end by 1
    for d in range(len(dimRanges)) :
        #if dimRanges[d][1] == dimRanges[d][0] :
        dimRanges[d][1] +=1
    #Extract out the points:
    points=[]
    for x in dimRanges[0] :
        for y in dimRanges[1] :
            for z in dimRanges[2] :
                points.append([x,y,z])
    #Vertices now join every point that shares 2 coordinates:
    #(note we avoid duplicates)
    vert=[]
    for v1 in points :
        for v2 in points :
            coplanar=0
            for d in range(len(v1)) :
                if v1[d] == v2[d] :
                    coplanar+=1
            if coplanar==2 :
                newVert=[v1,v2]
                if isUniqueVert(newVert,vert) :
                    vert.append([v1,v2])
    if len(vert)!=12 :
        print(f"How did you cock that up, expected 12 vertices got {len(vert)}")
        print('\n'.join([str(x) for x in sorted(vert)]))
        exit()
    return vert

#-----------------------------------------------------------------------
# calculate the range of a set of cuboids. Useful for setting boundaries
def getDimensionRange(list) :
    minP=[sys.maxsize,sys.maxsize,sys.maxsize]
    maxP=[-sys.maxsize,-sys.maxsize,-sys.maxsize]
    for c in list :
        for d in range(3) :
            if c[0][d] < minP[d] :
                minP[d] = c[0][d]
            if c[1][d] > maxP[d] :
                maxP[d] = c[1][d]
    return [minP,maxP]

#-----------------------------------------------------------------------
#This is a generic 3d plot of a bunch of cuboids :
def plotListOfCuboids(cuboidList) :
    #Cool Stuff. Most useful tutorial:
    # https://stackoverflow.com/questions/4622057/plotting-3d-polygons-in-python-matplotlib
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
    import matplotlib.pyplot as plt
    ax = Axes3D(plt.figure())
    #Get the limits
    r = getDimensionRange(cuboidList)
    lim=[]
    for d in range(3) :
        lim.append([r[0][d]-1,r[1][d]+1])  #grow the limits for display purposes.
    #Jiggery-pokery to make all the dimension the same length. Aids the display
    #perspective....
    maxR=0
    for d in lim:
        if d[1]-d[0] > maxR :
            maxR = d[1]-d[0]
    for d in lim :
        delta = maxR - (d[1]-d[0])
        d[1]+=delta
    ax.set(xlim=lim[0], ylim=lim[1], zlim=lim[2])

    #Now add the cuboids in the list to the plot
    cRange=len(colourlist)
    cIdx=0
    for c in cuboidList :
        ax.add_collection3d(Poly3DCollection(getCuboidVertices(c), color=colourlist[cIdx], edgecolor=colourlist[cIdx], alpha=0.5))
        cIdx = (cIdx+1)%cRange
    plt.show()

#-----------------------------------------------------------------------
#This function is specific to plotting the "remainder" list of cuboids
#when "big" is (wholly) intersected by "smol"
def plotCuboidRemaindersIn3d(big,smol,cuboidList) :
    #Cool Stuff. Most useful tutorial:
    # https://stackoverflow.com/questions/4622057/plotting-3d-polygons-in-python-matplotlib
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
    import matplotlib.pyplot as plt
    ax = Axes3D(plt.figure())
    lim=[[big[0][0],big[1][0]+1],
         [big[0][1],big[1][1]+1],
         [big[0][2],big[1][2]+1]]
    ax.set(xlim=lim[0], ylim=lim[1], zlim=lim[2])
    ax.add_collection3d(Line3DCollection(getCuboidVertices(big), color="blue"))
    ax.add_collection3d(Poly3DCollection(getCuboidVertices(smol), color="red", edgecolor="red", alpha=1))
    cRange=len(colourlist)
    cIdx=0
    for c in cuboidList :
        ax.add_collection3d(Poly3DCollection(getCuboidVertices(c), color=colourlist[cIdx], edgecolor=colourlist[cIdx], alpha=0.2))
        cIdx = (cIdx+1)%cRange
    plt.show()

#-----------------------------------------------------------------------
# when computing intersections and unions it's helpful to know if
# once cube is entirely contained by another...
def isCompletelyContainedBy(big,smol) :
    smolWithinBig = True
    for d in range(3) :
        if smol[0][d] < big[0][d] or smol[1][d] > big[1][d] :
            smolWithinBig = False
    return smolWithinBig

#-----------------------------------------------------------------------
# It Turns Out it would be good to know if two cuboids are coplanar
# along any of their 6 faces. So work it out, once:
def getCoplanarity(c1,c2) :
    return {
        #top coplanar if c2 top Z == c1 top Z
        'top' : c2[1][2] == c1[1][2],
        #front coplanar if c2 bottom y == c1 bottom y
        'front' : c2[0][1] == c1[0][1],
        #right coplanar if c2 top X == c1 top X
        'right' : c2[1][0] == c1[1][0],
        #rear coplanar if c2 top Y == c1 top Y
        'rear'  : c2[1][1] == c1[1][1],
        #left coplanar if c2 bottom X == c1 bottom X
        'left'  : c2[0][0] == c1[0][0],
        #bottom coplanar if c2 bottom Z == c1 bottom Z
        'bottom' : c2[0][2] == c1[0][2]
    }


#-------------------------------------------------------------------------
#Sub-part a: Get the (up to) 8 cuboids making up the corner-adjacent
#remainder: Because this is integer arithmetic, we offset "smol" by 1
def getCornerCuboids(big,smol,cp) :
    bMin=big[0]
    bMax=big[1]
    #To account for int arithmetic, we offset smol by one:
    sMin=[smol[0][0]-1,smol[0][1]-1,smol[0][2]-1]
    sMax=[smol[1][0]+1,smol[1][1]+1,smol[1][2]+1]
    #print(f"cp   = {cp}")
    #print(f"big  = {big}")
    #print(f"smol = {smol}")
    #print(f"[sMin,sMax] = [{sMin},{sMax}]")

    #We can ALWAYS generate all 8 corner cuboids:
    candCuboids=[]
    if not cp['front'] :
        if not cp['bottom'] :
            if not cp['left'] :
                #print("front-bottom-left")
                candCuboids.append([bMin,sMin])  #"Bottom left front"
            if not cp['right'] :
                #print("front-bottom-right")
                candCuboids.append([[sMax[0],bMin[1],bMin[2]], [bMax[0],sMin[1],sMin[2]]]) #"bottom right front"
        if not cp['top'] :
            if not cp['left'] :
                #print("front-top-left")
                candCuboids.append([[bMin[0],bMin[1],sMax[2]], [sMin[0],sMin[1],bMax[2]]]) #"top left front"
            if not cp['right'] :
                #print("front-top-right")
                candCuboids.append([[sMax[0],bMin[1],sMax[2]], [bMax[0],sMin[1],bMax[2]]]) #"top right front"
    if not cp['rear'] :
        if not cp['bottom'] :
            if not cp['left'] :
                #print("rear-bottom-left")
                candCuboids.append([[bMin[0],sMax[1],bMin[2]], [sMin[0],bMax[1],sMin[2]]]) #"bottom left rear"
            if not cp['right'] :
                #print("rear-bottom-right")
                candCuboids.append([[sMax[0],sMax[1],bMin[2]], [bMax[0],bMax[1],sMin[2]]]) #"bottom right rear"
        if not cp['top'] :
            if not cp['left'] :
                #print("rear-top-left")
                candCuboids.append([[bMin[0],sMax[1],sMax[2]], [sMin[0],bMax[1],bMax[2]]]) #"top left rear"
            if not cp['right'] :
                #print("rear-top-right")
                candCuboids.append([[sMax[0],sMax[1],sMax[2]], [bMax[0],bMax[1],bMax[2]]]) #"top right rear"

    #print(f"generated corner cuboids: {[str(x) for x in candCuboids]}")
    return candCuboids

#-----------------------------------------------------------------------
#When smol is entirely enclosed within big there are up to 6 "face" cuboids
#between smol and big boundaries.
def getFaceCuboids(big,smol,cp) :
    bMin,bMax = big
    sMin,sMax = smol

    #Define the  face cuboids:
    faceCuboids=[]
    if not cp['top'] :
        faceCuboids.append([[sMin[0],sMin[1],sMax[2]+1],[sMax[0],sMax[1],bMax[2]]])
    if not cp['front'] :
        faceCuboids.append([[sMin[0],bMin[1],sMin[2]],[sMax[0],sMin[1]-1,sMax[2]]])
    if not cp['right'] :
        faceCuboids.append([[sMax[0]+1,sMin[1],sMin[2]],[bMax[0],sMax[1],sMax[2]]])
    if not cp['rear'] :
        faceCuboids.append([[sMin[0],sMax[1]+1,sMin[2]],[sMax[0],bMax[1],sMax[2]]])
    if not cp['left'] :
        faceCuboids.append([[bMin[0],sMin[1],sMin[2]],[sMin[0]-1,sMax[1],sMax[2]]])
    if not cp['bottom'] :
        faceCuboids.append([[sMin[0],sMin[1],bMin[2]],[sMax[0],sMax[1],sMin[2]-1]])

    return faceCuboids


#-----------------------------------------------------------------------
#When smol is entirely enclosed within big there are up to 12 "vertex" cuboids
#between smol and big boundaries.
def getVertexCuboids(big,smol,cp) :
    bMin=big[0]
    bMax=big[1]
    sMin=smol[0]
    sMax=smol[1]

    vertexCuboids=[]
    #front 4:
    if not cp['front'] :
        if not cp['top'] :
            vertexCuboids.append([[sMin[0],bMin[1],sMax[2]+1],[sMax[0],sMin[1]-1,bMax[2]]])
        if not cp['right'] :
            vertexCuboids.append([[sMax[0]+1,bMin[1],sMin[2]],[bMax[0],sMin[1]-1,sMax[2]]])
        if not cp['bottom'] :
            vertexCuboids.append([[sMin[0],bMin[1],bMin[2]],[sMax[0],sMin[1]-1,sMin[2]-1]])
        if not cp['left'] :
            vertexCuboids.append([[bMin[0],bMin[1],sMin[2]],[sMin[0]-1,sMin[1]-1,sMax[2]]])
    #right 2:
    if not cp['right'] :
        if not cp['bottom'] :
            vertexCuboids.append([[sMax[0]+1,sMin[1],bMin[2]],[bMax[0],sMax[1],sMin[2]-1]])
        if not cp['top'] :
            vertexCuboids.append([[sMax[0]+1,sMin[1],sMax[2]+1],[bMax[0],sMax[1],bMax[2]]])
    #rear 4:
    if not cp['rear'] :
        if not cp['top'] :
            vertexCuboids.append([[sMin[0],sMax[1]+1,sMax[2]+1],[sMax[0],bMax[1],bMax[2]]])
        if not cp['right'] :
            vertexCuboids.append([[sMax[0]+1,sMax[1]+1,sMin[2]],[bMax[0],bMax[1],sMax[2]]])
        if not cp['bottom'] :
            vertexCuboids.append([[sMin[0],sMax[1]+1,bMin[2]],[sMax[0],bMax[1],sMin[2]-1]])
        if not cp['left'] :
            vertexCuboids.append([[bMin[0],sMax[1]+1,sMin[2]],[sMin[0]-1,bMax[1],sMax[2]]])
    #left 2:
    if not cp['left'] :
        if not cp['bottom'] :
            vertexCuboids.append([[bMin[0],sMin[1],bMin[2]],[sMin[0]-1,sMax[1],sMin[2]-1]])
        if not cp['top'] :
            vertexCuboids.append([[bMin[0],sMin[1],sMax[2]+1],[sMin[0]-1,sMax[1],bMax[2]]])


    return vertexCuboids

#-----------------------------------------------------------------------
#We need to do "subtraction" to work out the sub-cubes resulting from
#the removal of a smaller cube from a bigger cube
#NB: We've already done an intersection so we KNOW "smol" is within
#   "bigs" boundaries
def cuboidRemainder(big,smol) :
    #print("-"*80)
    #print(f"big:  {big}")
    #print(f"smol: {smol}")

    #(I confess to using a hint online)
    #Since we know smol is entirely enclosed within big, we can work out the
    #set of remainder cuboids as:
    #  a) Up to 8 cuboids from big's corners to smol's corners. ("corner cuboids")
    #  b) Up to 6 cuboids aligned with smol's faces to the big boundary ("face cuboids")
    #  c) Up to 12 cuboids aligned with smol's vertices to the big boundary ("vertex cuboids")
    cp = getCoplanarity(big,smol)
    remainderCuboids=[]

    #Append the corner cuboids:
    remainderCuboids.extend(getCornerCuboids(big,smol,cp))

    #Append the face cuboids
    remainderCuboids.extend(getFaceCuboids(big,smol,cp))

    #Append the vertex cuboids
    remainderCuboids.extend(getVertexCuboids(big,smol,cp))

    #fmtCub='\n'.join([str(c) for c in remainderCuboids])
    #print(f"remainder cuboids:\n{fmtCub}")

    return remainderCuboids

#-----------------------------------------------------------------------
# When something's up with your algorithm, you need to check you haven't
# got intersecting cuboids in your list:
def getIntersectingCuboids(cuboidList) :
    noIntersectingBlocks=True
    tList=[]
    for a in range(len(cuboidList)) :
        for b in range(len(cuboidList)) :
            if a == b :
                continue
            else :
                i = cubicIntersection(cuboidList[a],cuboidList[b])
                if i != None :
                    noIntersectingBlocks=False
                    tList.append(cuboidList[a])
                    tList.append(cuboidList[b])

    #By design this'll find every block twice a-b b-a, so de-dup the list before
    #returning:
    intBlocks=[]
    if not noIntersectingBlocks:
        for b in tList :
            if b not in intBlocks :
                intBlocks.append(b)

    return intBlocks


#-----------------------------------------------------------------------
def testSuite() :

    """
    big=[[-49, -3, -24], [1, 46, 28]]
    smol=[[-27, -3, -21], [1, 26, 28]]
    rem=cuboidRemainder(big,smol)
    print(f"{big} by {smol} gives:")
    print('\n'.join([str(x) for x in rem]))
    plotCuboidRemaindersIn3d(big,smol,cuboidRemainder(big,smol))
    return False
    """

    c = toXYZCoords([[-5,5],[5,15],[0,10]])
    expected=[[-5,5,0],[5,15,10]]
    if c != expected :
        print(f"failed toXYZCoords(), expected {expected} got {c}")
        return False

    cVolList= [
        {'c' : [[0,0,0],[0,0,0]],
        'a' : 1*1*1},
        {'c' : [[0,0,0],[1,1,1]],
        'a' : 2*2*2},
        {'c' : [[0,0,0],[2,2,2]],
        'a' : 3*3*3},
        {'c' : [[10,10,10],[10,10,10]],
        'a' : 1*1*1},
        {'c' : [[10,10,10],[11,11,11]],
        'a' : 2*2*2},
        {'c' : [[0,0,0],[1,1,0]],
         'a' : 2*2*1},
        {'c' : [[0, 0, 0], [0, 0, 1]],
         'a' : 1*1*2},
        {'c' : [[-5,5,0],[5,15,10]],
         'a' : 11*11*11},
        {'c' : [[3, 1, 3], [3, 3, 3]],
         'a' : 1*3*1},
        {'c' : [[3, 1, 1], [3, 3, 3]],
         'a' : 1*3*3},
        {'c' : [[-27, -28, -21], [23, 26, 29]],
         'a' : 143055},
        {'c' : [[23,22,29], [73,76,79]],
         'a' : 143055},
        ]
    for cube in cVolList :
        v = cubicVolume(cube['c'])
        if v != cube['a'] :
            print(f"failed cubicVolume({cube['c']}) expected {cube['a']} got {v}")
            plotListOfCuboids([cube['c']])
            return False

    tList = [
        {'c1' : [[1,1,1],[3,3,3]],
        'c2'  : [[2,2,2],[2,2,2]],
        'i'   : [[2,2,2],[2,2,2]]},
        {'c1' : [[2,2,2],[2,2,2]],
         'c2' : [[1,1,1],[3,3,3]],
         'i'  : [[2,2,2],[2,2,2]]},
        {'c1' : toXYZCoords([[-5,5],[5,15],[0,10]]),
         'c2' : [[0,0,0],[10,20,30]],
         'i'  : [[0,5,0],[5,15,10]]},
        {'c1' : [[1,1,1],[3,3,3]],
         'c2' : [[0,0,0],[1000,1000,1000]],
         'i'  : [[1,1,1],[3,3,3]]},
        {'c1' : [[1,1,1],[3,3,3]],
         'c2' : [[1,1,1],[3,3,3]],
         'i'  : [[1,1,1],[3,3,3]]},
        #I KNOW this is failing, I am fucked if I can see how:
        {'c1' : [[-49, -3, -24], [1, 46, 28]],
         'c2' : [[-27, -28, -21], [23, 26, 29]],
         'i'  : [[-27,-3,-21], [1,26,28]]},
    ]
    for t in tList :
        i = cubicIntersection(t['c1'],t['c2'])
        r = cubicIntersection(t['c2'],t['c1'])
        if i != r :
            print(f"Failed reflectivity; c1={t['c1']} c2={t['c2']}, i={i} but r={r}")
            return False
        if i != t['i'] :
            print(f"cubicIntersection({t['c1']},{t['c2']}) failed, expected {t['i']} got {i}")
            plotListOfCuboids([t['c1'],t['c2'],i])
            return False


    tList=[
        { 'b' : [[1,1,1],[3,3,3]],
          's' : [[2,2,2],[2,2,2]],
          'c' : 26,
          'v' : (3*3*3)-(1*1*1)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[1,1,1],[9,9,9]],
          'c' : 26,
          'v' : (11*11*11)-(9*9*9)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[5,5,5],[5,5,5]],
          'c' : 26,
          'v' : (11*11*11)-(1*1*1)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[1,1,1],[9,10,9]],
          'c' : 4+4+1+3+3+2,
          'v' : (11*11*11) - (9*10*9)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[3,3,0],[7,7,10]],
          'c' : 8,
          'v' : (11*11*11)-(5*5*11)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[0,0,0],[9,9,9]],
          'c' : 1+3+3,
          'v' : (11*11*11)-(10*10*10)},
        { 'b' : [[0,0,0],[10,10,10]],
          's' : [[1,0,0],[9,9,9]],
          'c' : 2+4+5,
          'v' : (11*11*11)-(9*10*10)},
        { 'b' : [[1,1,1],[3,3,3]],
          's' : [[3,3,3],[3,3,3]],
          'c' : 1+3+3,
          'v' : (3*3*3)-(1*1*1) },
        { 'b' : [[1,1,1],[100,100,100]],
          's' : [[2,2,2],[4,4,4]],
          'c' : 8+6+12,
          'v' : (100*100*100)-(3*3*3) },
        { 'b' : [[-49, -3, -24], [1, 46, 28]],
          's' : [[-27, -3, -21], [1, 26, 28]],
          'c' : 7,
          'v' : (51*50*53)-(29*30*50) }


    ]
    for t in tList :
        r=cuboidRemainder(t['b'],t['s'])
        cV=calcTotalVolOfCuboids(r)
        if len(r) != t['c'] or cV != t['v']:
            print(f"cuboidRemainder({t['b'],t['s']}) FAIL. Count expected {t['c']} got {len(r)}, Vol expected {t['v']} got {cV}")
            for c in r :
                print(f"{c} with volume {cubicVolume(c)}")
                plotCuboidRemaindersIn3d(t['b'],t['s'],[c])
            return False

    return True

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    if not testSuite() :
        print("GET YOUR MATHS RIGHT FIRST")
        exit()
    else :
        print("Pre-flight checks passed; testSuite() ran OK")
    reactorInstructions=readInstructionsFromFile(inputfile)
    print(f"Read {len(reactorInstructions)} instructions from {inputfile}")
    """
    reactorInstructions=[
        [ "on", [1,10],[1,10],[1,10] ],
        [ "on", [1,10],[0,0],[1,10] ],
        [ "on", [0,0],[1,10],[1,10] ],
        [ "on", [1,10],[1,10],[11,11] ],
        [ "on", [1,10],[1,10],[0,0] ],
        [ "on", [11,11],[1,10],[1,10] ],
        [ "on", [1,10],[11,11],[1,10] ],
        [ "on", [0,11],[0,11],[0,11] ],
    ]
    """
    blocksOn=[]
    for i in range(len(reactorInstructions)):
        op=reactorInstructions[i][0]
        insCuboid=toXYZCoords(reactorInstructions[i][1:])
        print(f"{i+1}/{len(reactorInstructions)} Turning {op} block {insCuboid}",end="...")
        postInsBlocksOn=[]
        for c in blocksOn :
            intersection=cubicIntersection(c,insCuboid)
            if intersection==None :
                postInsBlocksOn.append(c) #IF no intersection we append the old block and move on.
                #print(f"\tNo intersection with {c}")
            elif intersection != c :
                #Current block is partly but not wholly included in the new block,
                #so we only want to "save" the parts of the original that don't overlap:
                postInsBlocksOn.extend(cuboidRemainder(c,intersection))
                #print(f"\tPARTIAL INTERSECTION with {c} at {intersection}")
            #Blank operation here for ELSE because what we've now found is that
            #the intersection is ALL of the test block, which means whatever we
            #do with this instruction it affects ALL of the test block, so that's
            #now superfluous

        #And now postInsBlocksOn contains ONLY a list of blocks GUARANTEED NOT TO INTERSECT WITH
        #insCuboid :
        for v in postInsBlocksOn :
            i = cubicIntersection(v,insCuboid)
            if i != None :
                print(f"Error - should be no intersection between {v} and {insCuboid} but got {i}")
                exit(1)

        #So now all we have to do is act on the instruction; if it's an "on" we
        #append the insCuboid; if it's not we don't.
        if op == "on" :
            postInsBlocksOn.append(insCuboid)

        """
        if len(getIntersectingCuboids(postInsBlocksOn))>0 :
            print("POSTPHASE No point continuing, the answer will be bogus anyway")
            exit()
        """
        print(f"Now {len(postInsBlocksOn)} blocks lit; {calcTotalVolOfCuboids(postInsBlocksOn)} nodes")
        blocksOn = postInsBlocksOn

    print(f"After processing {len(reactorInstructions)} commands there are {len(blocksOn)} cuboids")
    totalVol = calcTotalVolOfCuboids(blocksOn)
    print(f"At the end, {totalVol} nodes are lit")

    test1ExpectedAnswer=590784 + ((abs(-39298 - -54112)+1) * abs(-49293 - -85059)+1 * abs(7877 - -27449)+1)
    test1ExpectedAnswer+=((abs(23432-967)+1) * (abs(81175-45373)+1) * (abs(53682-27513)+1))

    test2ExpectedAnswer=2758514936282235
    if inputfile == "data/day22test.txt" and totalVol != test1ExpectedAnswer :
        print(f"Expected:   {test1ExpectedAnswer}")
        print(f"Calculated: {totalVol}")
        print(f"Wrong By:   {abs(test1ExpectedAnswer-totalVol)}")
    elif inputfile == "data/day22test2.txt" and totalVol != test2ExpectedAnswer :
        print(f"Expected:   {test2ExpectedAnswer}")
        print(f"Calculated: {totalVol}")
        print(f"Wrong By:   {abs(test2ExpectedAnswer-totalVol)}")
