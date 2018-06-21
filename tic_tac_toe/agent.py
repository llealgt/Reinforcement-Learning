import numpy as np

class  Agent:
	def __init__(self,alpha = 0.1, epsilon = 0.5):
		self.aplha = alpha # learning rate
		self.epsilon = epsilon # epsilon for espsilon-freedy explore/exploit selection
		self.verbose = False #if true, print values for every positon on the board
		self.state_history = []

	def set_value(self,value): #the value funciton of this agent
		self.value = value

	def set_symbol(self,symbol):
		self.symbol = symbol

	def set_verbose(self,verbose):
		self.verbose = verbose

	def reset_history(self):
		self.state_history = []

	def take_action(self,env):
		#choose and action based on epsilon-greedy strategy
		r = np.random.rand()
		best_state = None

		if r < self.epsilon:
			#take random action
			if self.verbose:
				print("Taking random action")

			possible_moves = []
			for i in xrange(LENGTH):
				for j in xrange(LENGTH):
					if env.is_empty(i,j):
						possible_moves.append((i,j))

			idx  = np.random.choice(len(possible_moves))
			next_move = possible_moves[idx]
		else:
			#greedy action
			position_to_value = []
			next_move = None
			best_value = -1

			for i in xrange(LENGTH):
				for j in xrange(LENGTH):
					if env.is_empty(i,j):
						#what is the state if we make this move
						env.board[i,j] = self.symbol
						state = env.get_state()
						#change the board back
						env.board[i,j] = 0
						position_to_value[(i,j)] = self.value[state]

						if self.value[state] > best_value:
							best_value = self.value[state]
							best_state = state
							next_move =(i,j)

			if self.verbose:
				print("Taking greedy action")
				for i in xrange(LENGTH):
					print("-------------")
					for j in xrange(LENGTH):
						if env.is_empty((i,j)):
							print(position_to_value[(i,j)])
						else:
							print(" ")
							if env.board[i,j] == env.x:
								print("x |")
							elif env.board[u,j] == env.o:
								print("o |")
							else:
								print(" |")
					print("")
				print("-------------")

	def update_state_history(self,s):
		self.state_history.append(s)

	def update(self,env):
		reward = env.reward(self.symbol)
		target = reward

		for previous in reversed(self.state_history):
			new_value = self.value[previous] + self.alpha*(target * self.value[previous])
			self.value[previous] = new_value
			target = new_value

		self.reset_history()