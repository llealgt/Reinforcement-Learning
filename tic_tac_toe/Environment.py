

class Environment:
	def __init__(self):
		# three symbols will be used: 0 for empty , -1 for x, 1 for o
		self.board = np.zeros((LENGTH,LENGTH))
		self.x = -1 
		self.o = 1
		self.winner = None
		self.ended = False
		self.num_states  = np.power(3,(LENGTH*LENGTH)) 

	def is_empty(self,i,j):
		return self.board[i,j] == 0

	def reward(self,sym):
		#for all states reward is 0 until  game is over
		if not self.game_over():
			return 0

		#1 if the player is the current winner 0 otherwise
		return 1 if self.winner == sym else 0

	def get_state(self):
		# maps every possible board state to an integer number, that means theres 3^(LENGHT*LENGTH) possible values, 1  integer per possible state
		# for other problems different than tic tac toe this function does not apply and should be dessigned accordingly
		k = 0
		h = 0

		for i in xrange(LENGTH):
			for j in xrange(LENGTH):
				if self.board[i,j] == 0: #empty
					v = 0
				elif self.board[i,j] == self.x:
					v = 1
				elif self.board[i,j] == self.o:
					v = 2

				h += np.power(3,k) * v #h because its a hash(numeric), for the current state
				k += 1

		return h


		def game_over(self,force_recalculate = False):
			"""
			force recalculate is used because game_over may be called multiple times after the game is over
			enumarating states recursively brings the board in+out of game over step

			"""
			if not force_recalculate and self.ended: 
				return self.ended

			
			for player in (self.x,self.o):
				#check for winner in rows and cols 
				for i in xrange(LENGTH):
					if self.board[i].sum() == player*LENGTH or self.board[:,i].sum() == player*LENGTH:
						self.winner = player
						self.ended  = True
						return True

				#check diagonals(matrix trace or traza in spanish is the sum of main diagonal elements)
				## top-left to botton-right or top-right to botton-left
				if self.board.trace() == player*LENGTH or np.fliplr(self.board).trace() == player*LENGTH:
					self.winner = player
					self.ended = True
					return True

			#check if draw(if all board is filled but nobody won)
			if np.all((sellf.board == 0) == False):
				# winner is None but episode is ended
				self.winner = None
				self.ended = True
				return True

			#game not ended
			self.winner = None
			return False

		def draw_board(self):
			for i in xrange(LENGTH):
				print("-------------")
				for j in xrange(LENGTH):
					print(" ")
					if self.board[i,j] == self.x:
						print("x")
					elif self.board[i,j] == self.o:
						print("o")
					else:
						print(" ")
			print("")

	