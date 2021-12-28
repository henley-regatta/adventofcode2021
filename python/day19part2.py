#!/usr/bin/python3
# Python solution for AOC 2021 Day 19 Part 2
#
# Given a list of Scanners and the Probes that each can see, count the
# number of distinct probes in the water.
#
# Each scanner reports a set of probes at max ordinal distance 1000,1000,1000
# from it's position.  BUT each scanner may have one of 24 orientations.
# Probes are reported as distances from each scanner in it's chosen coordinate
# system.
#
# Take all the probes out of the equation, we're asked for the greatest
# "manhattan distance" between two scanners. This is shockingly close to the
# pseudo distance we've previously been using....

#infile="data/day19test.txt"
infile="data/day19part1.txt"

#-----------------------------------------------------------------------
def readDataFile(file) :
    dataList={}
    with open(file,'r') as idata:
        cScanner=-1
        inScanner=False
        cScannerData=[]
        for l in idata:
            l=l.strip()
            if len(l) > 0 :
                if not inScanner :
                    p=l.split()
                    if p[0] != '---' or p[1] != 'scanner' :
                        print(f"Error parsing expected scanner line got {l}")
                    else :
                        inScanner=True
                        cScanner=int(p[2])
                else :
                    p=l.split(',')
                    if len(p)!=3 :
                        print(f"Error expected 3 coordinates, got {l}")
                    else :
                        cScannerData.append([int(x) for x in p])
            else :
                #blank delimiter line
                if inScanner :
                    dataList[cScanner] = cScannerData
                    cScannerData = []
                    inScanner=False

        #final line handling
        if inScanner :
            dataList[cScanner] = cScannerData

    return dataList

#-----------------------------------------------------------------------
# NB: It's the caller's responsibility to make sure this is a consistent
#     set of probes (i.e. from one scanner or a consolidated list.)
# (also, strictly, this doesn't find distance but the square of it. Close Enough.)
def findProbeDistanceList(probelist) :
    probeDistances=[[] for y in  range(len(probelist))]
    for a in range(len(probelist)) :
        for b in range(a+1,len(probelist)) :
            if a==b :
                continue
            d=distanceAnalogue(probelist[a],probelist[b])
            probeDistances[a].append([b,d])
    return probeDistances
#-----------------------------------------------------------------------
#Likkle function to calc the square of distance between 2 points
def distanceAnalogue(a,b) :
    xSquared = (a[0]-b[0])**2
    ySquared = (a[1]-b[1])**2
    zSquared = (a[2]-b[2])**2
    return xSquared + ySquared + zSquared
#-----------------------------------------------------------------------
# find concordances in probe distances between 2 scanner's set of results
def findMatchingDistances(list1,list2) :
    #This is *quite* the combinatorial explosion.....
    matches=[]
    for a in range(len(list1)) :
        for b in list1[a] :
            for x in range(len(list2)) :
                for y in list2[x] :
                    if b[1] == y[1] :
                        matches.append([[a,b[0]],[x,y[0]]])
    return matches
#-----------------------------------------------------------------------
def probeHash(coords,scanner) :
    return ':'.join([str(scanner),str(coords[0]),str(coords[1]),str(coords[2])])
#-----------------------------------------------------------------------
#this is the meaningful stuff we'll need to calculate the rotations
def distanceVector(a,b) :
    xDiff = (a[0]-b[0])
    yDiff = (a[1]-b[1])
    zDiff = (a[2]-b[2])
    return [xDiff,yDiff,zDiff]
#-----------------------------------------------------------------------
#We can't determine actual probe concordances nor the translation/rotations
#with the distance analogues. We need actual distance vectors to compare.
#(our first step just reduced the noise-level)
#Note that if we matched [a,b] we need to include [b,a] too, because we don't
#yet know which way around the matches go.
def getActualDistances(dPairs,sProbeList,dProbeList) :
    distances=[{},{}] #snigger looks like boobs
    for pair in dPairs :
        sPair = pair[0]
        dPair = pair[1]
        sDistAB = distanceVector(sProbeList[sPair[0]],sProbeList[sPair[1]])
        sDistBA = distanceVector(sProbeList[sPair[1]],sProbeList[sPair[0]])
        dDistAB = distanceVector(dProbeList[dPair[0]],dProbeList[dPair[1]])
        dDistBA = distanceVector(dProbeList[dPair[1]],dProbeList[dPair[0]])
        if sPair[0] not in distances[0] :
            distances[0][sPair[0]] = {sPair[1] : sDistAB}
        else :
            distances[0][sPair[0]][sPair[1]] = sDistAB
        if sPair[1] not in distances[0]:
            distances[0][sPair[1]] = {sPair[0] : sDistBA}
        else :
            distances[0][sPair[1]][sPair[0]] = sDistBA

        if dPair[0] not in distances[1] :
            distances[1][dPair[0]] = {dPair[1] : dDistAB}
        else :
            distances[1][dPair[0]][dPair[1]] = dDistAB
        if dPair[1] not in distances[1]:
            distances[1][dPair[1]] = {dPair[0] : dDistBA}
        else :
            distances[1][dPair[1]][dPair[0]] = dDistBA
    return distances
#-----------------------------------------------------------------------
def printDist(actualDistances) :
    for s in range(len(actualDistances)) :
        for f in sorted(actualDistances[s].keys()) :
            for t,dist in actualDistances[s][f].items() :
                print(f"{s}: {f}->{t} = {dist}")
#-----------------------------------------------------------------------
#Rotate around X axis by 90 degrees
def rotateXAxis(vec) :
    return [vec[0],-1*vec[2],vec[1]]
#-----------------------------------------------------------------------
#Rotate around Y axis by 90 degrees
def rotateYAxis(vec) :
    return [vec[2],vec[1],-1*vec[0]]
#-----------------------------------------------------------------------
#Rotate around Z axis by 90 degrees
def rotateZAxis(vec) :
    return [-1*vec[1],vec[0],vec[2]]
#-----------------------------------------------------------------------
# The sequence of 24 rotations that iterate over a coordinate transform
# (6 faces, 4 orientations per face)
def iterateOrientations(vec) :
    outvec = [vec]
    # "Rotate around the X axis"
    x1=vec
    for i in range(3) :
        x1 = rotateXAxis(x1)
        outvec.append(x1)
    #"Rotate the cube right"
    r1=rotateYAxis(vec)
    outvec.append(r1)
    #Iterate over 4 directions (z-axis)
    r1z=r1
    for i in range(3) :
        r1z=rotateZAxis(r1z)
        outvec.append(r1z)
    #"Rotate the cube right"
    r2=rotateYAxis(r1)
    outvec.append(r2)
    #iterate over 4 directions (x-axis)
    r2x=r2
    for i in range(3) :
        r2x=rotateXAxis(r2x)
        outvec.append(r2x)
    #"Rotate the cube right"
    r3=rotateYAxis(r2)
    outvec.append(r3)
    r3z=r3
    for i in range(3) :
        r3z=rotateZAxis(r3z)
        outvec.append(r3z)
    #The next rotation returns to normal so skip it, instead "rotate about Z"
    u1=rotateZAxis(vec)
    outvec.append(u1)
    #Now rotate around y 4 times:
    u1y=u1
    for i in range(3) :
        u1y=rotateYAxis(u1y)
        outvec.append(u1y)
    #A single rotation here around Z is equivalent to ry2 so do 2
    u2=rotateZAxis(u1)
    u3=rotateZAxis(u2)
    outvec.append(u3)
    #final rotation sequence around y
    u3y=u3
    for i in range(3) :
        u3y=rotateYAxis(u3y)
        outvec.append(u3y)

    return outvec
#-----------------------------------------------------------------------
def notVecMultiplication(sVec,xform)  :
    return [sVec[0]*xform[0],sVec[1]*xform[1],sVec[2]*xform[2]]
#-----------------------------------------------------------------------
def findDefinitiveProbeMatches(pMatches,matchDistances) :
    definitiveMatches=[]
    for pair in pMatches :
        sPair = pair[0]
        sDistance = matchDistances[0][sPair[0]][sPair[1]]
        sRevDistance = matchDistances[0][sPair[1]][sPair[0]]
        dPair = pair[1]
        dDistance = matchDistances[1][dPair[0]][dPair[1]]
        dRevDistance = matchDistances[1][dPair[1]][dPair[0]]
        dTransforms=iterateOrientations(dDistance)
        dRevTransforms = iterateOrientations(dRevDistance)
        for m in range(len(dTransforms)) :
            if dTransforms[m] == sDistance :
                #We have a match with the "m" index
                definitiveMatches.append([sPair,dPair,m])
            elif dRevTransforms[m] == sDistance :
                definitiveMatches.append([sPair,dPair,m])
    return definitiveMatches
#-----------------------------------------------------------------------
def reduceAssociations(matches) :
    assocs={}
    #We'll arbitrarily treat the "left side" as master, "right side" matched-against
    for m in matches :
        ma=m[0][0]
        mb=m[0][1]
        if ma not in assocs :
            #This is a list of candidates, really
            assocs[ma]=[[m[1][0],m[2]],[m[1][1],m[2]]]
        else :
            #filter OUT right-sides not in list
            submatch=[]
            for a in assocs[ma]:
                if a[0] in m[1] :
                    submatch.append(a)
            if len(submatch)==0 :
                #no matches left, remove key
                del assocs[ma]
            else :
                assocs[ma]=submatch
        #REPEAT FOR THE OTHER SIDE:
        if mb not in assocs :
            assocs[mb]=[[m[1][0],m[2]],[m[1][1],m[2]]]
        else :
            submatch=[]
            for b in assocs[mb]:
                if b[0] in m[1] :
                    submatch.append(b)
            if len(submatch)==0 :
                del assocs[mb]
            else :
                assocs[mb]=submatch

    splicedAssociations={}
    for a in assocs.keys() :
        if len(assocs[a])==1 :
            splicedAssociations[a]=assocs[a][0]
        else :
            print(f"Unable to reduce A-side {a} to a single match: {assocs[a]}")
    return splicedAssociations
#-----------------------------------------------------------------------
#This is really inefficient. I'm a muppet.
def transformProbeList(probeList,transformIdx) :
    transformed=[]
    for p in probeList :
        xformed=iterateOrientations(p)
        transformed.append(xformed[transformIdx])
    return transformed
#-----------------------------------------------------------------------
#To complete the exam question, I need to be able to translate ALL
#scanner lists back to the zero'th. The least inefficient way to achieve this
#is to move from the "furthest from zero" (in terms of hops) scanner list back
#towards the zero scanner, transforming and coalescing on the way. To achieve
#this we first need to work out, er, what the hops are:
def getChainBackToTarget(scanners,target,offsets) :
    #Initialise a structure tracking "links back to zero"
    targetChains={}

    incompleteChains=list(scanners)
    incompleteChains.remove(target)

    makingProgress=True
    while len(incompleteChains)>0  and makingProgress :
        makingProgress=False
        toexamine = incompleteChains
        for s in toexamine :
            if s in offsets.keys() :
                targs = offsets[s].keys()
                if target in targs :  #this is simple, it's a 1-hopper back:
                    targetChains[s] = [target]
                    incompleteChains.remove(s)
                    print(f"Direct link {s} to {target}, incompletes now: {incompleteChains}")
                    makingProgress=True
                else :
                    for t in targs :
                        if t in targetChains.keys() : #OK this is a multi-hopper back:
                            targetChains[s] = [t]
                            targetChains[s].extend(targetChains[t])
                            if s in incompleteChains :
                                incompleteChains.remove(s)
                            print(f"Indirect link {s} to {target} via {t}, route {targetChains[s]}, incompletes now: {incompleteChains}")
                            makingProgress=True

    if len(incompleteChains)>0 :
        print(f"Did not resolve targets for {incompleteChains}")
        print(targetChains)
        exit()

    return targetChains

#-----------------------------------------------------------------------
def transformAndMerge(xform,fromList,toList) :
    outputList=toList
    for cand in transformProbeList(fromList,xform[0]) :
        xlateCand = [ cand[0] + xform[1][0], cand[1] + xform[1][1], cand[2] + xform[1][2]]
        if xlateCand not in outputList :
            outputList.append(xlateCand)
    return outputList
#-----------------------------------------------------------------------
def manhattanDistance(pos1,pos2) :
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1]) + abs(pos1[2]-pos2[2])
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    dataList=readDataFile(infile)
    print(f"Input Data Report.\nNumber of Scanners = {len(dataList)}")
    probeDistances=[]
    sRecords=0
    for s in sorted(dataList.keys()) :
        sRecords += len(dataList[s])
        probeDistances.append(findProbeDistanceList(dataList[s]))

    print(f"Input Data List number of probes:    {sRecords}")
    print("")

    scannerOffsets={}
    #Irritatingly, we need to calculate this both ways now....
    for s1 in range(len(dataList)) :
        #for s2 in range(s1+1,len(dataList)) :
        for s2 in range(len(dataList)) :
            if s1 == s2 :
                continue
            print(f"comparing scanner {s1} to {s2}....",end="")
            matchDist=findMatchingDistances(probeDistances[s1],probeDistances[s2])
            print(f"{len(matchDist)} scalar matches",end=",")
            #TODO there should be a discriminator here - no point proceeding if
            #there are insufficient potential matches.
            if len(matchDist)<12 :
                print("insufficient potential matches to proceed; iterating")
                continue
            distanceMatches=findDefinitiveProbeMatches(matchDist,getActualDistances(matchDist,dataList[s1],dataList[s2]))
            print(f"{len(distanceMatches)} actual distance matches",end=",")
            probeEquivalences=reduceAssociations(distanceMatches)
            print(f" {len(probeEquivalences)} probe matches",end=",")
            if len(probeEquivalences)<12 :
                print("Insufficient actual probe matches to proceed; iterating")
                continue
            xForm=-1
            for f,t in probeEquivalences.items() :
                if xForm==-1 :
                    xForm=t[1]
                elif xForm != t[1] :
                    print(f"OH NO different transformations: {f}->{t[0]}: {xForm}, {t[1]}")
            print(f"Using transformation {xForm}",end=",")
            dProbeTransforms=transformProbeList(dataList[s2],xForm)
            matchList=[]
            for f,t in probeEquivalences.items() :
                matchList.append([[f,dataList[s1][f]],[t[0],dataList[s2][t[0]],dProbeTransforms[t[0]]]])
            offset=None
            for m in matchList :
                thisOffset = distanceVector(m[0][1],m[1][2])
                if offset == None :
                    offset = thisOffset
                elif offset != thisOffset :
                    print(f"OH NO: Different offsets for {m}, was expecting {offset} calculated {thisOffset}")
            print(f"Scanner offset = {offset}")
            if s1 not in scannerOffsets :
                scannerOffsets[s1] = {s2 : [xForm,offset]}
            else :
                scannerOffsets[s1][s2] = [xForm,offset]

    #We're not really bothered by the actual probes from here on, but we do still
    #need the list of transforms in order to place the scanners on a coherent
    #coordinate plane (i.e. scanner 0's)

    #Translate the list of scanners back to zero
    zeroChains = getChainBackToTarget(dataList.keys(),0,scannerOffsets)
    #sort this list by longest-chain first
    chainLengths={}
    for k in zeroChains :
        l = len(zeroChains[k])
        if l in chainLengths :
            chainLengths[l].append(k)
        else :
            chainLengths[l] = [k]
    processScannerList = []
    for l in sorted(list(chainLengths.keys()),reverse=True) :
        processScannerList.extend(chainLengths[l])

    scannerPositions = { 0: [0,0,0] }
    for fromScanner in processScannerList :
        hopList = zeroChains[fromScanner]
        toScanner=hopList[0]
        del hopList[0]
        #First hop doesn't involve any coordinate translation
        scannerPos=scannerOffsets[toScanner][fromScanner][1]
        print(f"From the perspective of scanner {toScanner}, scanner {fromScanner} is at: {scannerPos}")
        lastScanner=toScanner
        for toScanner in hopList :
            print(f"From the perspective of scanner {toScanner}, scanner {fromScanner} is at:",end=" ")
            transform = scannerOffsets[toScanner][lastScanner]
            scannerPos=transformAndMerge(transform,[scannerPos],[])[0]
            print(scannerPos)
            lastScanner=toScanner
        scannerPositions[fromScanner] = scannerPos

    maxDistance=0
    maxPair=[0,0]
    for f in scannerPositions :
        for t in scannerPositions :
            if f == t :
                continue
            print(f"{f}:{scannerPositions[f]}<->{t}:{scannerPositions[t]} = ",end="")
            mDistance = manhattanDistance(scannerPositions[f],scannerPositions[t])
            print(mDistance)
            if mDistance > maxDistance :
                maxDistance = mDistance
                maxPair = [f,t]

    print(f"The maximum Manhattan distance found (PART TWO ANSWER) was {maxDistance} between scanners {maxPair}")
