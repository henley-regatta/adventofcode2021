#!/usr/bin/python3
# Python solution for AOC 2021 Day 15, Part 1
# Given an input "Risk Map" compute the lowest-risk path from top left (0,0)
# to bottom right (maxX,maxY).
# Moves may not be made diagonally.
# Route risk is computed as the sum of the risk values entered on the path.

#inputfile = "data/day15test.txt"
inputfile = "data/day15part1.txt"

#Globals All The Way
map=[]
maxX=0
maxY=0
#-----------------------------------------------------------------------
def loadMap(file) :
    map=[]
    with open(file,'r') as maplines :
        for l in maplines:
            c=l.strip()
            if len(c)>0 :
                map.append(c)
    return map
#-----------------------------------------------------------------------
def calcNavScores() :
    global costFromScores
    for y in range(maxY,-1,-1) :
        for x in range(maxX,-1,-1) :
            #We always have a cost to enter the square EXCEPT the origin:
            if x>0 or y>0 :
                costFromScores[y][x]=int(map[y][x])
            #Our cost from this square on depends...
            if x==maxX and y==maxY :
                print("(terminal)")
            elif x==maxX :
                #Cost adds score from below:
                costFromScores[y][x] += costFromScores[y+1][x]
            elif y==maxY :
                #Cost adds scores from right:
                costFromScores[y][x] += costFromScores[y][x+1]
            else :
                #Cost adds MINIMUM of either option:
                costFromScores[y][x] += min([costFromScores[y+1][x],costFromScores[y][x+1]])
                #Score is only the cost to enter this terminal
            #print(f"({x},{y})={costFromScores[y][x]}")

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
if __name__ == "__main__" :
    map=loadMap(inputfile)
    maxX=len(map[0])-1
    maxY=len(map[1])-1
    print(f"map is of size {maxX+1} x {maxY+1}")
    costFromScores=[[0 for x in range(len(map[0]))] for y in range(len(map))]
    calcNavScores()
    print(f"Minimum cost route to exit costs {costFromScores[0][0]}")
