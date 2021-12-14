#!/usr/bin/python3
# Python solution for AOC 2021 Day 8, Part 2
# Given an input of messed-up "segment inputs" and a 4-digit output value,
# work out which signal a-g displays which element of a 7-segment display

# OK Now we get to the decoding bit.....

#inputfile = "data/day8test.txt"
inputfile = "data/day8part1.txt"

#I need a map of the elements used by a 7-segment display
segmap={ 0 : {'count' : 6, 'elements' : ['a','b','c','e','f','g']},
         1 : {'count' : 2, 'elements' : ['c','f']},
         2 : {'count' : 5, 'elements' : ['a','c','d','e','g']},
         3 : {'count' : 5, 'elements' : ['a','c','d','f','g']},
         4 : {'count' : 4, 'elements' : ['b','c','d','f']},
         5 : {'count' : 5, 'elements' : ['a','b','d','f','g']},
         6 : {'count' : 6, 'elements' : ['a','b','d','e','f','g']},
         7 : {'count' : 3, 'elements' : ['a','c','f']},
         8 : {'count' : 7, 'elements' : ['a','b','c','d','e','f','g']},
         9 : {'count' : 6, 'elements' : ['a','b','c','d','f','g']},
       }

#
#NB: SOME of these aren't used but I'm scared to delete anything because I've
#    forgotten which....

#From this we derive a reverse by number of segments:
simpMap={2 : 1, 3 : 7, 4 : 4, 7 : 8}
fiveCands=[2,3,5]
sixCands=[0,6,9]
candDigitBySegmentsLit={2 : [1],
                        3 : [7],
                        4 : [4],
                        5 : [2,3,5],
                        6 : [0,6,9],
                        7 : [8]}
#And a "segment sharing" list shows which multivariant numbers share with which
#simple numbers: (digit X shares segments with [a,b,c])
uniqueShares= {1 : {4: ['c','f'], 7: ['c','f'], 8: ['c','f']},
               4 : {1: ['c','f'], 7: ['c','f'], 8: ['b','c','d','f'] },
               7 : {1: ['c','f'], 4: ['c','f'], 8: ['a','c','f']},
               8 : {1: ['c','f'], 4: ['b','c','d','f'], 7: ['a','c','f']}}

fiveshares={2 : [],
            3 : [7],
            5 : []}
sixshares={0 : [1,7],
           6 : [],
           9 : [1,7]}

# --------------------------------------------------------------------------
def parseSegSequence(seq) :
    outSeq=[]
    for c in seq :
        outSeq.append(c)
    return {'count' : len(outSeq), 'elements' : sorted(outSeq)}

# --------------------------------------------------------------------------
def parseInputFile(file) :
    #Input is of format [<word>]x10 | [<word]x4
    #with the part before the delimiter the "segment" input and the bit
    #after the "output digits"
    sequences=[]
    with open(file,'r') as data:
        for sequence in data :
            d=sequence.strip().split('|')
            if len(d)>1 :
                inList=[parseSegSequence(x) for x in d[0].split()]
                outList=[''.join(parseSegSequence(y)['elements']) for y in d[1].split()]
                sequences.append([inList,outList])
    return sequences

# --------------------------------------------------------------------------
def filterSimple(inputMap,sig) :
    try :
        d = simpMap[sig['count']]
    except KeyError :
        print(f"Invalid digit {sig} passed to filterSimple")
        exit()
    if d == 8 : return inputMap # no filtering possible, contains all elements

    #PRIMARY FILTERING - Filter back by the digits available
    candSegs=segmap[d]['elements']
    #print(f"Filtering for digit {d}, dest segments: {candSegs}, src segments: {sig['elements']}")
    filteredSegs=inputMap
    for c in candSegs :
        srcSeg=inputMap[c]
        #print(f"mapping dest segment {c}, started as {srcSeg}",end=",")
        filt=[]
        for v in srcSeg :
            if v in sig['elements'] :
                filt.append(v)
        if len(filt)==0 :
            print(f"Oops. Filtered out all values for segment {c}")
            exit()
        else :
            #print(f" ended as {filt}")
            filteredSegs[c] = filt

    return filteredSegs

# ------------------------------------------------------------------------
def transLiterate(segMappings) :
    elemParts={}
    for d in range(9) :
        segsInDigit = segmap[d]['elements']
        outSegsInDigit = []
        for n in segsInDigit :
            outSegsInDigit.extend(segMappings[n])
        outSegsInDigit = sorted(list(set(outSegsInDigit))) # make the values unique
        elemParts[d] = set(outSegsInDigit)
    return elemParts

# ------------------------------------------------------------------------
#After (simple) filtering,
#                 'a' is alway what's not shared between 7 and 1
#                 'b' is shared by 4 & 8 but NOT 1 & 7
#                 'c' is shared by 1,4,7,8
#                 'd' is what's shared by 4 and 8 but NOT 1 and 7
#                 'e' ONLY appears in 8
#                 'f' is shared by 1,4,7,8
#                 'g' ONLY appears in 8
def heuristicFilter(segMappings) :
    uniqueElems = transLiterate(segMappings)
    #Work out 'a'. This is our "gift":
    aSet=uniqueElems[7].difference(uniqueElems[1])
    segMappings['a'] = list(aSet)
    #remove from all the other mappings too
    for c in ['b','c','d','e','f','g'] :
        src=set(segMappings[c])
        segMappings[c] = list(src.difference(aSet))
    # "c" and "f" are the opposite of "a" - the segments that ARE shared by 1 and 7
    cfCand=uniqueElems[7].intersection(uniqueElems[1])
    segMappings['c'] = list(cfCand)
    segMappings['f'] = list(cfCand)
    # "b" and "d" can be calculated by the difference of 4 and (1 and 7) because 8 is everything
    bdCand=uniqueElems[4].difference(uniqueElems[1].union(uniqueElems[7]))
    segMappings['b'] = list(bdCand)
    segMappings['d'] = list(bdCand)
    #Determine "e"  and "g" candidates by subtracting everything else
    egCand=uniqueElems[8]
    for n in [1,4,7] :
        egCand=egCand.difference(uniqueElems[n])
    segMappings['e'] = list(egCand)
    segMappings['g'] = list(egCand)
    #No need to remove it from anything else, by definition it's not there.

    return segMappings
# --------------------------------------------------------------------------
def getCandBySeg(inSegMapping,v) :
    cand=[]
    for e in inSegMapping :
        if v in inSegMapping[e] :
            cand.append(e)
    return cand
# --------------------------------------------------------------------------
def filterFiveElements(inSegMapping,elemByDigit,numElem)  :
    # 2,3,5 are 5-element digits
    # 2,3,5 share 'a','d','g' (we know A at this point). If any of the input
    # "digits" are missing one of these, via the possible candidates, we can
    # use that to extract a mapping:
    segMapping=inSegMapping
    if inSegMapping['a'][0] not in numElem :
        print(f"Invalid number - must contain 'a' mapping ({inSegMapping['a'][0]}): {numElem}")
    missingCand=[]
    missingElem=list({'a','b','c','d','e','f','g'}.difference(set(numElem)))
    for v in missingElem:
        candElem=getCandBySeg(segMapping,v)
        if len(candElem)==1 :
            segMapping[candElem[0]] = [v]
        else :
            missingCand.extend(getCandBySeg(segMapping,v))
    return segMapping
# --------------------------------------------------------------------------
def filterSixElements(inSegMapping,elemByDigit,numElem)  :
    # 0,6,9 are 6-element digits
    # 0,6,9 share 'a','b','f','g'
    # If any of the incoming "digits" are missing one of these segments (via their
    # candidate mappings) we can use that to update the mapping table
    segMapping=inSegMapping
    if inSegMapping['a'][0] not in numElem :
        print(f"Invalid number - must contain 'a' mapping ({inSegMapping['a'][0]}): {numElem}")
    missingCand=[]
    missingElem=list({'a','b','c','d','e','f','g'}.difference(set(numElem)))
    for v in  missingElem:
        missingCand.extend(getCandBySeg(segMapping,v))
    revMissingCand=[]
    for vMis in missingCand :
        if vMis not in ['a','b','f','g'] :
            revMissingCand.append(vMis)
    if len(revMissingCand)== 1 :
        segMapping[revMissingCand[0]] = missingElem
    return segMapping
# --------------------------------------------------------------------------
def complexFilter(inSegMapping,nonUniqueNumbers) :
    elemByDigit = transLiterate(inSegMapping)
    segMapping=inSegMapping
    #There's a "gimme" by filtering 6-elements first:
    sixSeg=[]
    fiveSeg=[]
    for n in nonUniqueNumbers :
        if n['count']==5 :
            fiveSeg.append(n['elements'])
        elif n['count']==6 :
            sixSeg.append(n['elements'])
        else :
            print(f"WTF invalid length: {n}")
            exit(1)
    for n in sixSeg :
        segMapping=filterSixElements(segMapping,elemByDigit,n)
    for n in fiveSeg :
        segMapping=filterFiveElements(segMapping,elemByDigit,n)

    #FINAL filter as one will be left over:
    for s in segMapping :
        if len(segMapping[s]) > 1 :
            fSeg='z'
            cannotbe=[]
            for v in segMapping[s] :
                for n in segMapping :
                    if n == s :
                        continue
                    else :
                        cannotbe.extend(segMapping[n])
                if v not in cannotbe :
                    segMapping[s] = v
        else :
            segMapping[s] = segMapping[s][0]

    return segMapping
# --------------------------------------------------------------------------
def decodeDigit(inDigit,lookupTable,digitLUT) :
    decode=[]
    for c in inDigit :
        if c in lookupTable.keys() :
            decode.append(lookupTable[c])
        else :
            print(f"Unable to locate translation for {c} in {lookupTable}")
            exit()
    decStr=''.join(sorted(decode))
    if decStr in digitLUT.keys() :
        return {''.join(sorted(inDigit)) : digitLUT[decStr]}
    else :
        print(f"Unable to lookup {decStr} in lookup table {digitLUT}")
        exit()
# --------------------------------------------------------------------------
def invertSegmap() :
    inverted={}
    for d in segmap :
        v=''.join(sorted(segmap[d]['elements']))
        inverted[v]=d
    return inverted
# --------------------------------------------------------------------------
def decodeSequence(sequence) :
    #initialise a struct from which to deduce the mapping:
    outSegMapping = {a : [b for b in ['a','b','c','d','e','f','g']]  for a in ['a','b','c','d','e','f','g']}
    input=sequence[0]
    outdigits=sequence[1]
    #extract the "easy" numbers from the input
    uniqs=[]
    nonUniqs=[]
    lookupTable={}
    for sig in input :
        nDig=sig['count']
        elem=sig['elements']
        if sig['count'] in [2,3,4,7] :
            n=simpMap[nDig]
            lookupTable[''.join(elem)]=n
            uniqs.append(sig)
        else :
            nonUniqs.append(sig)
    #Reduce the output for the simple ones:
    for digit in uniqs :
        uniqSegMapping = filterSimple(outSegMapping,digit)
    uniqSegMapping=heuristicFilter(uniqSegMapping)
    segMapping = complexFilter(uniqSegMapping,nonUniqs)
    #invert segMapping to become our lookup table
    finalSegMapping={}
    for s in segMapping :
        if len(segMapping[s])>1 :
            print(f"Error decoding sequence, ended up with {segMapping}")
            exit()
        else :
            finalSegMapping[segMapping[s]] = s
    #turn the segment mapping into a digits lookup table
    digitLUT=invertSegmap()
    for nonU in nonUniqs :
        lookupTable.update(decodeDigit(nonU['elements'],finalSegMapping,digitLUT))

    #mechanically assemble the final number from the lookup table
    #(this is horribly ugly but I'm tired and fed up)
    outStr=""
    for outD in outdigits :
        if outD in lookupTable :
            outStr += str(lookupTable[outD])
        else :
            print(f"\nUnable to lookup {outD} in table {lookupTable}")
            exit(1)
    return int(outStr)


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
if __name__ == "__main__" :
    numberSequences=parseInputFile(inputfile)
    sum=0
    for seq in numberSequences :
        num = decodeSequence(seq)
        sum += num

    print(f"Sum of {len(numberSequences)} is {sum}")
