#!/usr/bin/python3
# Python solution for AOC 2021 Day 1, part 1
#
# Given a list of numbers of lanternfish representing days-to-reproduce,
# calculate the number of fish after N days.

#inputfile="data/day6test.txt"
inputfile="data/day6part1.txt"

fish=[]
with open(inputfile,'r') as fishdata:
    for l in fishdata:
        fs = l.strip().split(',')
        for s in fs : fish.append(int(s))

day=0
print(f"Day {day}, state: {fish}")
lastday=80
while day<lastday :
    day += 1
    for f in range(len(fish)) :
        if fish[f] == 0 :
            fish.append(8)
            fish[f]=6
        else :
            fish[f]-=1
    print(f"Day {day}, numfish: {len(fish)}")

print(f"On the last day, day {day}, there were {len(fish)} fish")
