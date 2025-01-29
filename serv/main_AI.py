from sanic import Sanic
from sanic.response import json
import tensorflow as tf
import json
import cv2

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import layers

app = Sanic(__name__)

#model loading
model_hate = load_model("model_LSTM.keras")
model_age = load_model("model_age.keras")

#tokenizer loading
with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = Tokenizer.from_json(data)
    del data

@app.route("/check-text", method=["GET"])
def check_text():
    # getting the text
    text = requests.args["text"]

    # preprocessing the text
    text = tokenizer.text_to_sequences(text)

    #testing the text
    index_of_hate = model_hate.predict(text)[0]

    return index_of_hate

@app.route("/age", method=["POST"])
def check_age():
    img = request.args["img"]
    open("img.png", "w").write(img)
    img = cv2.imread("img.png")
    image = cv2.resize(image, (224, 224))
    return model_age.predict(img)[0]