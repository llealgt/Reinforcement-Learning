
# https://deeplearningcourses.com/c/artificial-intelligence-reinforcement-learning-in-python
# https://www.udemy.com/artificial-intelligence-reinforcement-learning-in-python
# Simple reinforcement learning algorithm for learning tic-tac-toe
# Use the update rule: V(s) = V(s) + alpha*(V(s') - V(s))
# Use the epsilon-greedy policy:
#   action|s = argmax[over all actions possible from state s]{ V(s) }  if rand > epsilon
#   action|s = select random action from possible actions from state s if rand < epsilon
#
#
# INTERESTING THINGS TO TRY:
#
# Currently, both agents use the same learning strategy while they play against each other.
# What if they have different learning rates?
# What if they have different epsilons? (probability of exploring)
#   Who will converge faster?
# What if one agent doesn't learn at all?
#   Poses an interesting philosophical question: If there's no one around to challenge you,
#   can you reach your maximum potential?
from __future__ import print_function, division
from builtins import range, input
# Note: you may need to update your version of future
# sudo pip install -U future


import numpy as np
import matplotlib.pyplot as plt

LENGTH = 3


class  Agent:
  def __init__(self,alpha = 0.1, epsilon = 0.5,length=3):
    self.alpha = alpha # learning rate
    self.epsilon = epsilon # epsilon for espsilon-freedy explore/exploit selection
    self.verbose = False #if true, print values for every positon on the board
    self.state_history = []
    self.length = length

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
      for i in range(self.length):
        for j in range(self.length):
          if env.is_empty(i,j):
            possible_moves.append((i,j))

      idx  = np.random.choice(len(possible_moves))
      next_move = possible_moves[idx]
    else:
      #greedy action
      position_to_value = {}
      next_move = None
      best_value = -1

      for i in range(self.length ):
        for j in range(self.length ):
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
        for i in range(self.length):
          print("-------------")
          for j in range(self.length):
            if env.is_empty(i,j):
              print(position_to_value[(i,j)])
            else:
              print(" ")
              if env.board[i,j] == env.x:
                print("x |")
              elif env.board[i,j] == env.o:
                print("o |")
              else:
                print(" |")
          print("")
        print("-------------")

    env.board[next_move[0],next_move[1]] = self.symbol

  def update_state_history(self,s):
    self.state_history.append(s)

  def update(self,env):
    reward = env.reward(self.symbol)
    target = reward

    for previous in reversed(self.state_history):
      new_value = self.value[previous] + self.alpha*(target - self.value[previous])
      self.value[previous] = new_value
      target = new_value

    self.reset_history()


# this class represents a tic-tac-toe game
# is a CS101-type of project


class Environment:
  def __init__(self,length = 3):
    # three symbols will be used: 0 for empty , -1 for x, 1 for o
    self.board = np.zeros((length,length))
    self.x = -1 
    self.o = 1
    self.winner = None
    self.ended = False
    self.num_states  = np.power(3,(length*length)) 
    self.length = length

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

    for i in range(self.length):
      for j in range(self.length):
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
      for i in range(self.length):
        if self.board[i].sum() == player*LENGTH or self.board[:,i].sum() == player*self.length:
          self.winner = player
          self.ended  = True
          return True

      #check diagonals(matrix trace or traza in spanish is the sum of main diagonal elements)
      ## top-left to botton-right or top-right to botton-left
      if self.board.trace() == player*LENGTH or np.fliplr(self.board).trace() == player*self.length:
        self.winner = player
        self.ended = True
        return True

    #check if draw(if all board is filled but nobody won)
    if np.all((self.board == 0) == False):
      # winner is None but episode is ended
      self.winner = None
      self.ended = True
      return True

    #game not ended
    self.winner = None
    return False

  def draw_board(self):
    for i in range(self.length):
      print("-------------")
      for j in range(self.length):
        print("  ", end="")
        if self.board[i,j] == self.x:
          print("x", end="|")
        elif self.board[i,j] == self.o:
          print("o", end="|")
        else:
          print(" ", end="|")
      print("")
    print("-------------")

  

  



class Human:
  def __init__(self):
    pass

  def set_symbol(self,symbol):
    self.symbol = symbol

  def take_action(self,env):
    while True:
      move = raw_input("Enter coordinates i,j for your next move:")
      i,j = move.split(",")

      i = int(i)
      j = int(j)


      if env.is_empty(i,j):
        env.board[i,j] = self.symbol
        break

  def update(self,env):
    pass

  def update_state_history(self,s):
    pass


# recursive function that will return all
# possible states (as ints) and who the corresponding winner is for those states (if any)
# (i, j) refers to the next cell on the board to permute (we need to try -1, 0, 1)
# impossible games are ignored, i.e. 3x's and 3o's in a row simultaneously
# since that will never happen in a real game
def get_state_hash_and_winner(env, i=0, j=0):
  results = []

  for v in (0, env.x, env.o):
    env.board[i,j] = v # if empty board it should already be 0
    if j == 2:
      # j goes back to 0, increase i, unless i = 2, then we are done
      if i == 2:
        # the board is full, collect results and return
        state = env.get_state()
        ended = env.game_over(force_recalculate=True)
        winner = env.winner
        results.append((state, winner, ended))
      else:
        results += get_state_hash_and_winner(env, i + 1, 0)
    else:
      # increment j, i stays the same
      results += get_state_hash_and_winner(env, i, j + 1)

  return results

# play all possible games
# need to also store if game is over or not
# because we are going to initialize those values to 0.5
# NOTE: THIS IS SLOW because MANY possible games lead to the same outcome / state
# def get_state_hash_and_winner(env, turn='x'):
#   results = []

#   state = env.get_state()
#   # board_before = env.board.copy()
#   ended = env.game_over(force_recalculate=True)
#   winner = env.winner
#   results.append((state, winner, ended))

#   # DEBUG
#   # if ended:
#   #   if winner is not None and env.win_type.startswith('col'):
#   #     env.draw_board()
#   #     print "Winner:", 'x' if winner == -1 else 'o', env.win_type
#   #     print "\n\n"
#   #     assert(np.all(board_before == env.board))

#   if not ended:
#     if turn == 'x':
#       sym = env.x
#       next_sym = 'o'
#     else:
#       sym = env.o
#       next_sym = 'x'

#     for i in range(LENGTH):
#       for j in range(LENGTH):
#         if env.is_empty(i, j):
#           env.board[i,j] = sym
#           results += get_state_hash_and_winner(env, next_sym)
#           env.board[i,j] = 0 # reset it
#   return results


def initialV_x(env, state_winner_triples):
  # initialize state values as follows
  # if x wins, V(s) = 1
  # if x loses or draw, V(s) = 0
  # otherwise, V(s) = 0.5
  V = np.zeros(env.num_states)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.x:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


def initialV_o(env, state_winner_triples):
  # this is (almost) the opposite of initial V for player x
  # since everywhere where x wins (1), o loses (0)
  # but a draw is still 0 for o
  V = np.zeros(env.num_states)
  for state, winner, ended in state_winner_triples:
    if ended:
      if winner == env.o:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V


def play_game(p1, p2, env, draw=False):
  # loops until the game is over
  current_player = None
  while not env.game_over():
    # alternate between players
    # p1 always starts first
    if current_player == p1:
      current_player = p2
    else:
      current_player = p1

    # draw the board before the user who wants to see it makes a move
    if draw:
      if draw == 1 and current_player == p1:
        env.draw_board()
      if draw == 2 and current_player == p2:
        env.draw_board()

    # current player makes a move
    current_player.take_action(env)

    # update state histories
    state = env.get_state()
    p1.update_state_history(state)
    p2.update_state_history(state)

  if draw:
    env.draw_board()

  # do the value function update
  p1.update(env)
  p2.update(env)


if __name__ == '__main__':
  # train the agent
  p1 = Agent()
  p2 = Agent()

  # set initial V for p1 and p2
  env = Environment()
  state_winner_triples = get_state_hash_and_winner(env)


  Vx = initialV_x(env, state_winner_triples)
  p1.setV(Vx)
  Vo = initialV_o(env, state_winner_triples)
  p2.setV(Vo)

  # give each player their symbol
  p1.set_symbol(env.x)
  p2.set_symbol(env.o)

  T = 10000
  for t in range(T):
    if t % 200 == 0:
      print(t)
    play_game(p1, p2, Environment())

  # play human vs. agent
  # do you think the agent learned to play the game well?
  human = Human()
  human.set_symbol(env.o)
  while True:
    p1.set_verbose(True)
    play_game(p1, human, Environment(), draw=2)
    # I made the agent player 1 because I wanted to see if it would
    # select the center as its starting move. If you want the agent
    # to go second you can switch the human and AI.
    answer = input("Play again? [Y/n]: ")
    if answer and answer.lower()[0] == 'n':
      break