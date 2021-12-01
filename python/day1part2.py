#!/usr/bin/python3
# Python solution for AOX 2021 Day 1, Part 2
# Given an input "sonar depth readings", use a 3-measurement sliding window
# to assess increases, reporting the number of increases.

#inputfile = "data/day1test.txt"
inputfile = "data/day1part1.txt"

lc=0
windows=[]
winsize=3
#This is the reading loop
with open(inputfile,'r') as sonarreadings:
    for reading in sonarreadings:
        lc+=1
        ping=int(reading)
        windows.append(ping)
        ptr = len(windows) -1
        if ptr < winsize :
            for i in range(0,ptr) :
                windows[i] += ping
        else :
            for i in range(1,winsize) :
                x = ptr-i
                windows[x] += ping
#the last winsize-1 readings are bogus, drop them
for i in range(1,winsize) :
    windows.pop()

#The answer is just the same as part 1, but now we've got a list it's easier to compute
increases=0
for i in range(len(windows)) :
    if i == 0 :
        continue
    if windows[i] > windows[i-1] :
        increases+=1

print(f"Over {len(windows)} measurement windows, found {increases} reading increases")
