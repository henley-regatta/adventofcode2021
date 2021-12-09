#!/usr/bin/python3
# Python solution for AOX 2021 Day 8, Part 1
# Given an input of messed-up "segment inputs" and a 4-digit output value,
# work out which signal a-g displays which element of a 7-segment display

# NB: MUCH OF THIS IS UNNEEDED - PART1 IS A MUCH SIMPLIFIED QUESTION:
# "How many times do the unique-length numbers 1,4,7 or 8 appear in the output?"

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
#From this we derive a reverse:
candDigitBySegmentsLit={2 : [1],
                        3 : [7],
                        4 : [4],
                        5 : [2,3,5],
                        6 : [0,6,9],
                        7 : [8]}
#this means 2-,3-,4- and 8-wordlength inputs are instantly recognisable as
#digits BUT not necessarily the segment order. On with the show!

# --------------------------------------------------------------------------
def parseSegSequence(seq) :
    outSeq=[]
    for c in seq :
        outSeq.append(c)
    return {'count' : len(outSeq), 'elements' : outSeq}


# --------------------------------------------------------------------------
def parseInputFile(file) :
    #Input is of format [<word>]x10 | [<word]x4
    #with the part before the delimiter the "segment" input and the bit
    #after the "output digits"
    sequences=[]
    with open(file,'r') as data:
        for sequence in data :
            d=sequence.strip().split('|')
            inList=[parseSegSequence(x) for x in d[0].split()]
            outList=[parseSegSequence(y) for y in d[1].split()]
            sequences.append([inList,outList])
    return sequences

# --------------------------------------------------------------------------
def filterSimple(candMap,sig) :
    outMap=candMap
    #tbh this is easier:
    if sig['count'] == 2 :
        outDigit=1
    elif sig['count'] == 3 :
        outDigit=7
    elif sig['count'] == 4 :
        outDigit = 4
    elif sig['count'] == 7 :
        outDigit = 8
    else :
        print(f"Invalid digit {sig} passed to filterSimple")
        exit()

    filteredSegs=[]
    for c in candMap[outDigit] :
        if c in sig['elements'] :
            filteredSegs.append(c)
    if len(filteredSegs)==0 :
        print(f"Oops. Filtered out all possible segments for digit {outDigit}")
        exit()
    else :
        outMap[outDigit] = filteredSegs
    return outMap
# --------------------------------------------------------------------------
def decodeSequence(sequence) :
    #initialise a struct from which to deduce the mapping:
    outmap=[[l for l in ['a','b','c','d','e','f','g']] for n in range(9)]
    input=sequence[0]
    outdigits=sequence[1]
    #extract the "easy" numbers from the input
    uniqs=[]
    complex=[]
    for sig in input :
        if sig['count'] in [2,3,4,7] :
            uniqs.append(sig)
        else :
            complex.append(sig)

    #Reduce the output for the simple ones:
    for digit in uniqs :
        outmap = filterSimple(outmap,digit)

    print("After unique digit filtering:")
    for d in range(len(outmap)) :
        print(f"{d} : {outmap[d]}")

# ------------------------------------------------------------------------
def part1GetUniqueOutputs(sequence) :
    countUniqs = 0
    for digit in sequence[1] :
        if digit['count'] in [2,3,4,7] :
            countUniqs += 1
    return countUniqs
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
if __name__ == "__main__" :
    numberSequences=parseInputFile(inputfile)
    sumOutUniqs=0
    for seq in numberSequences :
        sumOutUniqs += part1GetUniqueOutputs(seq)

    print(f"Found {sumOutUniqs} unique-length digits in the output")
