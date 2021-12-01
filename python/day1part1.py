#!/usr/bin/python3
# Python solution for AOX 2021 Day 1, Part 1
# Given an input "sonar depth readings"
# count how many entries successively increase from measurement to measurement
# report the count of increases

#inputfile = "data/day1test.txt"
inputfile = "data/day1part1.txt"


increases=0
lastreading=0
lc=0
with open(inputfile,'r') as sonarreadings:
    for reading in sonarreadings:
        ping=int(reading)
        lc+=1
        print(f"{lc} : {ping}",end=" ")
        if lastreading != 0:
            if ping > lastreading:
                print("increase")
                increases+=1
            else:
                print("decrease")
        else:
            print("(n/a)")
        lastreading = ping

print(f"Out of {lc} lines, {increases} measurements increased from previous")
