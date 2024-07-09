from flask import Flask, request, jsonify
from flask_cors import CORS
#import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/get_AI_action', methods=['POST'])
def get_AI_action():
    data = request.json

    state = data['state']
    if state['birdBottomY'] > 0.5:
        action = 1
    else:
        action = 0

    return jsonify({'action': action})



if __name__ == '__main__':
    app.run(debug=True, port=5000)
