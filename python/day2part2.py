#!/usr/bin/python3
# Python solution for AOC 2021 Day 2, Part 2
# Given an input of steering commands, work out the position of the submarine
# permuted by something called "aim"

#inputfile="data/day2test.txt"
inputfile="data/day2part1.txt"

# horizontal is "pure" (affected directly by forward/back commands)
# but depth is affected by aim and horizontal commands.
# essentially up/down commands change the angle of steering fins...
horizontal = 0
aim = 0
depth = 0

cmdcount=0
with open(inputfile,'r') as instructions:
    for command in instructions:
        cmdcount+=1
        #split into a <direction> <distance> pair
        cmd,size = command.split(' ')
        size = int(size)
        #Action based on command:
        if cmd.lower() == "forward" :
            horizontal += size
            depth += (aim * size)
            if depth < 0 :
                depth = 0 # Guard against flying out of the ocean....
        elif cmd.lower() == "down" :
            aim += size
        elif cmd.lower() == "up" :
            aim -= size
        else :
            print(f"FAILED TO PARSE COMMAND: {command} - I only got {cmd},{distance}")
            cmdcount-=1

print(f"Final position after {cmdcount} valid commands is horizontal = {horizontal}, depth = {depth}")
print(f"Position Product is therefore: {horizontal * depth}")
