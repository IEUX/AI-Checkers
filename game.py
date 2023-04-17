import os
import tkinter as tk
import numpy as np
import pandas as pd
import AIChecker
import random

class Damier(tk.Canvas):
    global df
    df = pd.DataFrame(columns=['player1', 'player2', 'winner'])
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
        self.height
        self.width
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
        # self.appendFD(df, case)
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
            damier.refreshMap()
            return 0
        return 1

    # GAMEPLAY     

    def turn(self, event):
        self.checkWin()
        # ADD AI TURN HERE
            
            
        # select player pion
        if self.state == 0:
            pionPostion = self.choosePion(event)
            if pionPostion == None:
                return
            self.lastPostion = pionPostion
            print(self.lastPostion)
            self.state = 1
            return
        # select next case
        if self.state == 1:
            self.pionMove(event)
            print(self.playerTurn)
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
                #END DEV
                #aiEvent = self.ai.chooseMove(possiblePick)
                
                for i in range(0,len(possiblePick)):
                    pick = self.ai.chooseMove(possiblePick[i])
                    pion = self.getCase(pick)
                    x = pion[0]
                    y = pion[1]
                    possibleMove[pion] = self.checkMovable(x,y)
                for key, value in possibleMove.items():
                    print("Pion : ",key,"\nPossible move : ",value)
                pion = self.ai.chooseMove(random.choice(list(possibleMove.keys())))
                positionPick = random.choice(possibleMove[self.getCase(pion)])
                pick = self.ai.chooseMove((positionPick[1],positionPick[0]))
                previousPosition = self.getCase(pion)
                self.lastPostion = (previousPosition[1],previousPosition[0])
                self.pionMove(pick)
    # change common pion to a dame (1 to 2 or -1 to -2)
    def checkMovable(self, x, y):
        possibleMoves = []
        if y != 0:
            if self.checkerBoard[x+-self.playerTurn,y-1] == 0:
                possibleMoves.append((x+-self.playerTurn,y-1))
        if y != 9:
            if self.checkerBoard[x+-self.playerTurn,y+1] == 0:
                possibleMoves.append((x+-self.playerTurn,y+1))
        if y > 1:
            if self.checkerBoard[x+-self.playerTurn*2,y-2] == 0 and self.checkerBoard[x+-self.playerTurn,y-1] == -self.playerTurn:
                possibleMoves.append((x+-self.playerTurn*2,y-2))
        if y < 8:
            if self.checkerBoard[x+-self.playerTurn*2,y+2] == 0 and self.checkerBoard[x+-self.playerTurn,y+1] == -self.playerTurn:
                possibleMoves.append((x+-self.playerTurn*2,y+2))  
        return possibleMoves     
     
    def checkDamier(self):
        for i in range(10):
            if self.checkerBoard[0][i] == 1:
                self.checkerBoard[0][i] = 2
            if self.checkerBoard[9][i] == -1:
                self.checkerBoard[9][i] = -2
        
    # WIN
    def checkWin(self):
        if -1 not in self.checkerBoard and -2 not in self.checkerBoard:
            return 1
        if 1 not in self.checkerBoard and 2 not in self.checkerBoard:
            return -1

    def printWinner(self):
        winner = self.checkWin()
        if winner == 1:
            # self.dfCSV(df)
            print("White pion win")
            self.restart()
        elif winner == -1:
            # self.dfCSV(df)
            print("Black pion win")
            self.restart()


    #create winner state
    def restart(self):
        pagWin = tk.Toplevel()
        pagWin.title("Winner")
        pagWin.geometry("200x100")
        pagWin.resizable(False, False)
        pagWin.configure(bg="white")
        winner = self.checkWin()
        if winner == 1:
            tk.Label(pagWin, text="White pion win", bg="white", fg="black").pack()
        elif winner == -1:
            tk.Label(pagWin, text="Black pion win", bg="white", fg="black").pack()

    def dft(self,case):
        if self.playerTurn == 1:
            df = pd.read_csv("data.csv")
            df = df.append({"p1t": case, "p2t": np.nan, "p1p": np.nan, "p2p": np.nan, "winner": np.nan}, ignore_index=True)
            df.to_csv("data.csv", index=False)
        else:
            df = pd.read_csv("data.csv")
            df = df.append({"p1t": np.nan, "p2t": case, "p1p": np.nan, "p2p": np.nan, "winner": np.nan}, ignore_index=True)
            df.to_csv("data.csv", index=False)


    def dfp(self,case):
        if self.playerTurn == 1:
            df = pd.read_csv("data.csv")
            df = df.append({"p1t": np.nan, "p2t": np.nan, "p1p": case, "p2p": np.nan, "winner": np.nan}, ignore_index=True)
            df.to_csv("data.csv", index=False)
        else:
            df = pd.read_csv("data.csv")
            df = df.append({"p1t": np.nan, "p2t": np.nan, "p1p": np.nan, "p2p": case, "winner": np.nan}, ignore_index=True)
            df.to_csv("data.csv", index=False)


    # DFcheckLeft

    # def appendFD(self,df,case):
    #     if self.playerTurn == 1:
    #         df = df.append({'player1' : case}, ignore_index=True)
    #         return df
    #     if self.playerTurn == -1:
    #         df = df.append({'player2' : case}, ignore_index=True)
    #         return df


    # put df in csv
    # def dfCSV(self,df):
    #     df.to_csv('data.csv', index=False)


















fenetre = tk.Tk()
damier = Damier(fenetre, 500, 500, "tan1", "tan4")
if not os.path.exists("data.csv"):
        df = pd.DataFrame(columns=["p1t", "p1p", "p2t", "p2p", "winner"])
        df.to_csv("data.csv", index=False)
damier.refreshMap()
damier.bind("<Button-1>", damier.turn)
fenetre.mainloop()
