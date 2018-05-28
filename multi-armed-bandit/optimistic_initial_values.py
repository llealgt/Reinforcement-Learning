import numpy as np

class Bandit:
	def __init__(self,mean,initial_mean):
		self.mean = mean # true reward mean for the slot
		self.estimate_mean = initial_mean #the estimate reward mean(estimated from data)
		self.N = 0 #number of runs for this slot

	def pull(self): # play this slot and return a reward 
		return np.random.randn() + self.mean 

	def update(self,x): #update the estimated mean from the collected sample and update the number of plays for this slot
		self.N+=1
		self.estimate_mean = (1.0-1.0/self.N)*self.estimate_mean + (1.0/self.N)*x

