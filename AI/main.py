from flask import Flask, request, jsonify
from flask_cors import CORS
import DQN_ai as ai
import numpy as np
import threading
import time

app = Flask(__name__)
CORS(app)

default_values = {
        'birdRightX': 0,
        'birdLeftX': 0,
        'birdBottomY': 0,
        'birdTopY': 0,
        'nextPipeRightX': 0,
        'nextPipeLeftX': 0,
        'nextPipeBottomY': 0,
        'nextPipeTopY': 0,
        'score': 0,
        'alive': True
    }

state_size = 10
action_size = 2
agent = ai.DQNAgent(3, 2)

@app.route('/get_AI_action', methods=['POST'])
def get_AI_action():
    data = request.json

    birdRightX = data['state']['birdRightX']
    birdLeftX = data['state']['birdLeftX']
    birdBottomY = data['state']['birdBottomY']
    birdTopY = data['state']['birdTopY']
    nextPipeRightX = data['state']['nextPipeRightX']
    nextPipeLeftX = data['state']['nextPipeLeftX']
    nextPipeBottomY = data['state']['nextPipeBottomY']
    nextPipeTopY = data['state']['nextPipeTopY']
    score = data['state']['score']
    alive = data['state']['alive']

    processed_state = np.array([
        birdRightX,
        birdLeftX,
        birdBottomY,
        birdTopY,
        nextPipeRightX,
        nextPipeLeftX,
        nextPipeBottomY,
        nextPipeTopY,
        score,
        alive
    ]).reshape(1, state_size)

    processed_state = np.squeeze(processed_state)

    action = agent.act(processed_state)
    return jsonify({'action': action})

@app.route('/store_experience', methods=['POST'])
def store_experience():
    data = request.json

    birdRightX = data['state']['birdRightX']
    birdLeftX = data['state']['birdLeftX']
    birdBottomY = data['state']['birdBottomY']
    birdTopY = data['state']['birdTopY']
    nextPipeRightX = data['state']['nextPipeRightX']
    nextPipeLeftX = data['state']['nextPipeLeftX']
    nextPipeBottomY = data['state']['nextPipeBottomY']
    nextPipeTopY = data['state']['nextPipeTopY']
    score = data['state']['score']
    alive = data['state']['alive']

    state = np.array([
        birdRightX,
        birdLeftX,
        birdBottomY,
        birdTopY,
        nextPipeRightX,
        nextPipeLeftX,
        nextPipeBottomY,
        nextPipeTopY,
        score,
        alive
    ]).reshape(1, state_size)

    action = data.get('action', None)
    reward = calculate_reward(data['state'], data.get('next_state', {}))
    print("reward: ", reward)

    birdRightX = data['next_state']['birdRightX']
    birdLeftX = data['next_state']['birdLeftX']
    birdBottomY = data['next_state']['birdBottomY']
    birdTopY = data['next_state']['birdTopY']
    nextPipeRightX = data['next_state']['nextPipeRightX']
    nextPipeLeftX = data['next_state']['nextPipeLeftX']
    nextPipeBottomY = data['next_state']['nextPipeBottomY']
    nextPipeTopY = data['next_state']['nextPipeTopY']
    score = data['next_state']['score']
    alive = data['next_state']['alive']

    next_state = np.array([
        birdRightX,
        birdLeftX,
        birdBottomY,
        birdTopY,
        nextPipeRightX,
        nextPipeLeftX,
        nextPipeBottomY,
        nextPipeTopY,
        score,
        alive
    ]).reshape(1, state_size)

    done = data.get('done', False)

    # Store experience in DQN agent memory
    agent.remember(state, action, reward, next_state, done)

    return 'OK'

def calculate_reward(current_state, next_state):
    total_reward = 0

    if not current_state.get('alive'):
        total_reward -= 1.0
    else:
        total_reward -= 0.1
    
    if next_state.get('score') > current_state.get('score'):
        total_reward += current_state.get('score') - next_state.get('score')
    
    return total_reward

def background_training():
    batch_size = 32
    while True:
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
        time.sleep(0.1)

if __name__ == '__main__':
    training_thread = threading.Thread(target=background_training)
    training_thread.start()
    app.run(debug=True, port=5000)