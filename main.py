"""Simple simmulation viewing virus spread among nodes"""
from config import NODES, NODES_INFECTED, SIZE, SPEED
from objects import Simmulation

if __name__ == "__main__":
    sim = Simmulation(NODES, NODES_INFECTED, SIZE, SPEED)
    sim.setup()
    sim.run()
