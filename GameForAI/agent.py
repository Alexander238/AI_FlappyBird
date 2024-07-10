import torch
import random
import numpy as np
from collections import deque
from gameAI import FlappyBirdGameAI

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # for randomness
        self.gamma = 0 # discount rate
        '''
        will automatically remove the first element if the length exceeds MAX_MEMORY
        ===> older and less important memories are removed first
        '''
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None
        self.trainer = None      

    def get_state(self, game):
        lower_pipe_x = game.pipes[0].x if game.pipes[0].x is not None else -100
        lower_pipe_y = game.pipes[0].y if game.pipes[0].y is not None else -100
        upper_pipe_x = game.pipes[1].x if game.pipes[1].x is not None else -100
        upper_pipe_y = game.pipes[1].y if game.pipes[1].y is not None else -100

        return np.array([
            # Bird
            game.bird.x, game.bird.y, 
            # Pipes
            lower_pipe_x, lower_pipe_y, upper_pipe_x, upper_pipe_y], dtype=np.float32) # dtype=np.float32 would convert booleans to 0.0 or 1.0, if I want to add some later.
    
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
        self.epsilon = 80 - self.number_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    agent = Agent()
    game = FlappyBirdGameAI()

    # training loop
    while True:
        current_state = agent.get_state(game)
        move_of_agent = agent.get_action(current_state)
        # receive feedback from the environment
        game_over, reward, score = game.game_step(move_of_agent)

        new_state = agent.get_state(game)
    
        agent.train_short_memory(current_state, move_of_agent, reward, new_state, game_over)
        agent.remember(current_state, move_of_agent, reward, new_state, game_over)

        #agent.train_long_memory()

        if game_over:
            game.reset_game()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save()

            print(f'Game {agent.number_of_games} Score: {score} \nRecord: {record}')

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)

            if agent.number_of_games % 10 == 0:
                pass

        pass

if __name__ == '__main__':
    train()