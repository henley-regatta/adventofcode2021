#!/usr/bin/python3
# Python solution for AOC 2021 Day 16, Part 2
#
# It's Packet Decoding Day!
#
# As might be expected, part 2 is forcing me to sort out my simplifications
# and treat the problem properly. Not going to make it with Glob manipulation
# this time.
#
# Well. It *does* seem that slowly consuming a (global) message string might
# work out OK....

#inputfile="data/day16test.txt"
inputfile="data/day16part1.txt"

hexLUT = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111'}

#A Global. Just one, though.
message=""

# ---------------------------------------------------------------
def readFileToBinary(file) :
    binMsgs = []
    with open(file,'r') as bits :
        for l in bits:
            m=l.strip()
            if len(m)>0 :
                binMsgs.append(hexToBin(m))
    return binMsgs
# ---------------------------------------------------------------
def hexToBin(msg) :
    binMsg=""
    for c in msg :
        binMsg += hexLUT[c]
    return binMsg
# ---------------------------------------------------------------
def consumeBits(nBits) :
    global message
    #print(f"\nconsume {nBits} from {message}:",end="")
    if message==None or len(message)<nBits :
        print(f"ERROR trying to consume {nBits} bits from {message} ({len(message)})")
        exit()
    v=message[:nBits]
    message=message[nBits:]
    #print(f"{v} remaining {message}")
    return v
# ---------------------------------------------------------------
# These are "typeID 4" messages
def decodeLiteralValue() :
    global message
    #The rules say the pkt must be a multiple of 5 bits long.
    #(1 bit hdr, 4 bits data). The Last chunk of the pkt has a 0 hdr
    #ANYTHING AFTER THAT SHOULD BE RETURNED FOR PROCESSING
    binNum=""
    while len(message)>4 :
        nibble=consumeBits(5)
        cont=nibble[0]
        binNum+=nibble[1:]
        if cont=="0" :
            print(f"literal: {int(binNum,2)}")
            return int(binNum,2)

# ---------------------------------------------------------------
# I suspect this will get recursive so it's best to assume we're
# always going to be working in Binary input.
def decodeMsg(d,single) :
    global message
    if message==None or len(message)<6 :
        #print(f"message corrupt/missing: {message}")
        return None
    ver=int(consumeBits(3),2)
    type=int(consumeBits(3),2)
    print("\n" + str(d) + "\t" * d,end=" ")
    print(f"({d})PACKET type: {type}: ",end="")
    if type == 4 : # WARNING: There is potentially a series of these one after the other.
        if single :
            return decodeLiteralValue()
        else :
            vals=[decodeLiteralValue()]
            while len(message)>10 :
                vals.append(decodeMsg(d+1,True))
            return vals
    else :
        #First consume the length-type header to work out *how*
        #to interpret the sub-packets:
        lID=int(consumeBits(1))
        subLength=-1
        numSubs=-1
        vals=[]
        if lID==0 :  #Single sub-packet, length is a 15-bit number
            # There will be a need to "stack push" the message and process
            # the submessage separately. implementing a message stack is laughable...
            subLength=int(consumeBits(15),2)
            subMessage=consumeBits(subLength)
            globsavemessage=message
            message=subMessage
            while message!=None and len(message)>0 :
                decode = decodeMsg(d+1,False)
                if isinstance(decode,list):
                    vals.extend(decode)
                elif isinstance(decode,int) :
                    vals.append(decode)
                else :
                    print(f"I'm in a world of pain: {decode} isa {type(decode)}")
                    exit()
            print(f"({d})SINGLE sub-packet, length {len(subMessage)}, vals={vals},",end="")
            message=globsavemessage
        else :   #a number of sub-packets, length is an 11-bit number
            numSubs=int(consumeBits(11),2)
            for i in range(numSubs) :
                vals.append(decodeMsg(d+1,True))
            print(f"({d})MULTI {numSubs} sub-packets, vals={vals},",end="")
        if type == 0 :
            sumVals=sum(vals)
            print(f"SUM: {sumVals}")
            return sumVals
        elif type == 1 :
            product=1
            for p in vals :
                product = product * p
            print(f"PRODUCT: {product}")
            return product
        elif type == 2 :
            minVal=min(vals)
            print(f"MIN: {minVal}")
            return minVal
        elif type == 3 :
            maxVal=max(vals)
            print(f"MAX: {maxVal}")
            return maxVal
        elif type == 5 :
            if len(vals)!=2 :
                print(f"ERROR decoding, GTR should have 2 vals, instead: {vals}")
                exit()
            res=0
            if vals[0] > vals[1] :
                res=1
            print("GTR: {res}")
            return res
        elif type == 6 :
            if len(vals)!=2 :
                print(f"ERROR decoding, LTA should have 2 vals, instead: {vals}")
                exit()
            res=0
            if vals[0] < vals[1] :
                res=1
            print("LTA: {res}")
            return res
        elif type == 7 :
            if len(vals)!=2 :
                print(f"ERROR decoding, EQU should have 2 vals, instead: {vals}")
                exit()
            res=0
            if vals[0] == vals[1] :
                    res=1
            print("EQU")
            return res
    return None

# ---------------------------------------------------------------
def testSuite() :
    #For part two, we need to do Maths based on Operators within the packets
    #and come up with a Number.
    global message
    msgs=[[3,"C200B40A82"],
        [54,"04005AC33890"],
        [7,"880086C3E88112"],
        [9,"CE00C43D881120"],
        [1,"D8005AC2A8F0"],
        [0,"F600BC2D8F"],
        [0,"9C005AC2F8F0"],
        [1,"9C0141080250320F1802104A08"]
    ]
    success=True
    for m in msgs :
        message=hexToBin(m[1])
        v= decodeMsg(0,False)
        if v != m[0] :
            success=False
            print(f"Test fail: msg {m[1]} result {v} !=  {m[0]}")
            break
        else :
            print(f"Test pass: msg {m[1]} result {v}  = {m[0]}")
    return success
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    if not testSuite() :
        print("Test Suite failed, aborting")
        exit()
    else :
        print("Test Suite Succeeded")

    msgs = readFileToBinary(inputfile)
    for msg in msgs :
        message=msg
        v = decodeMsg(0,False)
        print(f"The Part Two Answer You Seek Is: {v}")
