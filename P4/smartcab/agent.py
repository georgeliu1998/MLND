import random
import numpy as np
from pprint import pprint
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # All possible actions
        self.actions = self.env.valid_actions 
        # All traffic light choices
        traffic_light = ['red', 'green']
        # All other states have the same choices
        waypoint, oncoming, left = self.actions, self.actions, self.actions

        # Initialize trial and reward counters
        self.trials = 0
        self.rewards = 0
        # Initialize a dictionary to store the Q-values, intialized with all zeros        
        self.q_table = {}
        for li in traffic_light:
            for pt in waypoint:
                for on in oncoming:
                    for lf in left:
                        self.q_table[(li, pt, on, lf)] = {None: 0, 'forward': 0, 'left': 0, 'right': 0}
    

    def reset(self, destination=None):
        self.planner.route_to(destination)
 

    def update(self, t):
        # Update trial counter
        if self.env.t == 0:
            self.trials += 1

        # Set the tuning parameters
        alpha = 0.5 # learning rate
        gamma = 0.5 # discount factor
        # Exploration probability, i.e. the fraction of random actions
        # Start with the given value then decay at equal interval towards zero for each trial
        epsilon_start = .2
        epsilon = list(np.arange(0, epsilon_start, epsilon_start/100))[100 - self.trials] 
        
        # Gather inputs and sense the "before state" s
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        self.state = (inputs['light'], self.next_waypoint, inputs['oncoming'], inputs['left'])
        
        # Perform action a and collect reward r
        # Select action using Epsilon-greedy strategy
        if random.uniform(0, 1) < epsilon:
            action = random.choice(self.actions) # take random actions
        else:
            action = max(self.q_table[self.state],
                         key=self.q_table[self.state].get) # take optimal actions
        # Execute action and get reward
        reward = self.env.act(self, action)
        self.rewards += reward
        
        # Sense the new state s'
        next_waypoint_new = self.planner.next_waypoint()
        inputs_new = self.env.sense(self)
        state_new = (inputs_new['light'], next_waypoint_new, inputs_new['oncoming'], inputs_new['left'])

        # Calculate the Q_value
        q_value = (1 - alpha) * self.q_table[self.state][action] + \
                  alpha * (reward + gamma * max(self.q_table[state_new].values()))
        # Update the Q_table
        self.q_table[self.state][action] = q_value
          
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit

    # Print the total reward
    print "The total reward is: {}".format(a.rewards)
    # Print the Q-table
    #pprint(a.q_table)


if __name__ == '__main__':
    run()
