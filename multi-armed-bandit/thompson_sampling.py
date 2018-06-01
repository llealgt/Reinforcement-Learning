

class BayesianBandit():

	def __init__(self,true_reward_mean):
		self.true_reward_mean = true_reward_mean

		self.predicted_mean = 0
		self.lambda_  = initial_lambda_ #estimated std
		
		self.sum_x = 1 #aux variable to calculate the gausian parameters(mean and std)
		self.tau = 1 #used in the calculation of gausian parameters
		

	def pull(self):
		return np.random.randn() + self.true_reward_mean

	def sample_mean_distribution(self): 
		'''	when selecting the best bandit instead of selecting  the one with biggest estimated mean
			we sample a mean from the estimated mean gaussian distrubution and select the bandit with biggest sampled mean
		'''
		return np.random.randn() / np.sqrt(self.lambda_) + self.predicted_mean

	def update(self,x):

		self.lambda_  += self.tau
		self.sum_x += x
		self.predicted_mean = self.tau*self.sum_x / self.lambda_
