#!/usr/bin/python3
# Python solution for AOC 2021 Day 1, part 1
#
# Given a list of numbers of lanternfish representing days-to-reproduce,
# calculate the number of fish after N days.
#
# Part 2 makes N=256 (up from 80), leading to algorithmic explosion. We Need
# A Better Algorithm.
# Fortunately, because fish are simple, we can put them into buckets by age...

#inputfile="data/day6test.txt"
inputfile="data/day6part1.txt"

#-----------------------------------------------------------------------
def buckSum(bucket) :
    bsum=0
    for b in bucket :
        bsum+=b
    return bsum
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
fbucket=[0 for i in range(9)]
with open(inputfile,'r') as fishdata:
    for l in fishdata:
        fs = l.strip().split(',')
        for s in fs : fbucket[int(s)]+=1

day=0
print(f"Day {day}, numfish: {buckSum(fbucket)}, state: {fbucket}")
lastday=256
while day<lastday :
    day += 1
    nextbucket=[0 for i in range(9)]

    for j in range(len(fbucket)) :
        i=8-j #important to count DOWN not up to prevent overwrite-by-zero
              #(there has to be a better way to do reverse iteration than that)
        if i == 0 :
            nextbucket[6] = fbucket[7] + fbucket[i] #existing fish
            nextbucket[8] = fbucket[i] #newfish
        else :
            nextbucket[i-1] = fbucket[i]
    fbucket = nextbucket
    print(f"Day {day}, numfish: {buckSum(fbucket)}")

print(f"On the last day, {day}, there were {buckSum(fbucket)} fish")
