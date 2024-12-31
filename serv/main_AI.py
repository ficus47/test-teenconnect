from flask import Flask, request
import tensorflow as tf
import json

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import layers

app = Flask(__name__)

#model loading
model = load_model("model_LSTM.keras")

#tokenizer loading
with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = Tokenizer.from_json(data)
    del data

@app.route("/check-text")
def check_text():
    text = request.args["text"]