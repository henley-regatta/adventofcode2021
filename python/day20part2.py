#!/usr/bin/python3
# Python solution for AOC 2021 Day 20 Part 2
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

# PART 2 invalidates this assumption. Actual data has all-zeros mapping to all-ones
# and vice-versa. So growth is still 1 block at a time but the "filler" needs to be
# all zeros IF an even step, but all ones IF an odd step.

# Part 2: DO IT MOAR. 50 times in fact.

# ANSWER IS LESS THAN 28288
# IS NOT   20094
# IS NOT   11987 (grow 6 clip 5)
# MIGHT BE 19261
# MIGHT BE 18395 (grow 4, clip 1)



# There's a better way of doing this by growing by 6 each time and clipping
# the result. But... eh.

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
def clipImage(image,toClip) :
    outImage=[]
    for y in range(toClip,len(image)-(1+toClip)) :
        l=image[y]
        outImage.append(l[toClip:len(l)-(1+toClip)])
    return outImage
#-----------------------------------------------------------------------
def countClippedSetPixelsInImage(image) :
    return countSetPixelsInImage(clipImage(image,1))
#-----------------------------------------------------------------------
# Image needs growing by 2 on each dimension prior to enhancement
def growImagePriorToAlgo(image,growth,filler) :
    nWidth = len(image[0]) + (2 * growth)
    outImage = [filler * nWidth for y in range(growth)]
    for l in image :
        outImage.append(filler * growth + l + filler * growth)
    outImage.extend([filler * nWidth for y in range(growth)])
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
        glob=""
        if x == 0 :
            glob= "." + line[0:2]
        elif x == len(line)-1 :
            glob= line[-2:] + "."
        else :
            glob= line[x-1:x+2]
        if len(glob)!=3 :
            print(f"X for {x},{y} is borked: '{glob}'")
            exit()
        else :
            return glob
    #Returning to our regularly-scheduled programming:
    hashString=""
    if y == 0 :
        hashString += "..."
        for l in [0,1] :
            hashString += getImgLine(image[l])
    elif y == len(image)-1 :
        for l in [y-1,y] :
            hashString += getImgLine(image[l])
        hashString += '...'
    else :
        for l in [y-1,y,y+1] :
            hashString += getImgLine(image[l])

    if len(hashString) != 9 :
        print(f"Y for {x},{y} is borked: '{hashString}' ({len(hashString)})")
        exit()
    else :
        return hashToBinary(hashString)

#-----------------------------------------------------------------------
def enhanceImage(inImage, algoString) :
    outImage = []
    for y in range(0,len(inImage)) :
        outLine = ""
        for x in range(0,len(inImage[y])) :
            pVal = getValueForPixel(inImage,x,y)
            try:
                outLine += algoString[pVal]
            except IndexError :
                print(f"Pixel {x},{y} gives value {pVal} which is out of range")
                exit()
        outImage.append(outLine)
    return outImage

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    image,algo = readInputAlgoAndImage(infile)

    print(f"Algorithm is {len(algo)} chars long.")
    print(f"Source Image is {len(image[0])} pixels wide by {len(image)} pixels tall")

    for s in range(1,51) :
        if s%2==0 :
            filler='#'
        else :
            filler='.'
        image=clipImage(enhanceImage(growImagePriorToAlgo(image,3,filler),algo),1)
        print(f"Step {s}: Image is now {len(image[0])}x{len(image)}; {countSetPixelsInImage(image)} pixels are set")

    drawImage(image)
