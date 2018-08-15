import numpy as np
import matplotlib.pyplot as plt

# grid-world to test some rl algorithms
class Grid: # the environment
	def __init__(self,width,height,start): #width and height are scalars, start is a 2 elements tuple
		self.width = width
		self.height = height
		self.i = start[0]
		self.j = start[1]

	def set(self,rewards,actions): #configure environment rewards and actions
		# rewards is a dictionary indexed by coordinates i,j and value is a reward
		# actions is a dictionary indexed by coordinates i,j and value is a list of evailable actions
		self.rewards = rewards
		self.actions = actions

	def set_state(self,s):
		self.i = s[0]
		self.j  = s[1]

	def current_state(self):
		return (self.i,self.j)

	def is_terminal(self,s):
		return s not in self.actions

	def move(self,action):
		# verify if action is valid action, go to the next state and return corresponding reward(or zero if not valid)
		if action in self.actions[(self.i,self.j)]:
			if action == "U":
				self.i -= 1
			elif action == "D":
				self.i += 1
			elif action == "R":
				self.j += 1
			elif action == "L":
				self.j -=1

		reward = self.rewards.get((self.i,self.j),0)
		#print(action,self.i,self.j,reward)
		return reward

	def undo_move(self,action):
		#perform opposite action
		if action == "U":
			self.i += 1
		elif action == "D":
			self.i -= 1
		elif action == "R":
			self.j -= 1
		elif self.action == "L":
			self.j += 1

	def game_over(self):
		# returns true if game is over(in terminal state, or state with no possible actions)
		return (self.i,self.j) not in self.actions

	def all_states(self):
		#not-optimal ,could be changed to a permanent data structure instead of calculating it every time
		return set(self.actions.keys() | self.rewards.keys())

	def standard_grid():
		# configures a grid (rewards and actions)
		grid = Grid(3,4,(2,0))
		rewards = {(0,3): 1 , (1,3):-1}
		actions = {
			(0,0):('D','R'),
			(0,1):('L','R'),
			(0,2):('L','D','R'),
			(1,0):('U','D'),
			(1,2):('U','D','R'),
			(2,0):('U','R'),
			(2,1):('L','R'),
			(2,2):('L','R','U'),
			(2,3):('L','U')
		}
		grid.set(rewards,actions)

		return grid

	def negative_grid(step_cost=-0.1):
		# configures the grid created in standard_grid to add penalizations for each non reward step
		grid = Grid.standard_grid()
		grid.rewards.update(
			{
				(0,0):step_cost,
				(0,1):step_cost,
				(0,2):step_cost,
				(1,0):step_cost,
				(1,2):step_cost,
				(2,0):step_cost,
				(2,1):step_cost,
				(2,2):step_cost,
				(2,3):step_cost
			}
		)

		return grid

	def play_game(agent,env):
		pass
