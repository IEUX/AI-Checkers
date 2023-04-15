import random
import numpy as np


class AI:
    def __init__(self,color,posMap) -> None:
        self.color = color
        self.posMap = posMap
    def chooseMove(self):
        postions = random.choice(random.choice(self.posMap))
        x = (postions[0] + postions[1])/2
        y = (postions[2] + postions[3])/2
        return CustomEvent(x,y)
    
class CustomEvent:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y