import tkinter as tk
import numpy as np

class Damier(tk.Canvas):
    checkerBoard = np.zeros((10,10))
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
                    if j < 3:
                        self.create_oval(i*height/10,j*width/10,(i+1)*height/10,(j+1)*width/10,fill="black")
                        Damier.checkerBoard[j][i] = 1
                    elif j > 6:
                        self.create_oval(i*height/10,j*width/10,(i+1)*height/10,(j+1)*width/10,fill="white")
                        Damier.checkerBoard[j][i] = 2

        self.pack()


fenetre = tk.Tk()
Damier(fenetre,500,500,"tan1","tan4")
print(Damier.checkerBoard)
fenetre.mainloop()
