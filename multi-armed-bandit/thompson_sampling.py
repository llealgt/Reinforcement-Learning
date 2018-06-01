

class BayesianBandit():

	def __init__(self,true_reward_mean):
		self.true_reward_mean = true_reward_mean

		self.initial_mean = 0 #m0
		self.predicted_mean = initial_mean #m
		self.initial_lambda_ = 1 #initial std
		self.lambda_  = initial_lambda_ #estimated std
		
		self.sum_x = 0 #aux variable to calculate the gausian parameters(mean and std)
		self.tau = self.lambda_ #used in the calculation of gausian parameters
		self.N = 0

	def pull(self):
		self.N+=1
		return np.random.randn() + self.true_reward_mean

	def sample(self): 
		'''	when selecting the best bandit instead of selecting  the one with biggest estimated mean
			we sample a mean from the estimated mean gaussian distrubution and select the bandit with biggest sampled mean
		'''
		return np.random.randn() / np.sqrt(self.lambda_) + self.predicted_mean

	def update(self,x):

		self.lambda_  = self.initial_lambda_ + (self.tau*self.N)
		self.sum_x += x
		self.predicted_mean = (self.initial_lambda_*self.initial_mean +self.tau*self.sum_x)/(self.initial_lambda_  + self.tau*self.N)