# Double DQN Algorithm Description

In this project i implemented a variation of the DQN algorithm called Double DQN .

DQN stands for deep Q-Network which combines a deep neural network with classic temporal difference learning algorithm Q-learning(also called sarsamax).

DQN is a function approximation algorithm , where the neural network serves as a function approximator for Q-learning's state-action Q value function Q(s,a)  which is interpreted as the expected feature reward if the agent starts and state "s" and takes action "a", this approximator is then used to derive the optimal policy of the agent which consists on the action that maximizes the Q function for a given state.

In order to train the Q function approximator network a second function is needed, this second function is a related function that needs to be optimized, in this case a cost/loss function which needs to be minimized with respect to the parameters of the Q function parameters via gradient descent. The minimized function is the mean squared error which is based on the squared difference between an approximation for a given state and action , and a real oserved value for the same state and action , the observed values are real values collected by the agent through experience.

This method uses "experience replay" storing experience tuples in a memory buffer and a target network which is a previous copy of the Q network , this helps stabilize the training making the process similar to a supervised learning setting.

Additional to these 2 techniques(taken from the 2015 DeepMind Atari Paper) i used another technique from a different DeepMind paper called double deep Q-learning which tries to minimize maximization bias by using the second deep neural network(target network) as an evaluator of the value of the actions selected by the local original Q network

## Hyperparameters

| Hyperparameter        | Value           | Comment  |
| ------------- |:-------------:| -----:|
| start epsilon      | 1.0| The agent starts in full exploration mode |
| end epsilon      | 0.01      |   The exploration decay to a limit of 1% meaning it will explore 1% of the time |
| epsilon decay | 0.99125      |    The exploration probability decrases 99.125% every iteration |
| update target network every      | 50 | Target network gets a copy from local network every 50 steps |
| replay buffer size      | 100000      |   How many experience tuples to  store(last observed) |
| train every | 4      |    Trainind is not performed every step but every 4 experience steps |
| batch size      | 32 | A batch of 32 experience tuples is randomly sampled from replay buffer |
| learning rate      | 0.00025      |   a learning rate of 0.00025 is used with an Adam optimizer |
| QNetork hidden layers| 2      |    The Q network has hidden 2 layers |
| Number of hidden units in QNetwork      | 150,150 | every hidden layer las 150 nits|


## Rewards per episode

!Rewards Per Episode](rewards_per_episode.png)
Format: ![Alt Text](url)
