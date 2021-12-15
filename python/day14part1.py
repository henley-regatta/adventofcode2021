#!/usr/bin/python3
# Python solution for AOC 2021 Day 14, Part 1
#
# Given input consisting of a "template" and some production rules,
# iteratively "polymerize" the template according to the rules. Output is
# simultaneous - all rules are applied *at once* to the input at stage N to
# produce the output at stage N+1 (i.e. updates along the template aren't
# sequential.)

#inputfile = "data/day14test.txt"
inputfile = "data/day14part1.txt"

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
def applyProdRules(inStr) :
    outStr=""
    global pRules
    #Iterate across the inStr string char-by-char, taking 2 chars at a
    #time:
    for x in range(len(inStr)-1) :
        cPair=inStr[x:x+2:]
        if cPair in pRules :
            #ONLY on the first input do we need to write cPair[0]
            if x==0 :
                outStr = cPair[0] + pRules[cPair] + cPair[1]
            else :
                outStr += pRules[cPair] + cPair[1]
        else :
            print("NONE")
    return outStr
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
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    polymer=loadTemplateAndRules(inputfile)
    print(f"start: {polymer}")
    for x in range(1,11) :
        polymer = applyProdRules(polymer)
        print(f"{x} : {countCharType(polymer)}")

    print(f"Polymer has grown to length {len(polymer)}")
    cCounts=countCharType(polymer)
    print(f"Poly Counts By Char: {cCounts}")
    k=list(cCounts.keys())
    bigNum=cCounts[k[-1]]
    smolNum=cCounts[k[0]]
    print(f"Most numerous element:  {k[-1]} ({bigNum})")
    print(f"Least numerous element: {k[0]} ({smolNum})")
    print(f"Part One Answer: {bigNum - smolNum}")
