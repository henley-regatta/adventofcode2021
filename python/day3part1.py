#!/usr/bin/python3
# Python solution for AOC 2021 Day 3, Part 1
# Given an input of 5-bit binary numbers, calculate "gamma" and "epsilon"
# and provide the power consumption as the product of the two.
#
# "gamma" is calculated as the number resulting from taking the most-popular
# value across all input numbers at each bit position.
#
# "epsilon" is the opposite - the least-popular value for each bit across all
# input numbers

#inputfile="data/day3test.txt"
inputfile="data/day3part1.txt"

#Iterate over the input calculating the sum of each bit position as we go
bitsums=[]
numvals=0
with open(inputfile,"r") as readings:
    for bitval in readings:
        if len(bitval) > 0 :
            numvals += 1
            #Initialise the array if empty
            if len(bitsums) == 0 :
                bitsums = [0] * (len(bitval)-1)
        for i in range(0, len(bitval)) :
            if bitval[i] == '1' :
                bitsums[i] += 1
print(f"Read {numvals} numbers with bitsums = {bitsums}")

#Build gamma and epsilon.
#Since we're using sums, "most popular" is met if the bitsum position is >50%
#of the number of values read. So we need that number first:
halfvalues = numvals / 2
gamma=""
epsilon=""
for b in bitsums:
    if b > halfvalues:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"
#Convert both to decimal
g_num = int(gamma,2)
e_num = int(epsilon,2)

print(f"With threshold {halfvalues}, gamma = {gamma} ({g_num}) and epsilon = {epsilon} ({e_num})")
print(f"This makes the power consumption: {g_num * e_num}")
