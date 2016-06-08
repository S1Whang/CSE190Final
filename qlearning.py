# qlearning implementation

from math import *
from read_config import read_config
from numpy import copy
from random import *
class qLearn():
  def __init__(self):
    self._printMap_()
    self._runRobot_()
  def _printMap_(self):
    c = read_config()
    self.robotpos = [['0' for x in range(c["map_size"][1])] for y in range(c["map_size"][0])]
    self.floormap = [['0' for x in range(c["map_size"][1])] for y in range(c["map_size"][0])]
    self.valuemap = [[[0.0,0.0,0.0,0.0] for x in range(c["map_size"][1])] for y in range(c["map_size"][0])]
    floor = []
    for i in range(c["map_size"][0]):
      pos = ""
      row = []
      for j in range(c["map_size"][1]):
         if [i,j] == c["start"]: 
           pos = 'S'
           self.floormap[i][j] = "S"
         elif [i,j] == c["goal"]: 
           pos = 'G'
           self.floormap[i][j] = "G"
           self.robotpos[i][j] = "G"
           self.valuemap[i][j] = c["reward_goal"]
         elif [i,j] in c["walls"]: 
           pos = 'W'
           self.floormap[i][j] = "W"
           self.robotpos[i][j] = "W"
           self.valuemap[i][j] = c["reward_wall"]
         elif [i,j] in c["pits"]: 
           pos = 'P'
           self.floormap[i][j] = "P"
           self.robotpos[i][j] = "P"
           self.valuemap[i][j] = c["reward_pits"]
         else: pos = '0'
         row.append(pos)
      floor.append(row)
    for i in self.valuemap: print i
  def _runRobot_(self):
    pospos = []
    for i in self.robotpos: print i
    for i in range(len(self.robotpos)):
      for j in range(len(self.robotpos[i])):
        if self.robotpos[i][j] == "G": pass
        elif self.robotpos[i][j] == "W": pass
        elif self.robotpos[i][j] == "P": pass
        else: pospos.append([i,j])
    # we have positions, now we need to iterate through each block depending on the starting position
    #for i in range(c["iterations"]):
    startpos = read_config()["start"]
    currentpos = startpos
    self.robotpos[startpos[0]][startpos[1]] = "R"
    alive = True
    j = 0
    c = read_config()
    print startpos
    for i in self.robotpos: print i 
    while alive == True:
      move = randint(0,3)
      print "move", move
      print "current", currentpos
      move = 2
      if move == 0: # move right
        self.robotpos[currentpos[0]][currentpos[1]] = "_"
        tempx = currentpos[0] + c["move_list"][0][0]
        tempy = currentpos[1] + c["move_list"][0][1]
        if tempx < 0: currentpos[0] = c["map_size"][0]-1
        elif tempx >= c["map_size"][0]: currentpos[0] = 0
        else: currentpos[0] = tempx
        if tempy < 0: currentpos[1] = c["map_size"][1]-1
        elif tempy >= c["map_size"][1]: currentpos[1] = 0
        else: currentpos[1] = tempy
        self.robotpos[currentpos[0]][currentpos[1]] = "R"
        j+= 1
        if self.floormap[currentpos[0]][currentpos[1]] == "G": alive = False
        if self.floormap[currentpos[0]][currentpos[1]] == "P": alive = False
        if j == 2: alive = False
      if move == 1: # move left
        currentpos[0] = currentpos[0] + c["move_list"][1][0]
        currentpos[1] = currentpos[1] + c["move_list"][1][1]
        print currentpos
        alive = False
      if move == 2: # move 
        # need to calculate before current pos changes
        self.robotpos[currentpos[0]][currentpos[1]] = "_"
        tempx = currentpos[0] + c["move_list"][2][0]
        tempy = currentpos[1] + c["move_list"][2][1]
        if tempx < 0: currentpos[0] = c["map)size"][2]-1
        elif tempx >= c["map_size"][0]: currentpos[0] = 0
        else: currentpos[0] = tempx
        self.robotpos[currentpos[0]][currentpos[1]] == "R"

        if self.floormap[currentpos[0]][currentpos[1]] == "G": alive = False
        print currentpos
        print tempx,tempy
        alive = False
      if move == 3:
        alive = False
    visited = set()
    # NSEW
    q = [(3,[1,4]),(3,[2,2]),(3,[5,0])]
    print self.valuemap[currentpos[0]][currentpos[1]]
    print max(q)
    print startpos
    print pospos
    print self._getNeighbors([0,0])
    print self._getNeighbors([1,0])
    #self._printValMap_()
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    '''
  # ascii representation of the current map -- inprogress
  def _printValMap_(self):
    length = read_config()["map_size"][0]
    height = read_config()["map_size"][1]
    for i in range(height):
      print ("+" + "-"*14)* length + "+" # horizontal borders
      print ("|" + " "*5 + '0.00' + " "*5) * length + "|"    
      print ("|" + " " + '0.00' + " "*4 + '0.00' + " ") * length + "|"
      print ("|" + " "*5 + '0.00' + " "*5) * length + "|"  
    print ("+" + "-"*14)* length + "+" # bottom borders
  # gets n,s,e,w positions of input position
  def _getNeighbors(self,pos,x=0,y=0):
    # get north neighbor[-1,0]
    n = self._checkValues(pos[0] - 1, pos[1])
    # get south neighbor[1, 0]
    s = self._checkValues(pos[0] + 1, pos[1])
    # get east neighbor [0, 1]
    e = self._checkValues(pos[0], pos[1] + 1)
    # get west neighbor [0,-1]
    w = self._checkValues(pos[0], pos[1] -1)
    return [n,s,e,w] 
  def _checkValues(self,x,y):
    # for the x value
    vx = 0
    vy = 0
    c = read_config()
    if x < 0: vx = c["map_size"][0]-1
    elif x >= c["map_size"][0]: vx = 0
    else: vx = x
    if y < 0: vy = c["map_size"][1]-1
    elif y >= c["map_size"][1]: vy = 0
    else: vy = y
    return [vx,vy]
  def _checkBounds(self,x,y):
    c = read_config()
    if x < 0 or x >= c["map_size"][0]: return False
    if y < 0 or y >= c["map_size"][0]: return False
    return True
  def _checkWall(self, x, y):
    if self.floormap[x][y] = "W": return True
    return False
  def getQValue(self, pos, direction):
    return self.valuemap[pos[0]
def printing(maps):
if __name__ == "__main__":
  calc = qLearn()
  printing()
