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

    def checkMoves(self,checkerBoard):
        Pions = []
        for i in range(0,9):
            for j in range(0,9):
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