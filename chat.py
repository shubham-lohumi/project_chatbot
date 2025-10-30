import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents
with open("data.json", "r") as f:
    intents = json.load(f)

# Load trained model
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    """Return response from local neural network trained on intents.json"""
    # Tokenize and convert to bag of words
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    # Predict intent
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Probability of prediction
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # If confident enough, return random response from that intent
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])

    # Otherwise fallback
    return "I'm not sure I understand. Could you rephrase?"

# if __name__ == "__main__":
#     print("Chatbot is running! (type 'quit' to exit)")
#     while True:
#         sentence = input("You: ")
#         if sentence.lower() == "quit":
#             break

#         resp = get_response(sentence)
#         print(resp)
