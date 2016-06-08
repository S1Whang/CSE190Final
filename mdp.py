# mdp implementation needs to go here

from math import *
from read_config import read_config, read_config_mdp
from numpy import copy
class MDP():

  def __init__(self):
    c = read_config_mdp()
    self.movelist   = c["move_list"]
    self.mapsize    = c["map_size"]
    self.start      = c["start"]
    self.goal       = c["goal"]
    self.walls      = c["walls"]
    self.pits       = c["pits"]
    self.stepRew    = c["reward_for_each_step"]
    self.wallRew    = c["reward_for_hitting_wall"]
    self.goalRew    = c["reward_for_reaching_goal"]
    self.pitsRew    = c["reward_for_falling_in_pit"]*2
    self.discount   = c["discount_factor"]
    self.forward    = c["prob_move_forward"]
    self.left       = c["prob_move_left"]
    self.right      = c["prob_move_right"]
    self.backward   = c["prob_move_backward"]
    self.iterations = c["max_iterations"]
    self.iteratemap = []
    self.pmaps      = []
    self.threshDiff = c["threshold_difference"]
    self.visited    = set()
    self.cmaps      = []
    self.run = 100
    self.makeMap()
    self.current = 0
    for i in range(self.run-1):
      self.current += 1
      self.traverse()
  def getPolicy(self):
    curmap = []
    for i in range(len(self.pmaps[self.current-1])):
      row = self.pmaps[self.current-1][i]
      for j in range(len(row)):
        curmap.append(str(row[j].strip()))
    return curmap 
  def makeMap(self):
    totalcostmap = [[0.0 for x in range(self.mapsize[1])] for y in range(self.mapsize[0])]
    policymap    = [["    " for y in range(self.mapsize[1])] for x in range(self.mapsize[0])]

    totalcostmap[self.goal[0]][self.goal[1]] = self.goalRew
    policymap[self.goal[0]][self.goal[1]]    = "GOAL"

    for i in range(len(self.pits)):
      pitx,pity                  = self.pits[i]
      totalcostmap[pitx][pity]   = self.pitsRew
      policymap[pitx][pity]      = "PIT "

    for i in range(len(self.walls)):
      wallx,wally                = self.walls[i]
      totalcostmap[wallx][wally] = self.wallRew
      policymap[wallx][wally]    = "WALL"

    self.pmaps = [copy(policymap) for x in xrange(self.run)]
    self.cmaps = [copy(totalcostmap) for x in xrange(self.run)]
  
  def printMap(self):
    for i in self.pmaps[self.current]:
      string = ""
      for j in i: string += j
      print(string)
    #for i in self.cmaps[self.current]: print(i)
  def getMap(self):
    return self.pmaps[self.current]
  def getPos(self,x,y):
    W = [x,y-1]
    E = [x,y+1]
    N = [x-1,y]
    S = [x+1,y]
    return [W,E,N,S]

  def getVals(self,x,y):
    directs = self.getPos(x,y)
    vals = []
    directs.append([x,y])  
    for i in directs:
      if self.checkNeighbors(i[0],i[1]):
        if self.pmaps[self.current-1][i[0]][i[1]] == "GOAL":
          vals.append([self.goalRew*self.discount+self.stepRew,"GOAL"])
        elif self.pmaps[self.current-1][i[0]][i[1]] == "PIT ":
          vals.append([self.pitsRew*self.discount+self.stepRew,"PIT"])
        elif self.pmaps[self.current-1][i[0]][i[1]] == "WALL":
          vals.append([self.wallRew+self.discount*self.cmaps[self.current-1][x][y],"WALL"])
        else: vals.append([self.cmaps[self.current-1][i[0]][i[1]]+self.stepRew,"TILE"])
      else: vals.append([self.wallRew+self.discount*self.cmaps[self.current-1][x][y],"WALL"])
    
    prob = []
    R = vals[1][0]*.8 + vals[2][0]*.1 + vals[3][0]*.1
    L = vals[0][0]*.8 + vals[2][0]*.1 + vals[3][0]*.1 
    U = vals[2][0]*.8 + vals[0][0]*.1 + vals[1][0]*.1
    D = vals[3][0]*.8 + vals[0][0]*.1 + vals[1][0]*.1
    prob = [[L," W  "],[R," E  "],[U," N  "],[D," S  "]]
    
    self.cmaps[self.current][x][y] = float("{0:.2f}".format(max(prob)[0]))
    self.pmaps[self.current][x][y] = max(prob)[1]
    return vals
  
  def traverse(self):
    visited = set()
    frontier = []
    frontier.append(tuple(self.goal))
    while len(frontier) > 0:
      x,y = frontier.pop(0)
      visited.add(tuple([x,y]))
      if self.pmaps[self.current-1][x][y] == "GOAL": pass
      elif self.pmaps[self.current-1][x][y] == "PIT ": pass
      elif self.pmaps[self.current-1][x][y] == "WALL": pass
      else: self.getVals(x,y)
      coord = self.getNeighbors(x,y)

      for i in coord:
        if i != [None,None] and tuple(i) not in visited and tuple(i) not in frontier:
          frontier.append(tuple([i[0],i[1]]))

  def checkNeighbors(self,x,y):
    if x < 0 or x >= self.mapsize[0]: return False
    if y < 0 or y >= self.mapsize[1]: return False
    return True
  
  def checkWall(self,x,y):
    if self.pmaps[self.current-1][x][y] == "WALL": return True
    return False
  
  def getNeighbors(self,x,y):
    if self.checkNeighbors(x-1,y): 
      if not self.checkWall(x-1,y): W = [x-1,y]
      else: W = [None,None]
    else: W = [None,None]
    if self.checkNeighbors(x+1,y): 
      if not self.checkWall(x-1,y): E = [x+1,y]
      else: E = [None,None]
    else: E = [None,None]
    if self.checkNeighbors(x,y+1): 
      if not self.checkWall(x,y+1): S = [x,y+1]
      else: S = [None,None]
    else: S = [None,None]
    if self.checkNeighbors(x,y-1): 
      if not self.checkWall(x,y-1): N = [x,y-1]
      else: N = [None,None]
    else: N = [None,None]
    return [N,S,E,W]
 
if __name__ == "__main__":
  calc = MDP()
  

