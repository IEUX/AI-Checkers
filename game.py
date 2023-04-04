import tkinter as tk
import numpy as np

class Damier(tk.Canvas):
    checkerBoard = np.zeros((10,10))
    playerTurn = 1
    state = 0
    lastPostion = None
    def __init__(self,parent, height, width,color1,color2):
        # attributs
        self.parent = parent
        self.color1 = color1
        self.color2 = color2
        self.height = height
        self.width = width
        # tkinter  
        tk.Canvas.__init__(self,parent, height=height, width=width, bg=color1)
        for i in range(10):
            for j in range(10):
                if (i+j)%2 == 0:
                    self.create_rectangle(i*height/10,j*width/10,(i+1)*height/10,(j+1)*width/10,fill=color1)
                else:
                    self.create_rectangle(i*height/10,j*width/10,(i+1)*height/10,(j+1)*width/10,fill=color2)
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
                (yMin,yMax,xMin,xMax) = (i*self.height/10,(i+1)*self.width/10,j*self.height/10,(j+1)*self.width/10)
                position.append((yMin,yMax,xMin,xMax))
            positions.append(position)
        return positions

    def refreshMap(self):
        for i in range(10):
            for j in range(10):
                if (i+j)%2 == 0:
                    self.create_rectangle(i*self.height/10,j*self.width/10,(i+1)*self.height/10,(j+1)*self.width/10,fill=self.color1)
                else:
                    self.create_rectangle(i*self.height/10,j*self.width/10,(i+1)*self.height/10,(j+1)*self.width/10,fill=self.color2)
                if self.checkerBoard[j][i] == -1:
                    self.create_oval(i*self.height/10,j*self.width/10,(i+1)*self.height/10,(j+1)*self.width/10,fill="black")
                if self.checkerBoard[j][i] == 1:
                    self.create_oval(i*self.height/10,j*self.width/10,(i+1)*self.height/10,(j+1)*self.width/10,fill="white")

    def getCase(self,event):
        x = event.x
        y = event.y
        positions = self.createPosMap()
        for i in range(10):
            for j in range(10):
                if x > positions[i][j][0] and x <= positions[i][j][1] and y > positions[i][j][2] and y <= positions[i][j][3]:
                    return (i,j)
    
    # MOVEMENTS

    def choosePion(self,event):
        case = self.getCase(event) 
        x = case[1]
        y = case[0]
        if self.checkerBoard[x][y] == self.playerTurn:
            if x == 0:
                if self.checkRight(x,y):
                    return case
            if x == 9:
                if self.checkLeft(x,y):
                    return case
            if self.checkLeft(x,y) or self.checkRight(x,y):
                return case
        return None
    
    def checkLeft(self,x,y):
        if self.checkerBoard[x + -self.playerTurn, y - 1] != self.playerTurn:
            return True
        return False

    def checkRight(self,x,y):
        if self.checkerBoard[x + -self.playerTurn, y + 1] != self.playerTurn:
            return True
        return False
    
    def moveLeft(self,x,y):
        if self.checkerBoard[x,y] == 0 and self.lastPostion[0] - 1 == y and self.lastPostion[1] + -self.playerTurn == x:
            return True
        return False
    
    def moveRight(self,x,y):
        if self.checkerBoard[x,y] == 0 and self.lastPostion[0] + 1 == y and self.lastPostion[1] + -self.playerTurn == x:
            return True
        return False
    
    def takeLeft(self,x,y):
        if self.checkerBoard[x,y] == 0 and self.lastPostion[0] - 2 == y and self.lastPostion[1] + -2*self.playerTurn == x:
            return True
        return False
    
    def takeRight(self,x,y):
        if self.checkerBoard[x,y] == 0 and self.lastPostion[0] + 2 == y and self.lastPostion[1] + -2*self.playerTurn == x:
            return True
        return False
    

    def chooseCase(self,event):
        case = self.getCase(event)
        x = case[1]
        y = case[0]
        if self.moveLeft(x,y): 
            self.checkerBoard[x][y] = self.playerTurn
            return True
        if self.moveRight(x,y):
            self.checkerBoard[x][y] = self.playerTurn
            return True
        if self.takeLeft(x,y):
            self.checkerBoard[x][y] = self.playerTurn
            print(self.lastPostion)
            self.checkerBoard[self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] - 1] = 0
            return True
        if self.takeRight(x,y):
            self.checkerBoard[x][y] = self.playerTurn
            self.checkerBoard[self.lastPostion[1] + -self.playerTurn, self.lastPostion[0] + 1] = 0
            return True
        return False
        

    def pionMove(self,event):
        if self.chooseCase(event):
            self.refreshMap()
            self.state = 0
            self.playerTurn = -self.playerTurn
            self.checkerBoard[self.lastPostion[1]][self.lastPostion[0]] = 0
            damier.refreshMap()
        return

    # GAMEPLAY     

    def turn(self,event):
        # select pion
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
            print(self.playerTurn)

fenetre = tk.Tk()
damier = Damier(fenetre,500,500,"tan1","tan4")
damier.refreshMap()
damier.bind("<Button-1>", damier.turn)
fenetre.mainloop()
