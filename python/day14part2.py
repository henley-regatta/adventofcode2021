#!/usr/bin/python3
# Python solution for AOC 2021 Day 14, Part 2
#
# Given input consisting of a "template" and some production rules,
# iteratively "polymerize" the template according to the rules. Output is
# simultaneous - all rules are applied *at once* to the input at stage N to
# produce the output at stage N+1 (i.e. updates along the template aren't
# sequential.)
#
# Part 2 asks for the sums after 40 iterations. Given the exponential growth,
# this isn't feasibly calculable using the naieve approach (which becomes
# untenable after ~20 iterations). Instead we're going to need to Get Smart...
#
# NOTE: Caching doesn't work. I've tried it.
# NOTE2: The Naieve approach doesn't work. The OOM killer reaps after ~26 iterations.
#
# The question asks for a COUNT of the most frequent and least frequent chars
# in the output. It doesn't ask for the final sequence. This HAS TO BE a clue...
#
# The string length at step N = (2 x length(n-1))-1, and requires length(n-1)-1
# insertions to generate.
#
# I've done enough checking to know that just working out the output relative
# frequency of chars isn't enough to come close to predicting the answer.

inputfile = "data/day14test.txt"
#inputfile = "data/day14part1.txt"

#This is load-and-forget/use-everywhere so is a candidate for a global var:
pRules={}

# ---------------------------------------------------------------
def loadTemplateAndRules(file) :
    #The template is the first line of input, there's a blank, then
    #everything else is a production rule
    global pRules
    template=""
    with open(file,'r') as ifile :
        #Extract the template:
        template = ifile.readline().strip()
        #Now extract the production rules:
        for l in ifile :
            rls = l.strip().split(' -> ')
            if len(rls) == 2 :
                pRules[rls[0]]=rls[1]

    return template

#-----------------------------------------------------------------------
def iteratePolymer(polyStr) :
    outAdds=""
    for x in range(0,len(polyStr)-1) :
        outAdds += pRules[polyStr[x:x+2]]
    #print(f"in: {polyStr} adds: {outAdds}")
    outStr=""
    for c in range(0,len(polyStr)-1) :
        outStr += polyStr[c] + outAdds[c]
    return outStr + polyStr[-1]
#-----------------------------------------------------------------------
def countCharType(inStr) :
    cCount={}
    for c in inStr :
        if c not in cCount :
            cCount[c] = 1
        else :
            cCount[c] += 1
    #We want the biggest and the littlest so sort the output
    return dict(sorted(cCount.items(), key=lambda x: x[1]))
#-----------------------------------------------------------------------
def getPartOneAnswer(polymer) :
    print(f"Polymer has grown to length {len(polymer)}")
    cCounts=countCharType(polymer)
    k=list(cCounts.keys())
    bigNum=cCounts[k[-1]]
    smolNum=cCounts[k[0]]
    print(f"Most numerous element:  {k[-1]} ({bigNum})")
    print(f"Least numerous element: {k[0]} ({smolNum})")
    print(f"Part One Answer: {bigNum - smolNum}")

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    polymer=loadTemplateAndRules(inputfile)
    print(f"Start : {polymer}")
    startPairs = [polymer[i:i+2] for i in range(0,len(polymer),n)]
    pCounter={}
    lim=10
    for pair in startPairs :
        cDepth=iterDepth(pair,lim)

        print(f"{x} : length {len(polymer)}")

    getPartOneAnswer(polymer)
