import os
import tkinter as tk
import numpy as np
import pandas as pd
import AIChecker
import random
import warnings



class Damier(tk.Canvas):
    if not os.path.exists("data.csv"):
        df = pd.DataFrame(columns=["Player", "AI"])
        df.to_csv("data.csv", index=False)
    else:   
        df = pd.DataFrame(columns=["Player", "AI"])
    checkerBoard = np.zeros((10, 10))
    playerTurn = 1
    state = 0
    lastPostion = None
    
    def __init__(self, parent, height, width, color1, color2):
        # attributs
        self.parent = parent
        self.color1 = color1
        self.color2 = color2
        self.height = height
        self.width = width
        self.ai = AIChecker.AI(-1, self.createPosMap())
        # tkinter  
        tk.Canvas.__init__(self, parent, height=height, width=width, bg=color1)
        for i in range(10):
            for j in range(10):
                if (i + j) % 2 == 0:
                    self.create_rectangle(i * height / 10, j * width / 10, (i + 1) * height / 10, (j + 1) * width / 10,
                                          fill=color1)
                else:
                    self.create_rectangle(i * height / 10, j * width / 10, (i + 1) * height / 10, (j + 1) * width / 10,
                                          fill=color2)
                    if j < 4:
                        Damier.checkerBoard[j][i] = -1
                    elif j > 5:
                        Damier.checkerBoard[j][i] = 1
        self.pack()

    # UTILS
    def createPosMap(self):
        positions = []
        for i in range(10):
            position = []
            for j in range(10):
                (yMin, yMax, xMin, xMax) = (
                    i * self.height / 10, (i + 1) * self.width / 10, j * self.height / 10, (j + 1) * self.width / 10)
                position.append((yMin, yMax, xMin, xMax))
            positions.append(position)
        return positions

    def refreshMap(self):
        for i in range(10):
            for j in range(10):
                if (i + j) % 2 == 0:
                    self.create_rectangle(i * self.height / 10, j * self.width / 10, (i + 1) * self.height / 10,
                                          (j + 1) * self.width / 10, fill=self.color1)
                else:
                    self.create_rectangle(i * self.height / 10, j * self.width / 10, (i + 1) * self.height / 10,
                                          (j + 1) * self.width / 10, fill=self.color2)
                if self.checkerBoard[j][i] == -1:
                    self.create_oval(i * self.height / 10, j * self.width / 10, (i + 1) * self.height / 10,
                                     (j + 1) * self.width / 10, fill="black")
                if self.checkerBoard[j][i] == 1:
                    self.create_oval(i * self.height / 10, j * self.width / 10, (i + 1) * self.height / 10,
                                     (j + 1) * self.width / 10, fill="white")

    def getCase(self, event):
        x = event.x
        y = event.y
        positions = self.createPosMap()
        for i in range(10):
            for j in range(10):
                if x > positions[i][j][0] and x <= positions[i][j][1] and y > positions[i][j][2] and y <= \
                        positions[i][j][3]:
                    return (i, j)

    # MOVEMENTS
    # Check  if I can choose this pion
    def choosePion(self, event):
        case = self.getCase(event)
        y = case[1]
        x = case[0]
        if self.checkerBoard[y][x] == self.playerTurn:
            if x == 0:
                if self.checkRight(y, x):
                    # change the color of the pion chosen
                    self.create_oval(case[0] * self.height / 10, case[1] * self.width / 10,
                                     (case[0] + 1) * self.height / 10, (case[1] + 1) * self.width / 10, fill="red")
                    return case
                return None
            if x == 9:
                if self.checkLeft(y, x):
                    # change the color of the pion chosen
                    self.create_oval(case[0] * self.height / 10, case[1] * self.width / 10,
                                     (case[0] + 1) * self.height / 10, (case[1] + 1) * self.width / 10, fill="red")
                    return case
                return None
            if self.checkLeft(y, x) or self.checkRight(y, x):
                # change the color of the pion chosen
                self.create_oval(case[0] * self.height / 10, case[1] * self.width / 10,
                                 (case[0] + 1) * self.height / 10, (case[1] + 1) * self.width / 10, fill="red")
                return case
        return None

    def checkLeft(self, x, y):            
        if self.checkerBoard[x + -self.playerTurn, y - 1] == 0:
            return True
        if y-2 > 0:
            if self.checkerBoard[x + -self.playerTurn, y - 1] == -self.playerTurn and self.checkerBoard[x + 2 * -self.playerTurn, y - 2] == 0:
                return True
        return False

    def checkRight(self, x, y):
        if self.checkerBoard[x + -self.playerTurn, y + 1] == 0:
            return True
        if y+2 < 9:
            if self.checkerBoard[x + -self.playerTurn, y + 1] == -self.playerTurn and self.checkerBoard[x + 2 * -self.playerTurn, y + 2] == 0:
                return True
        return False

    def moveLeft(self, x, y):
        if self.checkerBoard[x, y] == 0 and self.lastPostion[0] - 1 == y and self.lastPostion[
            1] + -self.playerTurn == x:
            return True
        return False

    def moveRight(self, x, y):
        if self.checkerBoard[x, y] == 0 and self.lastPostion[0] + 1 == y and self.lastPostion[
            1] + -self.playerTurn == x:
            return True
        return False

    def takeLeft(self, x, y):
        if self.lastPostion[0] - 2 == y and self.lastPostion[
            1] + -2 * self.playerTurn == x and self.checkerBoard[x,y] == 0 and self.checkerBoard[
            self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] - 1] == -self.playerTurn:
            return True
        return False

    def takeRight(self, x, y):
        if self.lastPostion[0] + 2 == y and self.lastPostion[1] + -2 * self.playerTurn == x and self.checkerBoard[x,y] == 0 and self.checkerBoard[self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] + 1] == -self.playerTurn:
            return True
        return False

    def chooseCase(self, event):
        case = self.getCase(event)
        y = case[1]
        x = case[0]
        if self.moveLeft(y, x):
            self.checkerBoard[y][x] = self.playerTurn
            return True
        if self.moveRight(y, x):
            self.checkerBoard[y][x] = self.playerTurn
            return True
        if self.takeLeft(y, x):
            self.checkerBoard[y][x] = self.playerTurn
            self.checkerBoard[self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] - 1] = 0
            return True
        if self.takeRight(y, x):
            self.checkerBoard[y][x] = self.playerTurn
            self.checkerBoard[self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] + 1] = 0
            return True
        return False
    
    def checkCase(self, case):
        x = case[1]
        y = case[0]
        print(x, y)
        if self.moveLeft(y, x):
            return True
        if self.moveRight(y, x):
            return True
        if self.takeLeft(y, x):
            return True
        if self.takeRight(y, x):
            return True
        return False

    def pionMove(self, event):
        if self.chooseCase(event):
            self.refreshMap()
            self.state = 0
            self.playerTurn = -self.playerTurn
            self.checkerBoard[self.lastPostion[1]][self.lastPostion[0]] = 0
            self.removePion()
            self.refreshMap()
            self.checkWin()
            return 0
        return 1

    # GAMEPLAY     

    def turn(self, event):
        # ADD AI TURN HERE
        # select player pion
        if self.state == 0:
            pionPostion = self.choosePion(event)
            if pionPostion == None:
                return
            self.lastPostion = pionPostion
            self.state = 1
            return
        # select next case
        if self.state == 1:
            self.pionMove(event)
            print(event)
            print(self.playerTurn)
            pPtake = self.lastPostion
            pPpose = (self.getCase(event))
            self.checkWin()
            #AITurn
            if self.playerTurn == -1:
                # DEV AI
                Pions = self.ai.checkMoves(self.checkerBoard)
                possiblePick = []
                possibleMove = {}
                for i in range(0,len(Pions)):  
                    pionPosition = Pions[i]
                    x = pionPosition[0]
                    y = pionPosition[1]
                    if y == 0:
                        if self.checkRight(x,y):
                            possiblePick.append([x,y])
                        continue
                    if y == 9:
                        if self.checkLeft(x,y):
                            possiblePick.append([x,y])
                        continue
                    if self.checkLeft(x,y) or self.checkRight(x,y):
                        possiblePick.append([x,y])
                for i in range(0,len(possiblePick)):
                    pick = self.ai.chooseMove(possiblePick[i])
                    pion = self.getCase(pick)
                    x = pion[0]
                    y = pion[1]
                    possibleMove[pion] = self.checkMovable(x,y)
                possibleMove = self.ai.evaluateMoves(possibleMove,self.checkerBoard)
                bestMove = self.ai.pickBestMove(possibleMove)
                print("Possible Moves:")
                for key, value in possibleMove.items():
                    print(" ")
                    print(f"↳ [Pion: {key}]")
                    for i in range(0,len(value)):
                        print(f"  Move: {value[i][0]} Points: {value[i][1]}")
                print("")     
                print(f"Best Move: {bestMove[0]} ⎇  {bestMove[1][0]} Points: {bestMove[1][1]}")
                pion = self.ai.chooseMove(random.choice(list(possibleMove.keys())))
                positionPick = bestMove[1]
                pick = self.ai.chooseMove((positionPick[0][1],positionPick[0][0]))
                previousPosition = bestMove[0]
                self.lastPostion = (previousPosition[1],previousPosition[0])
                self.pionMove(pick)
                pAItake = self.lastPostion
                pAIpose = self.getCase(pick)
                self.dfadppend(pPtake,pPpose,pAItake,pAIpose)

    def checkMovable(self, x, y):
        possibleMoves = []
        if y != 0:
            if self.checkerBoard[x+-self.playerTurn,y-1] == 0:
                possibleMoves.append([(x+-self.playerTurn,y-1),0])
        if y != 9:
            if self.checkerBoard[x+-self.playerTurn,y+1] == 0:
                possibleMoves.append([(x+-self.playerTurn,y+1),0])
        if x < 8:
            if y > 1:
                if self.checkerBoard[x+-self.playerTurn*2,y-2] == 0 and self.checkerBoard[x+-self.playerTurn,y-1] == -self.playerTurn:
                    possibleMoves.append([(x+-self.playerTurn*2,y-2),0])
            if y < 8:
                if self.checkerBoard[x+-self.playerTurn*2,y+2] == 0 and self.checkerBoard[x+-self.playerTurn,y+1] == -self.playerTurn:
                    possibleMoves.append([(x+-self.playerTurn*2,y+2),0])
        return possibleMoves     
     
    def removePion(self):
        for i in range(10):
            if self.checkerBoard[0][i] == 1:
                self.checkerBoard[0][i] = 0
            if self.checkerBoard[9][i] == -1:
                self.checkerBoard[9][i] = 0
        
    # WIN
    def checkWin(self):
        if -1 not in self.checkerBoard:
            self.win = 1
            self.df_CSV()
            self.printWinner(self.win)
            exit(0)
        if 1 not in self.checkerBoard:
            self.win = -1
            self.df_CSV()
            self.printWinner(self.win)
            exit(0)

    def printWinner(self,win):
        if win == 1:
            print("White pion win")
        elif win == -1:
            print("Black pion win")

    def dfadppend(self,pPtake,pPpose ,pAItake, pAIpose):
        tuple1 = (pPtake, pPpose)
        tuple2 = (pAItake, pAIpose)
        df = self.df.append({"Player": tuple1, "AI": tuple2}, ignore_index=True)
        self.df = df

    def df_CSV(self):
        if self.win == 1:
            self.winn = "White pion win"
        elif self.win == -1:
            self.winn = "Black pion win"

        data = pd.read_csv("data.csv")
        data.insert(0, "Player", self.df["Player"], True)
        data.insert(1, "AI", self.df["AI"], True)
        data.insert(2, "Winner", self.winn, True)

        data.to_csv("data.csv", index=False)



warnings.filterwarnings("ignore")
fenetre = tk.Tk()
damier = Damier(fenetre, 500, 500, "tan1", "tan4")
damier.refreshMap()
damier.bind("<Button-1>", damier.turn)
fenetre.mainloop()
