# Double DQN Algorithm Description

In this project i implemented a variation of the DQN algorithm called Double DQN .

DQN stands for deep Q-Network which combines a deep neural network with classic temporal difference learning algorithm Q-learning(also called sarsamax).

DQN is a function approximation algorithm , where the neural network serves as a function approximator for Q-learning's state-action Q value function Q(s,a)  which is interpreted as the expected feature reward if the agent starts and state "s" and takes action "a", this approximator is then used to derive the optimal policy of the agent which consists on the action that maximizes the Q function for a given state.

In order to train the Q function approximator network a second function is needed, this second function is a related function that needs to be optimized, in this case a cost/loss function which needs to be minimized with respect to the parameters of the Q function parameters via gradient descent. The minimized function is the mean squared error which is based on the squared difference between an approximation for a given state and action , and a real oserved value for the same state and action , the observed values are real values collected by the agent through experience.

This method uses "experience replay" storing experience tuples in a memory buffer and a target network which is a previous copy of the Q network , this helps stabilize the training making the process similar to a supervised learning setting.

Additional to these 2 techniques(taken from the 2015 DeepMind Atari Paper) i used another technique from a different DeepMind paper called double deep Q-learning which tries to minimize maximization bias by using the second deep neural network(target network) as an evaluator of the value of the actions selected by the local original Q network
