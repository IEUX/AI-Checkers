import tkinter as tk
import numpy as np

class Damier(tk.Canvas):
    checkerBoard = np.zeros((10,10))
    playerTurn = -1
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
        print("clic")
        x = event.x
        y = event.y
        positions = self.createPosMap()
        for i in range(10):
            for j in range(10):
                if x > positions[i][j][0] and x < positions[i][j][1] and y > positions[i][j][2] and y < positions[i][j][3]:
                    return (i,j)

    def choosePion(self,event):
        case = self.getCase(event) 
        if self.checkerBoard[case[1]][case[0]] == self.playerTurn:
            return case 

    def pionMove(self,pionPostion):
        self.checkerBoard[pionPostion[1] + -self.playerTurn][pionPostion[0]] = self.playerTurn
            
            
    def turn(self,event):
        pionPostion = self.choosePion(event)
        if pionPostion == None:
            return  
        print(pionPostion)
        self.checkerBoard[pionPostion[1]][pionPostion[0]] = 0
        self.pionMove(pionPostion)
        self.playerTurn = -self.playerTurn
        damier.refreshMap()

fenetre = tk.Tk()
damier = Damier(fenetre,500,500,"tan1","tan4")
damier.refreshMap()
damier.bind("<Button-1>", damier.turn)
fenetre.mainloop()
