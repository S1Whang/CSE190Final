from math import *
from random import *
from numpy import *
import mdp
from read_config import read_config
import sys,time, subprocess as sp

HEADER = '\033[95m'
OKBLUE = '\033[94m'
SGREEN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class QLearn:
  def __init__(self):
    self.pmap = mdp.MDP()
    self.getConfigs()
    self.generateMs()
    self.generateQs()
    for i in range(100):
      self.simulate()
      #time.sleep(.1)
      #sp.call('clear',shell=True)
      #sys.stdout.flush()
    self.printMs()
    self.printRs([0,0])
    self.printPs()
  def getConfigs(self):
    c = read_config()
    self.x = c["map_size"][0]
    self.y = c["map_size"][1]
    self.start = c["start"]
    self.goal = c["goal"]
    self.wall = c["walls"]
    self.pits = c["pits"]
    self.movelist = c["move_list"]
    self.alpha = c["learning_rate"]
    self.gamma = c["discount_factor"]
    self.epsilon = .1
    self.rewardstep = c["reward_step"]
    self.rewardgoal = c["reward_goal"]
    self.rewardwall = c["reward_wall"]
    self.rewardpits = c["reward_pits"]
    self.q = {}
    self.moves = []
    for a in self.movelist:
      self.moves.append((a[0],a[1]))
  def generateMs(self):
    self.floor = [[" " for x in range(self.x)] for y in range(self.y)]
    self.floor[self.goal[0]][self.goal[1]] = "G"
    for i in range(len(self.wall)):
      self.floor[self.wall[i][0]][self.wall[i][1]] = "W"
    for i in range(len(self.pits)):
      self.floor[self.pits[i][0]][self.pits[i][1]] = "P"
  def generateQs(self):
    for i in range(len(self.floor)):
      for j in range(len(self.floor[i])):
        if self.floor[i][j] == "W": 
          for x,y in self.moves: self.q[((i,j),(x,y))] = None
        elif self.floor[i][j] == "G":
          for x,y in self.moves: self.q[((i,j),(x,y))] = self.rewardgoal
        elif self.floor[i][j] == "P":
          for x,y in self.moves: self.q[((i,j),(x,y))] = int("{0:.0f}".format(self.rewardpits))
        else:
          for x,y in self.moves: self.q[((i,j),(x,y))] = 0.00
  def printQs(self):
    for key,val in sorted(self.q.iteritems(),key=lambda(k,v):(v,k)):print "%s: %s"%(key,val)
  def updateQs(self, pos, action):
    x,y = pos
    a,b = action
    npos = (x+a,y+b)
    if x+a < 0 or x+a >= self.y: 
      npos = pos
    if y+b < 0 or y+b >= self.x: 
      npos = pos
    if self.floor[npos[0]][npos[1]] == "W": npos = pos
    oval = self.q.get((pos,action), None)
    maxq = max([self.q.get((npos,(x,y))) for x,y in self.movelist])
    if maxq == None: maxq = 0.0
    maxq *= self.gamma
    self.q[(pos,action)] = oval + self.alpha*(self.rewardstep + maxq-oval)
    return list(npos)    
  def getAction(self,pos):
      if random.random() < self.epsilon:
        index = random.choice([0,1,2,3])
        return self.movelist[index]
      x,y = pos
      q = [self.q.get(((x,y),(a,b))) for a,b in self.movelist]
      maxq = max(q)
      num = q.count(maxq)
      if num != 0:
        directions = [a for a in range(len(self.movelist)) if q[a] == maxq]
        index = random.choice(directions)
      else: index = q.index(maxq)
      return self.movelist[index]
  def simulate(self):
    move = random.choice([0,1,2,3])
    current = self.start[0]
    running = True
    while running:
      self.printMs()
      self.printRs(current)
      self.printPs()
      if current == self.start[0]: time.sleep(.75)
      time.sleep(.5)
      sp.call('clear',shell=True)
      sys.stdout.flush()

      if self.floor[current[0]][current[1]] == "P": break
      if self.floor[current[0]][current[1]] == "G": break
      action = self.getAction(current)
      new = self.updateQs(tuple(current),tuple(action))
      current = new    
  def printMs(self):
    self.mapx = self.x * 14 + 1 
    self.mapy = self.y * 5 + 1 
    for i in range(self.y):
      print ("+"+"-"*14)*self.x+"+"
      row = ""
      row = "|"+" "*5+self.formatQs(self.q[(i,0),(-1,0)])+" "*5+\
            "|"+" "*5+self.formatQs(self.q[(i,1),(-1,0)])+" "*5+\
            "|"+" "*5+self.formatQs(self.q[(i,2),(-1,0)])+" "*5+\
            "|"+" "*5+self.formatQs(self.q[(i,3),(-1,0)])+" "*5+\
            "|"+" "*5+self.formatQs(self.q[(i,4),(-1,0)])+" "*5+"|"
      print row
      row = "|"+" "+self.formatQs(self.q[(i,0),(0,-1)])+\
            " "*4+self.formatQs(self.q[(i,0),(0,1)])+\
            " "+"|"+" "+self.formatQs(self.q[(i,1),(0,-1)])+\
            " "*4+self.formatQs(self.q[(i,1),(0,1)])+\
            " "+"|"+" "+self.formatQs(self.q[(i,2),(0,-1)])+\
            " "*4+self.formatQs(self.q[(i,2),(0,1)])+\
            " "+"|"+" "+self.formatQs(self.q[(i,3),(0,-1)])+\
            " "*4+self.formatQs(self.q[(i,3),(0,1)])+\
            " "+"|"+" "+self.formatQs(self.q[(i,4),(0,-1)])+\
            " "*4+self.formatQs(self.q[(i,4),(0,1)])+" "+"|"
      print row
      row = "|"+" "*5+self.formatQs(self.q[(i,0),(1,0)])+\
            " "*5+"|"+" "*5+self.formatQs(self.q[(i,1),(1,0)])+\
            " "*5+"|"+" "*5+self.formatQs(self.q[(i,2),(1,0)])+\
            " "*5+"|"+" "*5+self.formatQs(self.q[(i,3),(1,0)])+\
            " "*5+"|"+" "*5+self.formatQs(self.q[(i,4),(1,0)])+" "*5+"|"
      print row
    print ("+"+"-"*14)*self.x+"+"
  def printRs(self, pos):
    row0 = None
    for i in range(self.y):
      row0 = ("+"+"-"*14)*self.x+"+"
      row1 = ("|"+" "*14)*self.x+"|"
      print row0
      print row1
      row2 = "|"
      for j in range(self.x):
        row2 += " "*5+self.formatRs(pos,i,j)+" "*5+"|"
      print row2
      print row1
    print row0
  def formatRs(self,pos,x,y): 
    if pos[0] == x and pos[1] == y:
      return " R  "
    else: return "    "
  def printPs(self):
    policy = self.pmap.getMap()
    for i in range(self.y):
      print ("+"+"-"*14)*self.x+"+"
      row = ("|"+" "*14)*self.x+"|"
      print row
      print ("|"+" "*5+self.formatPs(policy[i][0])+\
             " "*5+"|"+" "*5+self.formatPs(policy[i][1])+\
             " "*5+"|"+" "*5+self.formatPs(policy[i][2])+\
             " "*5+"|"+" "*5+self.formatPs(policy[i][3])+\
             " "*5+"|"+" "*5+self.formatPs(policy[i][4])+\
             " "*5+"|")
      print row
    print ("+"+"-"*14)*self.x+"+"
  def formatPs(self, string):
    if string.strip(' ') == "PIT": return FAIL+"PIT "+ENDC
    elif string.strip(' ') == "GOAL": return OKGREEN+"GOAL"+ENDC
    elif string.strip(' ') == "WALL": return WARNING+"GOAL"+ENDC
    else: return OKBLUE+string+ENDC
  def formatQs(self, num):
    if num >= 10.0:
      return OKGREEN+str(10.0)+ENDC
    elif num <= -10.0:
      return FAIL+str(int(num))+" "+ENDC
    elif num < 0: 
      if num == -10.0: return WARNING+str("{:.0f}".format(num))+ENDC
      return WARNING+str("{:.1f}".format(num))+ENDC
    elif num > 5: return SGREEN+str(10.0)+ENDC
    else: return OKBLUE+str("{:.2f}".format(num))+ENDC
if __name__ == "__main__":
  robot = QLearn()
