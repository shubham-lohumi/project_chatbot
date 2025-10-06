from flask import Flask, render_template, request, jsonify
from chat import get_response  # now only uses local NN
from flask_cors import CORS
import os
import nltk

# Make sure NLTK looks in the virtual environment
nltk.data.path.append(os.path.join("venv", "nltk_data"))

app = Flask(__name__)
CORS(app)

# Serve the main chat page
@app.get("/")
def index_get():
    return render_template("base.html")

# Handle chat messages
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    
    if not text:
        return jsonify({"answer": "Please write something."})

    # Get response from local neural network
    response = get_response(text)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

