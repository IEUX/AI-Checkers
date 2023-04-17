import random
import numpy as np


class AI:
    def __init__(self,color,posMap) -> None:
        self.color = color
        self.posMap = posMap
    def chooseMove(self,pick):
        postions = self.posMap[pick[0]][pick[1]] 

        x = (postions[0] + postions[1])/2
        y = (postions[2] + postions[3])/2
        return CustomEvent(x,y)

    def evaluateMoves(self,possibleMoves,currentBoard):
        for key,value in possibleMoves.items():
            for i in range(0,len(value)):
                points = 0
                position = value[i][0]
                # Don't touch the back line
                if key[0] != 0:
                    points += 2
                #Take if possible
                if (position[0] - 2,position[1] - 2) == key or (position[0] - 2,position[1] + 2) == key or (position[0] + 2,position[1] + 2) == key or (position[0] + 2,position[1] - 2) == key:
                    points += 4
                if position[0] - 2 >= 0 and position[1] - 2 >= 0 and position[0] + 2 <= 8 and position[1] + 2 <= 8:
                    #Get closer to another take
                    if currentBoard[position[0]-1][position[1]-1] == 1:
                        points += 1
                    if currentBoard[position[0]-1][position[1]+1] == 1:
                        points += 1
                    #Stay close
                    if currentBoard[position[0]+1][position[1]-1] == 0:
                        points += 1
                    if currentBoard[position[0]+1][position[1]+1] == 0:
                        points += 1
                    if currentBoard[position[0]-1][position[1]+1] == 0:
                        points += 1
                    if currentBoard[position[0]-1][position[1]-1] == 0:
                        points += 1
                #Get closer to middle
                if key[1] < 5 and position[1] > key[1]:
                    points += 1
                if key[1] > 5 and position[1] < key[1]:
                    points += 1
                if key[0] > 5 and position[0] < key[0]:
                    points += 1
                if key[0] < 5 and position[0] > key[0]:
                    points += 1
                possibleMoves[key][i][1] = points
        return possibleMoves

    def pickBestMove(self,possibleMoves):
        bestMove = 0
        bestMoves = []
        for key,value in possibleMoves.items():
            for i in range(0,len(value)):
                if value[i][1] > bestMove:
                    bestMoves = []
                    bestMove = value[i][1]
                    bestMoves.append((key,value[i]))
                if value[i][1] == bestMove:
                    bestMoves.append((key,value[i]))
        if len(bestMoves) > 1:
            move = random.choice(bestMoves)
            return move
        return bestMoves[0]
        
    def checkMoves(self,checkerBoard):
        Pions = []
        for i in range(0,10):
            for j in range(0,10):
                if checkerBoard[i][j] == self.color:
                    Pions.append([i,j])
        return Pions
    
    def checkPickablePion(self,checkerBoard):
        Pions = self.checkMoves(checkerBoard)
        possibleMoves = []
        for i in range(0,len(Pions)):
            possibleMoves.append(self.checkPosibleMoves(checkerBoard,Pions[i]))
        return possibleMoves

class CustomEvent:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y