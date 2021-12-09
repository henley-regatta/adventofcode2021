#!/usr/bin/python3
# Python solution for AOX 2021 Day 2, Part 1
# Given an input of steering commands, work out the position of the submarine

#inputfile="data/day2test.txt"
inputfile="data/day2part1.txt"

#we're only tracking forward/back and up/down
horizontal = 0
depth = 0

cmdcount=0
with open(inputfile,'r') as instructions:
    for command in instructions:
        cmdcount+=1
        #split into a <direction> <distance> pair
        cmd,distance = command.split(' ')
        distance = int(distance)
        #Action based on command:
        if cmd.lower() == "forward" :
            horizontal += distance
        elif cmd.lower() == "back" :
            horizontal += distance
        elif cmd.lower() == "down" :
            depth += distance
        elif cmd.lower() == "up" :
            if distance > depth :
                depth = 0
            else :
                depth -= distance
        else :
            print(f"FAILED TO PARSE COMMAND: {command} - I only got {cmd},{distance}")
            cmdcount-=1

print(f"Final position after {cmdcount} valid commands is horizontal = {horizontal}, depth = {depth}")
print(f"Position Product is therefore: {horizontal * depth}")
