"""Simple config, values can be changed to change
   the simmulation's behaviour"""
WIDTH = 400
HEIGHT = 300

BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255, 0, 0)

FPS = 120

SPEED = 2
NODES = 100 #nr of nodes
SIZE = 3 #size in pixels

NODES_INFECTED = 1
INFECTION_CHANCE  = 30  #in percent

INFECTION_DEADLYNESS = 40 # Chance of the infection killing the node
INFECTED_SURVIVAL_TIME = 1000 # Time it takes for the infection to kill the node

IMMUNE_TIME = 2000 # 2sec.
INFECTED_TIME = 10000 # Time in ms the node stays infected.
