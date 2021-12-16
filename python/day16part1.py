#!/usr/bin/python3
# Python solution for AOC 2021 Day 16, Part 1
#
# It's Packet Decoding Day!
#

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

binToDec = {
    '000' : 0,
    '001' : 1,
    '010' : 2,
    '011' : 3,
    '100' : 4,
    '101' : 5,
    '110' : 6,
    '111' : 7
}

#This is horrible, really. I should be ashamed of myself:
msgVersionNumbers=[]

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
def getPacketHdr(msg) :
    if len(msg)<6 :
        print(f"Invalid packet cannot extract header: {msg}")
        exit()
    hdr=msg[0:6]
    ver=binToDec[hdr[0:3]]
    type=binToDec[hdr[3:6]]
    return([ver,type,msg[6::]])

# ---------------------------------------------------------------
# These are "typeID 4" messages
def decodeLiteralValue(pkt) :
    #The rules say the pkt must be a multiple of 5 bits long.
    #(1 bit hdr, 4 bits data). The Last chunk of the pkt has a 0 hdr
    #ANYTHING AFTER THAT SHOULD BE RETURNED FOR PROCESSING
    remPkt=pkt
    binNum=""
    while len(remPkt)>0 :
        nibble=remPkt[0:5]
        remPkt=remPkt[5:]
        cont=nibble[0]
        binNum+=nibble[1:]
        if cont=="0" :
            num=int(binNum,2)
            return [num,remPkt]

# ---------------------------------------------------------------
# sub-packet identification
def expandSubPackets(pkt) :
    lengthID=pkt[0]
    if lengthID=="0" :
        #ONE sub-packet is defined with a trailing tail to be processed., 15 bit number
        subPktLength=pkt[1:16]
        sPL=int(subPktLength,2)
        subP = pkt[16:16+sPL]
        remain=pkt[16+sPL:]
        print(f"mode0 subpacket length: {sPL}, val: {subP}")
        while len(subP)>0 :
            subP=decodeMsg(subP)
        return remain
    else : # Length type "1", define the number of sub-packets not their length, 15 bit number
        numSubPkts=pkt[1:12]
        subP=pkt[12:]
        nSP=int(numSubPkts,2)
        print(f"mode1 number of subpackets: {nSP} ({numSubPkts})")
        #print(f"decode {numSubPkts} {nSP} sub-packets")
        for i in range(1,nSP+1) :
            print(f"sub-packet {i} from {subP}")
            subP=decodeMsg(subP)
        return subP


# ---------------------------------------------------------------
# I suspect this will get recursive so it's best to assume we're
# always going to be working in Binary input.
def decodeMsg(msg) :
    global msgVersionNumbers
    if msg==None or len(msg)<6 :
        #doesn't contain a header, might be a trailing padding.
        print(f"{msg} is not a packet")
        return ""
    ver,type,pkt = getPacketHdr(msg)
    msgVersionNumbers.append(ver)
    print(f"ver: {ver} type: {type} packet: {pkt}")
    if type == 4 :
        val,pkt = decodeLiteralValue(pkt)
        #packetValues.append(val)
        return pkt
    #This will get expanded in Part 2 no doubt. For now we just
    #need to follow the "expansion rules"
    else :
        return expandSubPackets(pkt)

# ---------------------------------------------------------------
def testSuite() :
    global msgVersionNumbers
    #For part one the check value is the SUM of packet versions in the message:
    #msgs=["D2FE28","8A004A801A8002F478","620080001611562C8802118E34","C0015000016115A2E0802F182340","A0016C880162017C3686B18A3D4780"]
    msgs=[[6,"D2FE28"],
          [9,"38006F45291200"],
          [14,"EE00D40C823060"],
          [16,"8A004A801A8002F478"],
          [12,"620080001611562C8802118E34"],
          [23,"C0015000016115A2E0802F182340"],
          [31,"A0016C880162017C3686B18A3D4780"],
         ]
    success=True
    for m in msgs :
        msgVersionNumbers=[]
        decodeMsg(hexToBin(m[1]))
        v = sum(msgVersionNumbers)
        #print(f"{m[1]} -> {v} : ", end="")
        if v != m[0] :
            success=False
            print(f"Failed Test msg {m[1]} should be {m[0]} calc as {m[1]}")
            break
    return success
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------
if __name__ == "__main__" :
    if not testSuite() :
        print("Test Suite failed, aborting")
        exit()

    msgs = readFileToBinary(inputfile)
    partOneMessageVersionNumbers=0
    for msg in msgs :
        msgVersionNumbers=[] #resetting a glob here...for shame
        decodeMsg(msg)
        partOneMessageVersionNumbers += sum(msgVersionNumbers)

    print(f"Sum of Version Numbers Across All Messages (Part One Answer): {partOneMessageVersionNumbers}")
