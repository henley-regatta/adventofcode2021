#!/usr/bin/python3
# Python solution for AOC 2021 Day 10, Part 2
#
# A Lexical parser.
# Given line-structured input, determine whether a line is "incomplete" or
# "corrupt" according to syntax rules:
#  A Line consists of one ore more *chunks*.
#  *chunks* can contain *chunks*.
#  Chunks are not separated by any delimiter.
#  A chunk must start and finish with one of the 4 pairs of matching chars:
#   (), [], {} or <>.
#
# A Corrupt chunk ends with an invalid char e.g. <}, (>
# Any corrupt chunk causes the whole line to be discarded.
#
# An incomplete line fails to terminate one or more chunks. Ignore these lines.
#
# Ignoring corrupt lines, make a correction so that incomplete lines parse.
# Do some maths on the correction.

#inputfile = "data/day10test.txt"
inputfile = "data/day10part1.txt"

cDelim = { '(' : ')', '[' : ']', '{' : '}', '<' : '>'}
startToks=list(cDelim.keys())
stopToks=list(cDelim.values())

#Because this is "stream input" we won't use our normal read-then-parse
#strategy, we'll do it like a grown up, line by line.

#-----------------------------------------------------------------------
# I know the answer is recursive, let's see how....
def grokChunk(openChunks,line) :
    global badchars
    global incompleteLine
    global corruptLine
    global missingClosures
    #on entry we're expecting AT LEAST an opener and a closer.
    if len(line)<2 : #We're expecting at least an opener and a closer at this point.
        incompleteLine=True
        if line[0] not in startToks :
            #corrupt
            corruptLine=True
            badchars.append(line[0])
        else :
            #incomplete
            newOpen=openChunks+line[0]
            if len(newOpen)>len(missingClosures) :
                missingClosures=newOpen
        return ""
    elif line[0] not in startToks :
        corruptLine=True
        badchars.append(line[0])
        return ""
    #To business...........
    #OK. At this point we can split the line into our opener and the rest of the line
    tokOpen=line[0]
    line=line[1::]
    #What we do next depends on what the next char in the list is:
    if line[0] == cDelim[tokOpen] :
        #We immediately found our closer. Good
        #consume both tokens and return the remainder of the line
        return line[1::]
    elif line[0] not in startToks :
        #we've found a closer but an invalid one.
        badchars.append(line[0])
        return ""
    else :
        #depth-first search for our closer
        while len(line)>0 and line[0] != cDelim[tokOpen] :
            line = grokChunk(openChunks+tokOpen,line)
        #Did we find it?
        if len(line)==0 :
            incompleteLine=True
            newOpen=openChunks+tokOpen
            if len(newOpen) > len(missingClosures) :
                missingClosures = newOpen
            return ""
        elif line[0] == cDelim[tokOpen] :
            return line[1::]

#-----------------------------------------------------------------------
#I'm sure there's rationale to this but from the outside it looks like
#made-up cobblers....
def calcClosureScore(closure) :
    score=0
    for c in closure :
        score=score*5
        if c == ')' :
            score += 1
        elif c == ']' :
            score += 2
        elif c == '}' :
            score += 3
        elif c == '>' :
            score += 4
        else :
            print(f"Invalid closure {c}")
            exit()
    return score
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #Bad Character tracker (calc score.)
    lc=0
    badchars=[]
    incompletes=[]
    with open(inputfile,'r') as navcode :
        for line in navcode :
            lc+=1
            line = line.strip()
            orgLine=line
            incompleteLine=False
            corruptLine=False
            missingClosures=[]
            while len(line) > 0 :
                line=grokChunk("",line)
            if incompleteLine and not corruptLine :
                incompletes.append([orgLine,missingClosures])

    print(f"{lc} lines in input. {len(incompletes)} were incomplete")
    #Generate the closures for each line, and calculate their scores:
    cScores=[]
    for l in incompletes :
        #Complete the string closures
        closure=""
        for c in reversed(l[1]) :
            closure += cDelim[c]
        closureScore=calcClosureScore(closure)
        print(f"Line {l[0]} is closed by  {closure} with score {closureScore}")
        cScores.append(closureScore)

    #Even more wierd maths
    cScores = sorted(cScores)
    #the actual score is the median from this list
    ptr=len(cScores)//2
    print(f"Median score of {len(cScores)} (index {ptr}) is: {cScores[ptr]}")
