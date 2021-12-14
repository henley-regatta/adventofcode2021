#!/usr/bin/python3
# Python solution for AOC 2021 Day 4, Part 1
# Play Bingo. Work out which board wins, and what the final score will
# be.
#
# Mainly an exercise in partsing, by the looks of it.

#inputfile="data/day4test.txt"
inputfile="data/day4part1.txt"

# ----------------------------------------------------------------------------
#Input parsing appears to be position dependent.
#Row 1 is the list of numbers called out, comma separated.
#There then follows a series of Bingo boards, separated by blank lines, each
#consisting of a series of 5 rows, each containing 5 blank-separated numbers.
def parseInputIntoBoardsAndNumbers(filename) :
    bingonumbers = [] # A simple array
    bingoboards = [] # Will become a 3 dimensional array - a list of 2-dimensional boards.

    #The input form is simple but using counters / sentinels is easiest to implement.
    haveNumbers=False
    currentBoard = [] # a work-in-progress board being built
    with open(filename,'r') as bingo:
        for line in bingo:
            line = line.strip()
            if not haveNumbers:
                numStr = line.split(',')
                for num in numStr:
                    bingonumbers.append(int(num))
                haveNumbers = True
                continue
            #What to do on a separator line
            if len(line)==0 :
                #If we've finished a board, store it and start again
                if len(currentBoard) > 0 :
                    bingoboards.append(currentBoard)
                    currentBoard = []
            else :
                blStr = line.split()
                if len(blStr) != 5 :
                    print(f"Error parsing bingo board line - should be 5 numbers, got: {boardLine}")
                else :
                    boardLine=[]
                    for num in blStr:
                        boardLine.append(int(num))
                    currentBoard.append(boardLine)
    #At the end we've got a board-in-progress which should be complete but needs plonking
    #on the list anyway
    if len(currentBoard) != 5 :
        print(f"Error - should have finished with a complete board in progress but have {currentBoard} instead")
    else :
        bingoboards.append(currentBoard)

    return { 'boards' : bingoboards, 'numbers' : bingonumbers }

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
if __name__ == "__main__" :
    bingo = parseInputIntoBoardsAndNumbers(inputfile)
    print(f"Read {len(bingo['boards'])} boards and {len(bingo['numbers'])} numbers")

    #Hypothesis: Each row,column has a unique sum across boards.
    #HYPOTHESIS DISPROVEN. Do it the hard way.
    bCount = len(bingo['boards'])
    rCount = len(bingo['boards'][0])
    cCount = len(bingo['boards'][0][0])

    boardRowSums = [[0 for i in range(rCount)] for j in range(bCount)]
    boardColSums = [[0 for i in range(cCount)] for j in range(bCount)]

    #Play bingo until we get a winner
    haveWinner = False
    usedBalls = []
    winningBoard = -1
    lastBallCalled = -1
    for ball in bingo['numbers'] :
        if not haveWinner :
            usedBalls.append(ball)
            for b in range(bCount) :
                if not haveWinner :
                    for r in range(rCount) :
                        if not haveWinner :
                            for c in range(cCount) :
                                if bingo['boards'][b][r][c] == ball :
                                    boardRowSums[b][r]+=1
                                    boardColSums[b][c]+=1
                                    if boardRowSums[b][r]==rCount or boardColSums[b][c]==cCount :
                                        haveWinner = True
                                        winningBoard=b
                                        lastBallCalled = ball
                                        break
    print(f"Board {winningBoard} called BINGO at ball {lastBallCalled} (after {len(usedBalls)} balls drawn)")
    #Now work out which numbers on the board were used and which were not.
    winningBoardNumbers=[]
    for r in range(rCount) :
        winningBoardNumbers += bingo['boards'][winningBoard][r]
    #Now calculate the sum of the unused numbers from the board
    unusedNumberSum=0
    for n in winningBoardNumbers :
        if n not in usedBalls :
            unusedNumberSum += n

    finalScore = unusedNumberSum * lastBallCalled
    print(f"Sum of unused numbers on board {winningBoard} is {unusedNumberSum}; final score is therefore {finalScore}")
