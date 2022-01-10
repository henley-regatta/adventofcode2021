#!/usr/bin/python3
# Python solution for AOC 2021 Day 20 Part 1
#
# Given an "Image enhancement algorithm" and a noisy 2-dimensional image,
# apply the algo to the image (all pixels simultaneously).
#
# The mechanism works by using a 3-by-3 grid of the pixels around the target
# pixel combining to form an index number based on their binary code. This is
# then a lookup to the Algorithm to select an on/off pattern from it.
#
# Edge cases are handled by assuming the shown image is the "middle" of an
# infinitely-sized image (all other pixels being off). This allows the image
# to "grow" outwards over time as successive optimisations are applied.

#infile="data/day20test.txt"
infile="data/day20part1.txt"

#-----------------------------------------------------------------------
def readInputAlgoAndImage(fromfile) :
    algorithm=""
    image = []
    with open(fromfile,'r') as stuff :
        for l in stuff :
            d=l.strip()
            if len(d)>0 :
                if algorithm == "" :
                    algorithm = d
                else :
                    image.append(d)

    return [image,algorithm]
#-----------------------------------------------------------------------
def drawImage(image) :
    for l in image :
        print(l)
#-----------------------------------------------------------------------
def countSetPixelsInImage(image) :
    pixelsSet=0
    for l in image :
        pixelsSet += l.count('#')
    return pixelsSet
#-----------------------------------------------------------------------
def countClippedSetPixelsInImage(image) :
    pixelsSet=0
    for y in range(1,len(image)-2) :
        l=image[y]
        pixelsSet += l[1:len(l)-2].count('#')
    return pixelsSet
#-----------------------------------------------------------------------
# Image needs growing by 2 on each dimension prior to enhancement
def growImagePriorToAlgo(image,growth) :
    nWidth = len(image[0]) + 2 * growth
    outImage = ['.' * nWidth for y in range(growth+1)]
    for l in image :
        outImage.append('.' * growth + l + '.' * growth)
    outImage.extend(['.' * nWidth for y in range(growth+1)])
    return outImage
#-----------------------------------------------------------------------
def hashToBinary(hashString) :
    binString = hashString.replace('.','0').replace('#','1')
    #print(f"{hashString} -> {binString} -> {int(binString,2)}")
    return int(binString,2)
#-----------------------------------------------------------------------
#The algorithm uses a 3-by-3 matrix around the point
def getValueForPixel(image,x,y) :
    #A sub-function, no less:
    def getImgLine(line) :
        if x == 0 :
            return "." + line[0:1]
        elif x == len(line) :
            return line[-2:] + "."
        else :
            return line[x-1:x+2]
    #Returning to our regularly-scheduled programming:
    hashString=""
    if y == 0 :
        hashString += "..."
        for l in [0,1] :
            hashString += getImgLine(image[l])
    elif y == len(image) :
        for l in [y-1,y] :
            hashString += getImgLine(image[l])
            hashString += '...'
    else :
        for l in [y-1,y,y+1] :
            hashString += getImgLine(image[l])

    return hashToBinary(hashString)

#-----------------------------------------------------------------------
def enhanceImage(inImage, algoString) :
    outImage = []
    for y in range(len(inImage)-1) :
        outLine = ""
        for x in range(len(inImage[y])) :
            outLine += algoString[getValueForPixel(inImage,x,y)]
        outImage.append(outLine)
    return outImage

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    image,algo = readInputAlgoAndImage(infile)

    print(f"Algorithm is {len(algo)} chars long.")
    print(f"Image is {len(image[0])} pixels wide by {len(image)} pixels tall")

    for g in range(4,50,10) :
        enhanced=enhanceImage(growImagePriorToAlgo(image,g),algo)
        enhanced=enhanceImage(enhanced,algo)
        #drawImage(enhanced)
        print(f"for dimensions {len(enhanced[0])}x{len(enhanced)} the final set pixels is {countSetPixelsInImage(enhanced)}, this clips to {countClippedSetPixelsInImage(enhanced)}")
