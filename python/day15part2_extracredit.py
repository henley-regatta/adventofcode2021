#!/usr/bin/python3
# Python solution for AOC 2021 Day 15, Part 2
#
# Although the "standard" version does nicely enough at producing a PNG, this
# one extends it to produce A Series Of Still Images That Can Be Combined Together
# To Give The Illusion Of Movement.
# This is achieved using:
#   ffmpeg -framerate 25 -f image2 -i visualisation/day15part2_frame_%5d.png -c:v libvpx-vp9 -pix_fmt yuva420p visualisation/aoc2021_day15part2.webm
#
# (Works best if you make ~20 copies of the final frame to use as filler at the end -
#   for x in {1..9}; do cp day15part2_frame_00100.png day15part2_frame_0010${x}.png; cp day15part2_frame_00100.png day15part2_frame_0011${x}.png; done)
#inputfile = "data/day15test.txt"
inputfile = "data/day15part1.txt"

import sys
import png

#Globals All The Way
map=[]
maxX=0
maxY=0
growthFactor=5
#-----------------------------------------------------------------------
def loadMap(file) :
    map=[]
    with open(file,'r') as maplines :
        for l in maplines:
            c=l.strip()
            if len(c)>0 :
                map.append(c)
    return map
#-----------------------------------------------------------------------
def growMap(srcmap) :
    global map
    orgX=len(srcmap[0])
    orgY=len(srcmap)
    #Re-initialise the global map
    map = ["" for y in range(orgY*growthFactor)]
    print(f"map now has {len(map)} rows (source had {len(srcmap)})")
    for y in range(len(map)) :
        srcY=y%orgY
        dY=y//orgY
        line=""
        for x in range(orgX*growthFactor) :
            srcX=x%orgX
            dX=x//orgX
            srcP=int(srcmap[srcY][srcX])
            newP=srcP + dX + dY
            if newP>9 :
                newP=newP-9
            line += str(newP)
            #print(f"{line} {srcP}->(+{dX+dY})->{newP}")
        if len(line)!=orgY*growthFactor :
            print(f"Cock-up producing line {y} : {line}")
            exit()
        map[y]=line

#-----------------------------------------------------------------------
def cKey(x,y) :
    return x*1000 + y
    #return str(x) + "," + str(y)
#-----------------------------------------------------------------------
def fast_cKey(k) :
    return k[0]*1000 + k[1]
    #return str(x) + "," + str(y)
#-----------------------------------------------------------------------
def uKey(k) :
    if k==0 :
        return([0,0])
    elif k<1000 :
        return([0,k])
    else :
        y=k%1000
        x=(k-y)//1000
        return([x,y])

#-----------------------------------------------------------------------
def walkBackRoute(path) :
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    RED   = "\033[1;31m"
    YELLOW = '\033[33m'
    REVERSE = "\033[;7m"

    checkSum=0

    for y in range(maxY+1) :
        for x in range(maxX+1) :
            if cKey(x,y) in path :
                checkSum+=int(map[y][x])
                if maxY<101 :
                    print(REVERSE + YELLOW + map[y][x] + RESET,end="")
            elif maxY<101 :
                print(map[y][x],end="")
        if maxY<101 :
            print()
    checkSum -= int(map[0][0])
    print(f"Shown path checksum: {checkSum}")
    return checkSum

#-----------------------------------------------------------------------
def mapCostToColour(cost,scale,offset) :
    #We'd like a spectrum from green (low cost) to red. Thankfully this
    #is fairly easy:
    cScale=int(cost*scale)
    distFromMaxBoost=128 - abs(cScale-128)
    boost=distFromMaxBoost
    red=abs(int(cost*scale)+offset)
    green=abs(255-red)
    #print(f"cScale={cScale},red={red},green={green},boost={boost}")
    return [min(red + boost,255),min(green + boost,255),0]

#-----------------------------------------------------------------------
# NOTHING IN THE SPECIFICATION SAYS WE MUST ALWAYS MOVE DOWN AND RIGHT.
# BUT NOT SODDING DIAGONALS SO HELP ME LORD
def fast_getNeighbours(k) :
    neighbours=[]
    xneigh=[k[0]-1,k[0],k[0]+1]
    yneigh=[k[1]-1,k[1],k[1]+1]
    for y in yneigh :
        for x in xneigh :
            if (x==k[0] and y==k[1]) or (x!=k[0] and y!=k[1]):
                pass # don't do ourselves, or diagonals
            elif x>=0 and x<=maxX and y>=0 and y<=maxY :
                neighbours.append([x,y])
    return neighbours

#-----------------------------------------------------------------------
def bestRouteSoFar(connections,source,dest) :
    route=[dest]
    pos=dest
    while pos != source :
        pos = connections[pos]
        route.append(pos)
    route.append(source)
    return route
#-----------------------------------------------------------------------
def plotPath(route,costs,recents,pngfile) :
    img=[]
    #This is the map  for "unvisited" nodes, reflecting the underlying
    #(source) risk map.
    riskLUT={'9' : [0,25,51],
               '8' : [0,51,102],
               '7' : [0,76,153],
               '6' : [0,102,204],
               '5' : [0,128,255],
               '4' : [51,153,255],
               '3' : [102,178,255],
               '2' : [153,204,255],
               '1' : [204,229,255] }
    costLUT={}
    #For visited nodes, we need to know the range of costs possible, which
    #means finding the max cost:
    maxCost=0
    minCost=sys.maxsize
    for n in costs :
        c=costs[n]
        if c>maxCost :
            maxCost=c
        elif c<minCost :
            minCost=c
    if maxCost == minCost :
        cScale=255
    else :
        cScale=255/(maxCost-minCost)
    cOffset=minCost

    #Setup the final image dimensions and map-scaling to match it:
    desiredHeight=1000
    scale=desiredHeight//len(map)

    height=len(map) * scale
    width=len(map[0]) * scale
    for y in range(height) :
        for x in range(width) :
            sX=x//scale
            sY=y//scale
            k=cKey(sX,sY)
            if k in route :
                #Actual route is in Cyan
                img.extend([0,255,255])
            elif k in recents :
                img.extend([128,128,128])
            elif k in costs :
                v=costs[k]
                if v not in costLUT :
                    costLUT[v] = mapCostToColour(v, cScale, cOffset)
                img.extend(costLUT[v])

            else :
                img.extend(riskLUT[map[sY][sX]])

    #print(costLUT)
    print(f"writing image {pngfile}")
    with open(pngfile, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=False)
        w.write_array(f,img)
#-----------------------------------------------------------------------
# Algorithm freely cribbed from https://isaaccomputerscience.org/concepts/dsa_search_dijkstra
# Atttempt to speed up algo. Work in coordinates and lists not dicts wherever possible.
# Note that the "select-from-queue" function is the rate limiter; minimising the time
# it takes to search for the next cheapest node is the primary objective.
def fast_dijkstra() :

    #graph=map_to_graph()
    initial=fast_cKey([0,0])
    dest=fast_cKey([maxX,maxY])
    path={}
    adj_node={}
    queue = []

    for node in graph:
        path[node] = sys.maxsize
        adj_node[node] = None
        queue.append(node)

    costHash={0 : [initial]}
    path[initial]=0

    import time
    sCounter=0
    frameCounter=0
    sInit=time.perf_counter()
    initQ=len(queue)
    visitedThisIteration=[]
    plotCosts={}
    print(f"Starting search across {len(queue)} Nodes....")
    while queue:
        #Dijkstra says "evaluate the lowest-cost node in the queue"
        #I've changed this to use a hashed list ordered by cost, instead
        #of searching though each time. It's about 1 order of magnitude faster
        #than the simple approach.
        #Also, since we remove empty hashes on remove, we don't even need to
        #loop to lookup...
        #for min_val in sorted(costHash.keys()) :
        #    if len(costHash[min_val])>0 :
        #        cur=costHash[min_val][0]
        #        break
        chK=sorted(costHash.keys())
        min_val=chK[0]
        cur=costHash[min_val][0]
        visitedThisIteration.append(cur)
        queue.remove(cur)
        costHash[min_val].remove(cur)
        if len(costHash[min_val])==0 :
            del costHash[min_val]

        for i in graph[cur] :
            alternate = graph[cur][i] + path[cur]
            #Two equal paths are possible. >= leads to across-first.
            #Web page seems to prefer down-first so use this form:
            if path[i] > alternate :
                path[i] = alternate
                plotCosts[i] = alternate
                if alternate in costHash :
                    costHash[alternate].append(i)
                else :
                    costHash[alternate] = [i]
                adj_node[i] = cur

        #Abort after route?
        if cur == dest :
            print(f"Abort; found route with {len(queue)} remaining")
            break

        # OUR INTRA-LOOP UPDATE OPPORTUNITY:
        if sCounter%500==0 :
            tElapsed=time.perf_counter() - sInit
            procQ=initQ-len(queue)
            pctProc=procQ/initQ
            tTotal=tElapsed * 1/pctProc
            tRemain = tTotal - tElapsed
            print(f"Loop {sCounter}. Total: {procQ} Remaining: {len(queue)} {pctProc:.2%} {tRemain:.2f} seconds remaining")
            pathSoFar=bestRouteSoFar(adj_node,initial,cur)
            plotPath(pathSoFar,plotCosts,visitedThisIteration,"visualisation/day15part2_frame_"+format(frameCounter,"05d")+".png")
            frameCounter+=1
            visitedThisIteration=[]
        sCounter+=1

    trackBack=bestRouteSoFar(adj_node,fast_cKey([0,0]),fast_cKey([maxX,maxY]))
    trackCost=walkBackRoute(trackBack)

    plotPath(trackBack,path,[],"visualisation/day15part2_frame_" +format(frameCounter,"05d")+".png")
    print(f"Dijkstra cost to navigate: {trackCost}")
    return trackBack
#-----------------------------------------------------------------------
def map_to_graph() :
    graph={}
    for y in range(len(map)) :
        for x in range(len(map[0])) :
            tK={}
            neigh=fast_getNeighbours([x,y])
            for n in neigh :
                tK[fast_cKey(n)] = int(map[n[1]][n[0]])
            graph[cKey(x,y)]=tK
    return graph
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    map=loadMap(inputfile)
    growMap(map)
    maxX=len(map[0])-1
    maxY=len(map[1])-1
    print(f"map is of size {maxX+1} x {maxY+1}")
    graph=map_to_graph()
    route=fast_dijkstra()
