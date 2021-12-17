#!/usr/bin/python3
# Python solution for AOC 2021 Day 17, Part 1
#
# It's Track-A-Probe-Velocity day here on the AOC submarine.
# PROBLEM: Given start and target zones, what is the MAXIMUM +VE HEIGHT
#          the probe can be fired at and still pass through the target zone.
#
# Today the input data - test and live - is so simple it's not even
# worth file access:
import sys

# TEST:
testLoc={ 'x' : [20,30], 'y' : [-10,-5]}
# LIVE:
liveLoc={ 'x' : [117,164], 'y' : [-140,-89]}

# Motion Constants for steps:
Xdot=-1  # vX moves towards zero - if it starts negative it adds 1, if it starts positive it subtracts 1
Ydot=-1  # vY always increases downwards

#This is, effectively, a restatement of the opening conditions:
targetBoundary={}

#-----------------------------------------------------------------------
def updateBoundaries(targetLoc) :
    global targetBoundary
    targetBoundary = {
        'u' : max(targetLoc['y']),
        'd' : min(targetLoc['y']),
        'l' : min(targetLoc['x']),
        'r' : max(targetLoc['x'])
    }

#The "right answer" is to work out which location in the target zone permits
#the maximum +y impulse in order to hit. Which is done by back-plotting a route
#until it intersects (0,0). Wrong answer look forwards:
#-----------------------------------------------------------------------
def plotProbeForward(Xvel,Yvel) :
    #We start from the Sub at t-zero:
    #print(f"plotting at launch vel=({Xvel},{Yvel}) to: {targetBoundary}")
    pos=[0,0]
    t=0
    dX=Xvel
    dY=Yvel
    maxY=0 #We need to track the max "height" we reached too
    #REPEAT until we fall through the floor.....
    while pos[1]>=targetBoundary['d'] :
        #Note the passage of time:
        t+=1
        #MOVE:
        pos[0] += dX
        pos[1] += dY
        #TRACK MAX HEIGHT REACHED
        if pos[1]>=maxY :
            maxY=pos[1]
        #ADJUST VELOCITY:
        if dX==0 :
            # X Tends to Zero and stays there:
            dX=0
        elif abs(dX) != dX :
            #I can't see any conditions under which dX would be negative, but part2
            #has ways of surprising us, so....
            dX -= Xdot
        else :
            dX += Xdot
        #Vertical velocity is so much easier to calculate:
        dY += Ydot

        #print(f"{t} : {pos} vel=({dX},{dY})")
        if inTargetZone(pos) :
            #print(f"Initial Velocity ({Xvel},{Yvel}) intersects target zone at {pos} after {t} steps. Max Height was {maxY}")
            return maxY

    #If we got here we missed the target zone...
    #print(f"Initial Velocity ({Xvel},{Yvel}) misses the target zone after {t} steps.")
    return -1
#-----------------------------------------------------------------------
# boolean test - does current position describe one within the target zone or
# not?
def inTargetZone(pos) :
    x=pos[0]
    y=pos[1]
    if ((x>=targetBoundary['l'] and x<=targetBoundary['r']) and
        (y<=targetBoundary['u'] and y>=targetBoundary['d'])) :
        return True
    return False

#-----------------------------------------------------------------------
def solveByBruteForce(targetLocation, maxVel) :
    updateBoundaries(targetLocation)
    #BRUUUTE FORCE!
    maxHeights={}
    for y in range(maxVel) :
        for x in range(maxVel) :
            hit=plotProbeForward(x,y)
            if hit>=0 :
                if hit in maxHeights :
                    maxHeights[hit].append([x,y])
                else :
                    maxHeights[hit]=[[x,y]]
    peakHeight=max(maxHeights.keys())
    return peakHeight, maxHeights[peakHeight]

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #Test Suite:
    updateBoundaries(testLoc)
    if (plotProbeForward(7,2)>=0 and
        plotProbeForward(6,3)>=0 and
        plotProbeForward(9,0)>=0 and
        plotProbeForward(17,-4)<0 ):
        print("Test Suite Completed Successfully")
    else :
        print("Test Suite Failed")
        exit()

    bestAnswer=0
    velLimit=400
    deltaBest=sys.maxsize
    while deltaBest>0 :
        maxHeight,traj=solveByBruteForce(liveLoc,velLimit)
        if maxHeight > bestAnswer :
            bestAnswer=maxHeight
        deltaBest = maxHeight - bestAnswer
        velLimit+=100

    print(f"Best height found was {bestAnswer} from trajectories {traj} (tested to {velLimit} velocity)")
