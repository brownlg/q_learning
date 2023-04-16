
from sim import Sim
import random
import numpy as np
#import asyncio  <---- future


class Agent():
    def __init__(self, sim) -> None:        
        self._Q = np.matrix(np.zeros([len(sim.states), len(sim.action_list)]))  
        self._sim = sim        
        self._gamma = 0.75        # learning rate
        self._sim_state = None    # error state
        self._agent_state = None #  TBD!!
        self._scores = []
        self._memory = []        # action memory
        self._memory_size = 5
        self._sim_state_prev = None

        # initial query of environment
        self.__query_sim()

    # check environment for updates
    def __query_sim(self):
        print("rec'd input from simulation")
        self._sim_state_prev = self._sim_state
        self._sim_state = self._sim.current_state

    # get the actions the agent can take in current state
    @property
    def actions(self):
        # figure out what possible actions there are in the current state
        self.agent_state = None # <---- future implementation

        allowed_actions = self._sim.get_actions(self._sim_state)

        print("DEBUG: allowed actions = "  + str(allowed_actions))

        # as the sim what are possible actions
        return allowed_actions
    
    @property
    def Q(self):
        return self._Q
               
    def __enqueue(self, item):
        if len(self._memory) >= self._memory_size:
            self._memory.pop(self._memory_size-1)
        self._memory.insert(0, item)
            
    def __dequeue(self):
        if len(self._memory) == 0:
            return None
        else:
            return self._memory.pop(0)
    
    def __queue(self, idx):        
        return self._memory[idx]
            
    def __act(self, action):
        if action == 'no_action':
            print("no action")        

        # signal environment that you are turning on g2:
        if action == 'g2_on':
            self._sim.try_action(action)
                    
        # signal environment that you are turning OFF g2:
        elif action == 'g2_off':
            self._sim.try_action(action)
          
        # always query after action
        self.__query_sim()

        return action
        
    def think(self, internal = True):                     
        if internal:
            resulting_action = self.__choose_action(self.actions)
            print("Agent wants to: " + resulting_action)
            self.__enqueue(resulting_action)
            self.__act(resulting_action)    
            # get the reward for this action (internal or external)
            print("Learn")
            score = self.learn()     # 
            print("score " + str(score))      
            self._scores.append(score)
            print(self.Q)
        else:
            # something happened externally:            
            self.__query_sim()    
            
    # Chooses one of the available actions at random
    # based on the action the agent is taking look up the next state:
    # 'action' is effectively the next state, so Q[action, ] get the current scores for this next state
    # here we get the best next action that has being learned, could be tied occurance, so max_index can have multiple values  
    # this is GREEDY algorthim: (i.e. no exploration)    
    def __choose_action(self, available_actions : list) -> int:
        random_index = random.randint(0, len(available_actions)-1)    
        return available_actions[random_index]


    # Define the state transition function
    # This is the probability that for a given action from a particular state 
    # the agent will move to the next state.

    # ( current state, action, probability )
    
    # Update the Q matrix and return the score
    # aka Q-table
    # The Q-matrix is a table that has one row for each state and one column for each possible action. Each entry in the table 
    # represents the expected future reward that an agent can achieve by taking a particular action in a given state. 
    def learn(self)->float:      
        # get the action index:        
        last_state_idx = self._sim.get_state_idx(self._sim_state_prev)
        last_action_idx = self._sim.get_action_idx(self.__queue(0))
        print("prev state={} idx={} last_action={} idx={}".format(self._sim_state_prev, last_state_idx, self.__queue(0), last_action_idx))
        # 
        # previous reward value:
        reward = self._Q[last_state_idx, last_action_idx]        

        self._Q[last_state_idx, last_action_idx] = self._sim.get_reward() + self._gamma * reward
        
        # Return the 'avg score' or reward obtained so far in the Q matrix
        if (np.max(self._Q) > 0):
            return np.sum(self._Q / np.max(self._Q)*100)
        else:
            return 0
        

    # Q Matrix
    # this contains the learned path, Q-values, represents the 'cummulative reward' an agent will rec in each state
    # # the Q-value represents how 'good' the action in a particular state is
    # The Bellman equation provides a recursive relationship between the value of a state and the values of its neighboring states. 
    # It is a fundamental concept in reinforcement learning and is used to update the Q-values in Q-learning.
    # The proof that the Bellman equation will converge to the optimal Q-values is based on the following assumptions:
    # The environment is stationary, meaning that the transition probabilities and rewards are constant over time.
    # The agent explores all state-action pairs infinitely often.
    # The learning rate parameter used to update the Q-values satisfies the Robbins-Monro conditions.
    # Under these assumptions, it can be shown that the Q-values converge to the true Q-values with probability 
    # 1. This means that as the number of iterations approaches infinity, the Q-values obtained through Q-learning will converge to the optimal Q-values.
    # The proof for this convergence is provided in many reinforcement learning textbooks, 
    # including "Reinforcement Learning: An Introduction" by Sutton and Barto, and "Algorithms for Reinforcement Learning" by Csaba Szepesvári. 
    # The proof involves the use of the theory of stochastic approximation, and it is quite technical. If you're interested, I recommend reading one of these textbooks for a detailed explanation of the proof.

