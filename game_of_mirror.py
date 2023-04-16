# Game of Mirror
# Feb 26, 2023
# L Brown

import numpy as np

# define the state space and action space
states = [0, 1, 2, 3]
actions = [0, 1]

# initialize the Q-table with zeros
Q = np.zeros((len(states), len(actions)))

# set the hyperparameters
alpha = 0.1 # learning rate
gamma = 0.9 # discount factor
epsilon = 0.1 # exploration rate

# define the reward function
def reward(state, action):
    if state == 3 and action == 1:
        return 1 # goal state
    else:
        return 0

# define the main training loop
for episode in range(1000):
    # reset the environment to the initial state
    state = 0

    # loop until the goal state is reached
    while state != 3:
        # choose an action using epsilon-greedy policy
        if np.random.uniform(0, 1) < epsilon:
            action = np.random.choice(actions)
        else:
            action = np.argmax(Q[state])

        # take the action and observe the reward and next state
        next_state = state + action + np.random.randint(-1, 2)
        next_state = max(0, min(next_state, 3)) # clamp the state to [0, 3]
        r = reward(state, action)

        # update the Q-value using the Bellman equation
        Q[state][action] = Q[state][action] + alpha * (r + gamma * np.max(Q[next_state]) - Q[state][action])

        # transition to the next state
        state = next_state

# print the learned Q-table
print(Q)
