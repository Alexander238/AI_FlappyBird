import torch
import random
import numpy as np
from collections import deque

import sys
import os

# Add the path to the parent directory of 'gameAI' to sys.path
gameAI_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(gameAI_path)
from FlappyBirdGameAI import FlappyBirdGameAI

from model import Linear_Q_Network, QTrainer
from helper import plot

MAX_MEMORY = 500_000
BATCH_SIZE = 2000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # for randomness
        self.gamma = 0.9 # discount rate
        '''
        will automatically remove the first element if the length exceeds MAX_MEMORY
        ===> older and less important memories are removed first
        '''
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_Q_Network(7, 256, 1) # inputs, hidden layers, output
        self.trainer = QTrainer(model=self.model, learning_rate=LEARNING_RATE, gamma=self.gamma)  

    def get_state(self, game):
        if len(game.pipes) > 0:
            pipe_x = game.pipes[0].x if game.pipes[0] is not None else 500
            lower_pipe_y = game.pipes[0].y if game.pipes[0] is not None else 500
        else:
            pipe_x = 500
            lower_pipe_y = 500
        
        if len(game.pipes) > 1:
            upper_pipe_y = game.pipes[1].y if game.pipes[1] is not None else 500
        else:
            upper_pipe_y = 500

        return np.array([
            # Bird
            game.bird.x, game.bird.y, 
            # Pipes
            pipe_x, lower_pipe_y, upper_pipe_y,
            # Environment
            game.ceiling, game.floor], dtype=np.float32) # dtype=np.float32 would convert booleans to 0.0 or 1.0, if I want to add some later.
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # random.sample() returns a list of unique elements chosen randomly from the memory
        else:
            mini_sample = self.memory # if less than BATCH_SIZE elements, use the whole memory
        
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def get_action(self, state):
        # random moves: tradeoff between exploration and exploitation
        # At first, do random moves and explore the environment, then the better the model gets, the less random moves it will do and the more it will exploit the environment.
        self.epsilon = 120 - self.number_of_games # The more games, the smaller epsilon gets, the less random moves the model will do.
        final_move = 0
        if random.randint(0, 200) < self.epsilon:
            final_move = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) # Prediction of the model for the current state, can be a raw value or a probability distribution
            final_move = torch.argmax(prediction).item() # Returns the index of the maximum value of the prediction tensor

        return final_move

# Main training loop
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    agent = Agent()
    game = FlappyBirdGameAI()

    while True:
        current_state = agent.get_state(game)
        move_of_agent = agent.get_action(current_state)
        # receive feedback from the environment
        game_over, reward, score = game.game_step(move_of_agent)

        new_state = agent.get_state(game)
    
        agent.train_short_memory(current_state, move_of_agent, reward, new_state, game_over)
        agent.remember(current_state, move_of_agent, reward, new_state, game_over)

        if game_over:
            game.reset_game()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f'Game {agent.number_of_games} Score: {score} \nRecord: {record}')

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()