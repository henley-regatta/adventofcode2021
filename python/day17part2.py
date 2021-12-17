#!/usr/bin/python3
# Python solution for AOC 2021 Day 17, Part 2
#
# It's Track-A-Probe-Velocity day here on the AOC submarine.
# PROBLEM: Given start and target zones, how many distinct trajectories pass
#          through the target zone?
#
# Today the input data - test and live - is so simple it's not even
# worth file access:
import sys
# It *is* computationally expensive though, so multi-threading ought to help.
# (running under WSL2 with memory=16GB and processors=4)
# (With my Ryzen 3700X, setting numThreads = 2 x num Processors appears optimal)
#               ProcessPoolExecutor         ThreadPoolExecutor
# 1 thread    = 54 seconds                  20.2 seconds
# 4 threads   = 51.3 seconds                15.4 seconds
# 8 threads   = 51.2 seconds                15.2 seconds
# 16 threads  = 54.1 seconds                15.4 seconds
# 32 threads  = 56 seconds                  15.7 seconds
# 100 threads = 75 seconds                  16.1 seconds
# Running "single threaded" (numThreads=1, but with all the scaffolding in place)
# gives ~54 seconds for the test result.
import concurrent.futures
numThreads=12

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
def plotProbeForward(traj) :
    #We start from the Sub at t-zero:
    #print(f"plotting at launch vel={traj} to: {targetBoundary}")
    pos=[0,0]
    t=0
    dX=traj[0]
    dY=traj[1]
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
            #print(f"Initial Velocity {traj} intersects target zone at {pos} after {t} steps. Max Height was {maxY}")
            return traj

    #If we got here we missed the target zone...
    #print(f"Initial Velocity {traj} misses the target zone after {t} steps.")
    return None
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
#For part 2 we don't need the maximum heights, we just need the initial
#velocities that worked and a count of same.
def solveByBruteForce(targetLocation, maxVel) :
    updateBoundaries(targetLocation)
    #BRUUUTE FORCE!
    successfulTrajectories=[]
    failedTrajectories=0
    testTrajectories=[]
    #WE CAN BE SMART ABOUT SETTING LIMITS ON TRAJECTORIES:
    #1) No point testing below y = targetBoundary['d'] as we skip below that
    #   in under a step.
    minY=-1 * maxVel
    if maxVel > abs(targetBoundary['d']) :
        minY = targetBoundary['d']-1
    #2) No point checking above x = targetBoundary['r'] as we'd skip past it
    #   on the first step
    maxX=maxVel
    if maxX > targetBoundary['r'] :
        maxX = targetBoundary['r']+1
    for y in range(minY,maxVel) :
        for x in range(maxX) :
            testTrajectories.append([x,y])
    print(f"Testing against {len(testTrajectories)} potential trajectories with velocity limit {maxVel}")
    #with concurrent.futures.ProcessPoolExecutor(max_workers=numThreads) as executor:
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        future_to_trajResult = {executor.submit(plotProbeForward,vel) : vel for vel in testTrajectories}
        for future in concurrent.futures.as_completed(future_to_trajResult) :
            s = future_to_trajResult[future]
            try:
                res=future.result()
                if res is not None :
                    successfulTrajectories.append(res)
                else :
                    failedTrajectories+=1
                if (len(successfulTrajectories)+failedTrajectories)%10000 == 0 :
                    print(f"Completed {len(successfulTrajectories)+failedTrajectories} tests; {len(successfulTrajectories)} matches found so far")
            except Exception as exc:
                print(f"Something went wrong with threading: {exc}")
                exit()
    return successfulTrajectories

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #Test Suite:
    updateBoundaries(testLoc)
    if (plotProbeForward([7,2]) is not None and
        plotProbeForward([6,3]) is not None and
        plotProbeForward([9,0]) is not None and
        plotProbeForward([17,-4]) is None):
        print("Test Suite Completed Successfully")
    else :
        print("Test Suite Failed")
        exit()

    bestAnswer=0
    velLimit=500
    deltaBest=sys.maxsize
    while deltaBest>0 :
        resultSet=solveByBruteForce(liveLoc,velLimit)
        print(f"limit {velLimit} finds {len(resultSet)} trajectories")
        if len(resultSet)> bestAnswer :
            deltaBest = len(resultSet) - bestAnswer
            bestAnswer=len(resultSet)
        else:
            deltaBest=0
        velLimit+=100

    print(f"After checking against {velLimit} velocity steps, we found {bestAnswer} successful trajectories")
    #print(resultSet)
