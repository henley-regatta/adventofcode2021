#!/usr/bin/python3
# Python solution for AOC 2021 Day 10, Part 1
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
# Do some maths based on the first illegal character on the line.

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
    print(f"{len(openChunks)} {openChunks} : {line}",end=" : ")
    #on entry we're expecting AT LEAST an opener and a closer.
    if len(line)<2 : #We're expecting at least an opener and a closer at this point.
        print("incomplete")
        incompleteLine=True
        return ""
    elif line[0] not in startToks :
        print(f"{line[0]} invalid starter")
        corruptLine=True
        badchars.append(line[0])
        return ""
    #OK. At this point we can split the line into our opener and the rest of the line
    tokOpen=line[0]
    line=line[1::]
    #What we do next depends on what the next char in the list is:
    if line[0] == cDelim[tokOpen] :
        #We immediately found our closer. Good
        print(f"{tokOpen} immediately closed by {line[0]}")
        #consume both tokens and return the remainder of the line
        return line[1::]
    elif line[0] not in startToks :
        #we've found a closer but an invalid one.
        print(f"{line[0]} invalid closer for {tokOpen}")
        badchars.append(line[0])
        return ""
    else :
        #depth-first search for our closer
        while len(line)>0 and line[0] != cDelim[tokOpen] :
            print(f"recurse to match {tokOpen}...")
            line = grokChunk(openChunks+tokOpen,line)
        #Did we find it?
        if len(line)>0 and line[0] == cDelim[tokOpen] :
            print(f"{len(openChunks)} : {openChunks} : {tokOpen} eventually closed by {line[0]}")
            return line[1::]
        else :
            print(f"Never found closer for {tokOpen}, incomplete")
            incompleteLine=True
            return ""
#-----------------------------------------------------------------------
def calcSyntaxScore(invalidChars) :
    score = 0
    for c in invalidChars :
        if c == ')' :
            score += 3
        elif c == ']' :
            score += 57
        elif c == '}' :
            score += 1197
        elif c == '>' :
            score += 25137
        else :
            print(f"incorrect invalid char '{c}'")
            exit()
    return score
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    #Bad Character tracker (calc score.)
    lc=0
    incompleteCounter=0
    badchars=[]
    with open(inputfile,'r') as navcode :
        for line in navcode :
            lc+=1
            line = line.strip()
            incompleteLine=False
            corruptLine=False
            while len(line) > 0 :
                line=grokChunk("",line)
            if incompleteLine and not corruptLine :
                incompleteCounter+=1
    print(f"{lc} lines in input. {incompleteCounter} were incomplete")
    print(f"Corrupt closers found: {badchars}")
    print(f"Gives a final incorrect score(?) of {calcSyntaxScore(badchars)}")
