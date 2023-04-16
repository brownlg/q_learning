# Configured for Game of Mirros

import numpy as np
import random 

from sim import Sim
from agent import Agent

sim : Sim = Sim()
agent : Agent = Agent(sim)

for i in range(0, 100):
    print("--------------------------------------- " + str(i))
    print("Sim current state: " + sim.current_state)
    result = agent.think()               

    # now randomly the human will change g1 10% of the time
    human_act = random.random()
    if human_act < 0.5:
        print("HUMAN ACTION")
        sim.human_action()
        # agent needs to get feedback, even though it didnt take an action
        agent.think(False)

   