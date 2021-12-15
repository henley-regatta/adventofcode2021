#!/usr/bin/python3
# Python solution for AOC 2021 Day 15, Part 2
# Given an input "Risk Map" compute the lowest-risk path from top left (0,0)
# to bottom right (maxX,maxY).
# Moves may not be made diagonally.
# Route risk is computed as the sum of the risk values entered on the path.
##
# Note that prior to use the map must be "grown" by 5 x in every dimension with
# risk scores incrementing by 1 (mod10) each time.
#
# The previous approach - calculating cost-to-finish for each point back from
# the end to the start - appears to have fluked the answer to Part 1.
# Irritatingly it also produces the "right" answer for the example data in Part 2
# but too big a value (apparently) for the live data set.
#
# NOTE PER THE HINTS ON REDDIT: Despite the sample data AND the part 1 solution
# not requiring "backtracking", there's nothing in the specification that
# precludes movement "left" or "up". If there was, my simpler part1 solution
# of back-calculating would be perfect.
#
# As a result, we need to implement the Dijkstra algorithm to find the cheapest
# cost from start to finish...
# Have tried to optimise it (a bit) but it's still slow using dicts and lists.
# This *is* a justification for using the "HiPower" profile on my machine to
# cut down calc costs.
#
# Note that the "Dijkstra Cost" shown is an analogue of the actual cost; the
# correct cost according to the specification is the "checksum" cost shown
# after display
#
# As a bonus, automatically does visualisation to a PNG

#inputfile = "data/day15test.txt"
inputfile = "data/day15part1.txt"

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
def plotPath(path,pngfile) :
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    RED   = "\033[1;31m"
    YELLOW = '\033[33m'
    REVERSE = "\033[;7m"
    #import sys
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

    import png
    img=[]
    colourLUT={'9' : [0,25,51],
               '8' : [0,51,102],
               '7' : [0,76,153],
               '6' : [0,102,204],
               '5' : [0,128,255],
               '4' : [51,153,255],
               '3' : [102,178,255],
               '2' : [153,204,255],
               '1' : [204,229,255] }
    scale=2
    height=len(map) * scale
    width=len(map[0]) * scale
    for y in range(height) :
        for x in range(width) :
            sX=x//scale
            sY=y//scale
            if cKey(sX,sY) in path :
                img.extend([255,255,0])
            else :
                img.extend(colourLUT[map[sY][sX]])

    print(f"writing image {pngfile}")
    with open(pngfile, 'wb') as f:
        w = png.Writer(width, height, greyscale=False, alpha=False)
        w.write_array(f,img)
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
# Algorithm freely cribbed from https://isaaccomputerscience.org/concepts/dsa_search_dijkstra
# Atttempt to speed up algo. Work in coordinates and lists not dicts wherever possible.
def fast_dijkstra() :
    import sys
    graph=map_to_graph()
    initial=fast_cKey([0,0])
    dest=fast_cKey([maxX,maxY])
    path={}
    adj_node={}
    queue = []

    for node in graph:
        path[node] = sys.maxsize
        adj_node[node] = None
        queue.append(node)

    path[initial]=0

    import time
    sCounter=0
    sInit=time.perf_counter()
    initQ=len(queue)
    while queue:
        key_min=queue[0]
        min_val = path[key_min]
        for n in range(1,len(queue)) :
            if path[queue[n]] <= min_val :
                key_min = queue[n]
                min_val = path[key_min]
        cur = key_min
        queue.remove(cur)

        for i in graph[cur] :
            alternate = graph[cur][i] + path[cur]
            #Two equal paths are possible. >= leads to across-first.
            #Web page seems to prefer down-first so use this form:
            if path[i] > alternate :
                path[i] = alternate
                adj_node[i] = cur

        #Abort after route?
        if cur == dest :
            print(f"Abort; found route with {len(queue)} remaining")
            break

        if sCounter%100==0 :
            tElapsed=time.perf_counter() - sInit
            procQ=initQ-len(queue)
            pctProc=procQ/initQ
            tRemain=tElapsed * 1/pctProc
            print(f"Loop {sCounter}. Visited {procQ} Remaining {len(queue)} {pctProc:.2%} {tRemain:.2f} seconds remaining")
        sCounter+=1


    dest=fast_cKey([maxX,maxY])
    trackBack=[dest]
    trackCost=0
    pos=dest
    while pos != initial :
        pos = adj_node[pos]
        trackBack.append(pos)
    trackBack.append(pos)

    dfile="visualisation/day15part2_lastplottedroute.out"
    df = open(dfile,'a')
    df.write("[" + ','.join(str(p) for p in trackBack) + "]\n")
    df.close()
    print(f"Route dumped to end of file {dfile}")
    plotPath(trackBack,"visualisation/day15part2_fast_dijkstra.png")
    print(f"Dijkstra cost to navigate: {trackCost}")
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
    dijkstraCost=fast_dijkstra()
    #dijkstraCost=dijkstra()
    print(dijkstraCost)
