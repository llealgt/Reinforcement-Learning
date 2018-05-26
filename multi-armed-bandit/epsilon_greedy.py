import numpy as np

class Bandit: #maybe slot is a better name ?

	def __init__(self,mean):
		"""mean: true mean rewards rate for  the slot"""

		self.mean = mean #true reward rate for the slot
		self.estimate_mean = 0 # reward rate found from exploration
		self.N  = 0 #number of steps run

	def pull(self):
		return np.random.randn() + self.mean #  play this slot and get a reward randomly from it

	def update(self,x): #update the estimate of rewards and number of esteps run
		"""Use the reward obtianed in a step(from pulling the slot) to update the estimated mean of reards"""
		self.N += 1
		self.estimate_mean = (1.0-1.0/self.N)*self.estimate_mean + (1.0/self.N)*x #recurence relation for averages