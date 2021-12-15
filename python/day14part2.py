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
###############################################################################
# The key insight is that if, at stage x you have n occurrences of pattern "ab",
# which produces insert "c", then at stage x+1 you're going to have n occurrences
# of pattern "ac", and n occurrences of "cb", AND lose n occurrences of "ab".
#
# This needs initialising with the first set of pair matches from the template.
#
# The final result is calculated by summing each character of each pair match
# then dividing the result by two (because each value overlaps). The FIRST and
# LAST character of the template are then added back to the totals (as they are
# constant in the output.)


#inputfile = "data/day14test.txt"
inputfile = "data/day14part1.txt"

#This is load-and-forget/use-everywhere so is a candidate for a global var:
pRules={}

# ---------------------------------------------------------------
def loadTemplateAndRules(file) :
    #The template is the first line of input, there's a blank, then
    #everything else is a production rule
    global pRules
    global cCounter
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
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    template=loadTemplateAndRules(inputfile)
    #Initialise the pair count against this
    pCounter= {pair: 0 for pair in pRules.keys()}
    for pair in [template[i:i+2] for i in range(0,len(template)-1)] :
        pCounter[pair]+=1

    #print(f"init : {pCounter}")
    #Now we can iterate for each of the pairs at each stage:
    for i in range(40) :
        #Use this form of "cast to list" to get a STATIC reading of the pCounter at iteration time
        for pair,cCount in list(pCounter.items()) :
            #print(f"{pair}:{cCount}")
            if cCount > 0 :
                head=pair[0] + pRules[pair]
                tail=pRules[pair] + pair[1]
                pCounter[head] += cCount
                pCounter[tail] += cCount
                pCounter[pair] -= cCount #nb this might not go to zero if head or tail match pair
        #print(f"{i} : {pCounter}")

    #Calculate the final element counts:
    eCounter = {}
    for pair in pCounter :
        for e in pair :
            if e not in eCounter :
                eCounter[e] = pCounter[pair]
            else :
                eCounter[e] += pCounter[pair]
    #Correct for "overlaps" and replace the start/finish elements
    for e in eCounter :
        eCounter[e] = eCounter[e]//2
        if e == template[0] or e == template[-1] :
            eCounter[e] += 1

    elemCounts=dict(sorted(eCounter.items(), key=lambda x: x[1]))
    k = list(elemCounts.keys())
    print(f"biggest elem:  {k[-1]} ({elemCounts[k[-1]]})")
    print(f"smallest elem: {k[0]} ({elemCounts[k[0]]})")
    bigAnswer = elemCounts[k[-1]] - elemCounts[k[0]]
    print(f"Magic Answer To Question: {elemCounts[k[-1]] - elemCounts[k[0]]}")
