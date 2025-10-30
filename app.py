# from flask import Flask, render_template, request, jsonify
# from chat import get_response  # now only uses local NN
# from flask_cors import CORS
# import os
# import json
# import torch
# import nltk
# from model import NeuralNet


# # Load trained model
# with open('data.json', 'r') as f:
#     intents = json.load(f)
# app = Flask(__name__)
# CORS(app)
# data=torch.load("data.pth")

# @app.route("/get", methods=["GET", "POST"])
# def chat():
#     userText = request.args.get('msg')
#     return str(get_response(userText))
# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data["all_words"]
# tags = data["tags"]
# model_state = data["model_state"]

# model = NeuralNet(input_size, hidden_size, output_size)
# model.load_state_dict(model_state)
# model.eval()

# # Make sure NLTK looks in the virtual environment
# nltk.data.path.append(os.path.join("venv", "nltk_data"))

# # Serve the main chat page
# @app.get("/")
# def index_get():
#     return render_template("base.html")

# # Handle chat messages
# @app.post("/predict")
# def predict():
#     text = request.get_json().get("message")
    
#     if not text:
#         return jsonify({"answer": "Please write something."})

#     # Get response from local neural network
#     response = get_response(text)
#     return jsonify({"answer": response})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=False)

from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import get_response  # this loads model & predicts

app = Flask(__name__)
CORS(app)  # allow frontend to connect from anywhere

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"answer": "Please enter a message"}), 400

    response = get_response(message)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
