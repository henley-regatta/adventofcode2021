#!/usr/bin/python3
# Python solution for AOC 2021 Day 3, Part 1
# Given an input of 5-bit binary numbers, calculate "oxygen" and "co2 scrubber"
# values and use that to determine life support rating.
#
# This uses a filtering process - described inline below - to extract the
# required numbers from the input string.

#inputfile="data/day3test.txt"
inputfile="data/day3part1.txt"

##########################################################################
# Find the most popular value (0,1) at position X in an array of binary numbers
def findMostPopularVal(numarray,pos) :
    halfval = len(numarray) / 2
    bitsum=0
    for num in numarray:
        bitsum += num[pos]
    if bitsum >= halfval :
        return 1
    else :
        return 0

###########################################################################
#Load the input stream into an array of binary numbers (as an array)
def buildBinaryArrayFromFile(filename) :
    valarray=[]
    with open(inputfile,"r") as readings:
        for bitval in readings:
            numArray = []
            for i in range(0,len(bitval)) :
                if bitval[i] == '1' :
                    numArray.append(1)
                elif bitval[i] == '0' :
                    numArray.append(0)
            valarray.append(numArray)
    return valarray

###########################################################################
# util func to filter array by val in pos x
def filterArrayByVal(inArray,val,bitPos) :
    outArray=[]
    for num in inArray:
        if num[bitPos] == val :
            outArray.append(num)
    return outArray

###########################################################################
def binNumArrayToDecimal(binArray) :
    binNum=0
    for i in range(len(binArray),0,-1) :
        bit=binArray[i-1]
        pow=len(binArray)-i
        bitval= 2**pow * bit
        binNum+=bitval
        #print(f"{binArray}({i}) bit {bit} dec {bitval} sum: {binNum}")
    return binNum

###########################################################################
# A recursive function to calculate the oxygen generator rating.
# It's a fancy form of filtering with a STOP condition when the inNumbers
# array has only a single member
def findOxyRating(inNumbers, ndx) :
    selectVal = findMostPopularVal(inNumbers,ndx)
    filteredNumbers = filterArrayByVal(inNumbers,selectVal,ndx)

    if len(filteredNumbers) == 1 :
        #FOUND IT!
        return filteredNumbers[0]
    elif ndx == len(filteredNumbers[0]) :
        print(f"ERROR filtering numbers for findOxyRating - reached end but still have {len(filteredNumbers)} candidates: {filteredNumbers}")
    else :
        return findOxyRating(filteredNumbers,ndx+1)

###########################################################################
# I know I could coalesce these into 1 recursive call with appropriate
# filtering but Time Is Money.
def findCO2Rating(inNumbers, ndx) :
    selectVal = abs(findMostPopularVal(inNumbers,ndx)-1)
    filteredNumbers = filterArrayByVal(inNumbers,selectVal,ndx)

    if len(filteredNumbers) == 1 :
        #FOUND IT!
        return filteredNumbers[0]
    elif ndx == len(filteredNumbers[0]) :
        print(f"ERROR filtering numbers for findCO2Rating - reached end but still have {len(filteredNumbers)} candidates: {filteredNumbers}")
    else :
        return findCO2Rating(filteredNumbers,ndx+1)

###########################################################################
###########################################################################
###########################################################################
if __name__ == "__main__" :
    srcNumbers = buildBinaryArrayFromFile(inputfile)

    oxyGenRating = findOxyRating(srcNumbers,0)
    CO2ScrubRating = findCO2Rating(srcNumbers,0)
    o2rat=binNumArrayToDecimal(oxyGenRating)
    co2rat=binNumArrayToDecimal(CO2ScrubRating)
    print(f"Oxygen Generator Rating: {o2rat} {oxyGenRating}, CO2 Scrubber Rating: {co2rat} {CO2ScrubRating}\nLIFE SUPPORT RATING: {o2rat*co2rat}")
