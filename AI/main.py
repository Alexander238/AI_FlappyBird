from flask import Flask, request, jsonify
from flask_cors import CORS
import DQN_ai as ai
import numpy as np
import threading
import time

app = Flask(__name__)
CORS(app)

state_size = 7
action_size = 2
agent = ai.DQNAgent(state_size=state_size, action_size=action_size)

@app.route('/get_AI_action', methods=['POST'])
def get_AI_action():
    data = request.json
    state = data['state']

    state_values = np.array([
        state['birdLeftX'],
        state['birdBottomY'],
        state['nextPipeLeftX'],
        state['nextPipeTopY'],
        state['score'],
        state['alive'],
        state['timeAlive']
    ]).reshape(1, state_size)

    action = agent.act(state_values)
    return jsonify({'action': action})

@app.route('/store_experience', methods=['POST'])
def store_experience():
    data = request.json
    state = data['state']
    next_state = data['next_state']

    try:
        state_values = np.array([
            state['birdLeftX'],
            state['birdBottomY'],
            state['nextPipeLeftX'],
            state['nextPipeTopY'],
            state['score'],
            state['alive'],
            state['timeAlive']
        ]).reshape(1, state_size)
    except KeyError as e:
        print(f"Missing key in state: {e}")
        return 'Bad state data', 400
    
    try:
        next_state_values = np.array([
            next_state['birdLeftX'],
            next_state['birdBottomY'],
            next_state['nextPipeLeftX'],
            next_state['nextPipeTopY'],
            next_state['score'],
            next_state['alive'],
            next_state['timeAlive']
        ]).reshape(1, state_size)
    except KeyError as e:
        print(f"Missing key in next_state: {e}")
        return 'Bad next_state data', 400

    action = data['action']
    reward = calculate_reward(state, next_state)
    print(reward)
    done = data['done']

    if None not in state_values and None not in next_state_values:
        agent.remember(state_values, action, reward, next_state_values, done)
    else:
        print("Encountered None in state or next_state values")
        return 'Bad state or next_state data', 400
    
    return 'OK'

def calculate_reward(current_state, next_state):
    total_reward = 0

    if not current_state.get('alive'):
        total_reward -= 10.0

    if (next_state.get('timeAlive') - current_state.get('timeAlive')) > 0:
        total_reward += 1.0
    
    if next_state.get('score') > current_state.get('score'):
        total_reward += 5.0
    
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