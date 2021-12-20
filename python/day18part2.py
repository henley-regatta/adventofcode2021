#!/usr/bin/python3
# Python solution for AOC 2021 Day 18, Part 2
#
# Snailfish Homework Day. Snailfish count in Vectors. A number is either a
# "pair" - ordered list of 2 numbers or a scalar. Oh wow this is complicated.
#
# What is the largest Magnitude you can get from adding only 2 of the snailfish
# numbers ?
#
# thankfully this builds on the part 1 solution. I can see BRUTE FORCE coming
# in here because I have *had it* with this dreck.
# (not least of all because there's only 100 input numbers so only 10K evals)
# evaluations to try.
#
# I could even multi-thread it, I suppose. But there's not much point when
# naïve runtime is only 10 seconds.

#-----------------------------------------------------------------------
def addSnailFishNumbers(n1,n2) :
    sum = "[" + n1 + "," + n2 + "]"
    #print(f"{n1} + {n2} = {sum}")
    #NOPE only do the reduce AFTER all the sums:
    return sum

#-----------------------------------------------------------------------
#If any pair is nested inside four pairs, the leftmost such pair explodes.
#To explode a pair, the pair's left value is added to the first regular
#number to the left of the exploding pair (if any), and the pair's right
#value is added to the first regular number to the right of the exploding
#pair (if any). Exploding pairs will always consist of two regular numbers.
#Then, the entire exploding pair is replaced with the regular number 0.
def explodeNumber(num) :
    out=""
    d=0
    for i in range(len(num)) :
        if num[i]=="[" :
            d+=1
        elif num[i] == "]" :
            d-=1
        out+=num[i] # Start with a copy....
        if d>4 :   # are we at depth==4 time to explode?
            #NOTE: both first and second numbers could be 2-digit. Hence
            #use of "index"
            #first=int(num[i+1])
            #second=int(num[i+3])
            sPos=num.index(",",i)
            first=int(num[i+1:sPos])
            ePos=num.index("]",sPos)
            second=int(num[sPos+1:ePos])
            tail=num[ePos+1:] #Strip the pair's "]" from the tail
            head=out[0:i] #Strip the last append - the "[" - from the input
            #print(f"exploding pair {first} {second} from {head} : {tail}")
            #increment last number in head
            v=""
            inVal=False
            sHead=-1
            for h in range(len(head)-1,-1,-1) :
                if not inVal and head[h].isdigit() :
                    inVal=True
                    sHead=h
                    v=head[h]
                elif inVal and head[h].isdigit() :
                    v = head[h] + v
                elif inVal and not head[h].isdigit() :
                    inVal=False
                    v=int(v)
                    r=v+first
                    #print(f"found head num {v} -> {r}")
                    head=head[0:h+1] + str(r) + head[sHead+1:]
                    break
            #increment first number in tail :
            v=""
            sTrail=-1
            inVal=False
            for t in range(len(tail)) :
                if not inVal and tail[t].isdigit() :
                    sTrail=t
                    inVal=True
                    v=tail[t]
                elif inVal and tail[t].isdigit() :
                    v+=tail[t]
                elif inVal and not tail[t].isdigit() :
                    inVal=False
                    v=int(v)
                    r=v+second
                    #print(f"found tail num {v} -> {r}")
                    tail = tail[0:sTrail] + str(r) + tail[t:]
                    break
            return head + "0" + tail # we don't need to look any further
    return out # but we might drop out the bottom having done nothing
#-----------------------------------------------------------------------
#If any regular number is 10 or greater, the leftmost such regular number splits.
#To split a regular number, replace it with a pair; the left element of the
#pair should be the regular number divided by two and rounded down, while the
#right element of the pair should be the regular number divided by two and
#rounded up.
def splitNumber(num) :
    out=""
    for i in range(len(num)) :
        if num[i].isdigit() and num[i+1].isdigit() : # We've hit a number and it's 10 or over
            fIndex=i+1
            tosplit=""
            for j in range(i,len(num)) :
                if num[j].isdigit() :
                    tosplit += num[j]
                else :
                    fIndex=j
                    break
            tosplit=int(tosplit)
            d1=tosplit//2 #this rounds-down which is what we want anyway
            d2=tosplit-d1 #and this is the remainder which is nice
            replPair = "[" + str(d1) + "," + str(d2) + "]"
            #print(f"splitting {tosplit} to {replPair}")
            #print(f"tosplit: {tosplit} d1: {d1} d2: {d2} replPair: {replPair}")
            out +=  replPair + num[fIndex:]
            return out
        else :
            out += num[i]

    return out
#-----------------------------------------------------------------------
def reduceNumber(num) :
    #print(num,end=":")
    while True :
        n1=explodeNumber(num)
        if n1 != num :
            #print(f"exploded: {n1}")
            num=n1
            continue
        n2=splitNumber(num)
        if n2 != num :
            #print(f"split : {n2}")
            num=n2
            continue
        return num
#-----------------------------------------------------------------------
# The magnitude of a pair is 3 times the magnitude of its left element plus
# 2 times the magnitude of its right element. The magnitude of a regular number
# is just that number. Magnitude calculations are recursive
def calcMagnitude(num) :
    n = eval(num)

    return getMagnitude(n)
#-----------------------------------------------------------------------
def getMagnitude(n) :
    n1=n[0]
    n2=n[1]
    if isinstance(n1,int) :
        magnitude = 3 * n1
    else :
        magnitude = 3 * getMagnitude(n1)
    if isinstance(n2,int) :
        magnitude = magnitude + 2 * n2
    else :
        magnitude = magnitude + 2 * getMagnitude(n2)

    return magnitude

#-----------------------------------------------------------------------
def testSuite() :
    explodeTest="""[[[[[9,8],1],2],3],4] [[[[0,9],2],3],4]
[7,[6,[5,[4,[3,2]]]]] [7,[6,[5,[7,0]]]]
[[6,[5,[4,[3,2]]]],1] [[6,[5,[7,0]]],3]
[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] [[3,[2,[8,0]]],[9,[5,[7,0]]]]"""
    for l in explodeTest.splitlines() :
        n,v = l.split()
        r=explodeNumber(n)
        print(f"{n} -> {r}",end=" : ")
        if r==v :
            print("OK")
        else :
            print("FAIL")
            print(r)
            print(v)
            exit()

    splitTest="""[[[[9,[9,1]]]]] [[5,5]]"""
    for l in splitTest.splitlines() :
        n,v = l.split()
        r=reduceNumber(n)
        print(n)
        print(r)

    sumTest="""[[[[4,3],4],4],[7,[[8,4],9]]]  [1,1] [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]] [7,[[[3,7],[4,3]],[[6,3],[8,8]]]] [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"""
    for l in sumTest.splitlines() :
        p1,p2,v = l.split()
        r=reduceNumber(addSnailFishNumbers(p1,p2))
        print(f"{p1} + {p2} = {r}", end=" : ")
        if r==v :
            print("OK\n")
        else :
            print("FAIL")
            print(r)
            print(v)
            exit()

    print("\nBIG SUM TEST")
    smolSumTest="""[1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    [6,6]"""
    bigSumTest="""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]  [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]] [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]] [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
[7,[5,[[3,8],[1,4]]]] [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
[[2,[2,2]],[8,[8,1]]]  [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
[2,9] [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
[1,[[[9,3],9],[[9,0],[0,7]]]] [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
[[[5,[7,4]],7],1] [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
[[[[4,2],2],6],[8,7]]  [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"""

    acc=""
    for d in bigSumTest.splitlines() :
        print(f"in: {d}")
        if acc == "" :
            acc = d
        else :
            n,v = d.split()
            acc = reduceNumber(addSnailFishNumbers(acc,n))
            if acc != v :
                print("FAIL SUM: ")
                print(f"SUM: {acc}")
                print(f"CHK: {v}")
                exit()
            else :
                print(f"OK : {acc}")
    result=acc
    if result == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]" :
        print("Big Sum Added Up Correct")
    else :
        print("Big Sum Failed")
        exit()

    magnitudeTest="""[9,1]  29
[1,9]  21
[[9,1],[1,9]]  129
[[1,2],[[3,4],5]]  143
[[[[0,7],4],[[7,8],[6,0]]],[8,1]]  1384
[[[[1,1],[2,2]],[3,3]],[4,4]]  445
[[[[3,0],[5,3]],[4,4]],[5,5]]  791
[[[[5,0],[7,4]],[5,5]],[6,6]]  1137
[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]  3488
"""
    for m in magnitudeTest.splitlines() :
        n,v=m.split()
        mag=calcMagnitude(n)
        print(f"{n} magnitude: {mag}", end=":")
        if str(mag) == v :
            print("OK")
        else :
            print("FAIL")
            print(mag)
            print(v)
            exit()

    finalExamTest ="""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    acc=""
    for n in finalExamTest.splitlines() :
        if acc == "" :
            acc = n
        else :
            acc = reduceNumber(addSnailFishNumbers(acc,n))
    result=acc
    print(f"sum result: {result}")
    if result != "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]" :
        print("didn't get correct sum, no point proceeding")
        print(result)
        print("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
        exit()

    finalResult = calcMagnitude(result)
    print(f"{result} got magnitude {finalResult}, should be 4140",end=":")
    if finalResult == 4140 :
        print("OK passed final check")
    else :
        print("FAIL abort")
        exit()

    return True
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    if testSuite() :
        print("sailfish math works out OK")
        print("-" * 80)

    #Part 2 requires a bigger test-set.
    p2testData="""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    tData=[]
    for l in p2testData.splitlines() :
        tData.append(l)

    maxMagnitude=0
    numA=""
    numB=""
    for a in range(len(tData)) :
        for b in range(len(tData)) :
            if a==b :
                continue
            mag=calcMagnitude(reduceNumber(addSnailFishNumbers(tData[a],tData[b])))
            if mag > maxMagnitude :
                maxMagnitude = mag
                numA=tData[a]
                numB=tData[b]

    print(f"Largest 2-sum magnitude found : {maxMagnitude}, came from sum of: ")
    print(f"A: {numA}\nB: {numB}")
    if(maxMagnitude != 3993) :
        print("test failed, should have got 3993")
        exit()
    else :
        print("=" * 80)
        print("=" * 80)

    liveData=[]
    with open("data/day18part1.txt",'r') as sums :
        for line in sums:
            liveData.append(line.strip())

    print(f"Working out biggest magnitude from {len(liveData)} input numbers")
    import time
    sInit=time.perf_counter()
    scounter=0
    maxCounter=len(liveData) ** 2 - len(liveData)
    maxMagnitude=0
    for a in range(len(liveData)) :
        for b in range(len(liveData)) :
            if a == b :
                continue # no square(numbers) allowed
            mag=calcMagnitude(reduceNumber(addSnailFishNumbers(liveData[a],liveData[b])))
            if mag > maxMagnitude :
                maxMagnitude = mag
                numA=liveData[a]
                numB=liveData[b]
            #Bookkeeping & Reporting
            scounter+=1
            if scounter%1000==0 :
                tElapsed=time.perf_counter() - sInit
                pctProc=scounter/maxCounter
                tTotal=tElapsed * 1/pctProc
                tRemain = tTotal - tElapsed
                print(f"Loop {scounter}. Remaining: {maxCounter-scounter} {pctProc:.2%} {tRemain:.2f} seconds remaining")
    print(f"Largest 2-sum magnitude found : {maxMagnitude}, came from sum of: ")
    print(f"A: {numA}\nB: {numB}")
