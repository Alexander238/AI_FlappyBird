import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os # to save the model

class Linear_Q_Network(nn.Module):
    '''
    input_layer: Represents the state. 

    hidden_layer: 256 neurons, first hidden layer. It takes input from the input layer and passes output to the second hidden layer

    output_layer: 1 neuron, represents the action. Since there are only two actions in Flappy Bird, flap or do nothing, we only need a single neuron.

    '''
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model' # Folder to save models
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, learning_rate, gamma):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss() # Mean Squared Error Loss, which is used to measure the difference between two sets of data. 

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long) # action is either 0 or 1
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1: # only one dimension => one sample => unsqueeze to add a dimension. If this is false, it means there are multiple samples and already have the correct shape.
            # unsqueeze() adds a dimension to the tensor. 
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, ) # tuple with only a single value

        # ----------- Bellman Equation to update the Q value -----------

        # Predicted Q values on the current state
        prediction = self.model(state)

        target = prediction.clone()
        for index in range(len(game_over)):
            if not game_over[index]: # if the game is not over, we add a discounted future reward
                Q_new = reward[index] + self.gamma * torch.max(self.model(next_state[index])) # r + γ * max(next_predicted Q value)
            else:
                Q_new = reward[index]

            action[index] = torch.argmax(action[index]) # action is either 0 or 1
            target[index][action[index]] = Q_new

        # lossfunction: MSE
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward() # backpropagation

        self.optimizer.step() # update the weights