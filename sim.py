
import asyncio
import websockets

# Define the sim environment class that accepts both human input and agent input
class Sim:
    def __init__(self) -> None:
        # send initial state to the aruido board
        # initialize with LEDs off
        self.g1 = False
        self.g2 = False
        return
    
    
    # list of states allowed
    __states : list = [
        'g1_on, g2_on',  # index 0
        'g1_on, g2_off',
        'g1_off, g2_on',
        'g1_off, g2_off'
    ]

    __action_list : list = [
        'no_action', #0
        'g2_off',    #1
        'g2_on'      #2
    ]

    # Possible actions for each state
    # refer to the states by index
    __actions = { 
        0 : [0, 1],  # no action or g2_off
        1 : [0, 2],  # no action or g2_on   etc...
        2 : [0, 1],
        3 : [0, 2]  
    }

    @property
    def states(self):
        return self.__states
    
    @property
    def current_state(self):
        g1 = 'g1_on' if self.g1 else 'g1_off'
        g2 = 'g2_on' if self.g2 else 'g2_off'
        return g1 + ', ' + g2
  
    @property
    def current_state_idx(self):
        try:
            return self.__states.index(self.current_state)                                    
        except ValueError:
            raise ValueError("ERR-0001: Current state not found in the list of states.")
        
    @property
    def actions(self):
        return self.__actions
    
    @property
    def action_list(self):
        return self.__action_list
    
    # the human is flipping g1
    def human_action(self):
        self.g1 = False if self.g1 else True
        self.g2 = False if self.g2 else True
        return

    # external agent trying an action
    def try_action(self, action):
        if action not in self.get_actions(self.current_state):
            print("action not allowed " + action)
            assert "error"
            return False
        
        # change state:
        print("action attempted: " + str(action))

        if action == 'g2_on':
            self.g2 = True
        
        if action == 'g2_off':
            self.g2 = False
        
        return True
    
    def get_action_idx(self, action):
        try:
            return self.__action_list.index(action)                                    
        except ValueError:
            return None
    
    def get_actions(self, state):
        try:
            state_idx = self.__states.index(state)            
            allowed_action_indexes = self.__actions[state_idx]        
            return [self.__action_list[i] for i in allowed_action_indexes]
        except ValueError:
            return []

    def get_state_idx(self, state):
        try:
            return self.__states.index(state)            
        except ValueError:
            return None


    # the reward is calculate based on if G1 == G2
    def get_reward(self):
        if self.g1 == self.g2:
            return 10        
            
        return -5
    

    async def client():        
        async with websockets.connect("ws://localhost:8765") as websocket:
            await websocket.send("Hello, world!")
            response = await websocket.recv()
            print("Received response:", response)
        