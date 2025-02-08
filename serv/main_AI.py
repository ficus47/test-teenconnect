from sanic import Sanic
from sanic.response import json
import tensorflow as tf
import numpy as np
import cv2
import base64
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Sanic("AI_API")

# Chargement des modèles
model_hate = load_model("model_LSTM.keras")
model_age = load_model("model_age.keras")
model_img = load_model("model_img_hate.keras")

# Chargement du tokenizer
with open("tokenizer.json") as f:
    tokenizer_json = f.read()
    tokenizer = Tokenizer.from_json(tokenizer_json)

@app.route("/check-text", methods=["GET"])
async def check_text(request):
    text = request.args.get("text", None)
    
    if not text:
        return json({"error": "Missing text parameter"}, status=400)
    
    # Prétraitement du texte
    sequences = tokenizer.text_to_sequences([text])  # Correction : mettre dans une liste
    padded_sequences = pad_sequences(sequences, maxlen=100)  # Adapter à la taille max

    # Prédiction
    prediction = model_hate.predict(padded_sequences)[0].tolist()

    return json({"hate_score": prediction})

@app.route("/age", methods=["POST"])
async def check_age(request):
    try:
        img_data = request.json.get("img", None)
        
        if not img_data:
            return json({"error": "Missing img parameter"}, status=400)

        # Décodage base64 en image
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return json({"error": "Invalid image data"}, status=400)

        # Redimensionner l'image
        img_resized = cv2.resize(img, (224, 224))
        img_resized = np.expand_dims(img_resized, axis=0)  # Ajout d'une dimension batch

        # Prédiction de l'âge
        age_prediction = model_age.predict(img_resized)[0].tolist()

        return json({"age_prediction": age_prediction})

    except Exception as e:
        return json({"error": str(e)}, status=500)


@app.route("/age", methods=["POST"])
async def check_img(request):
    try:
        img_data = request.json.get("img", None)
        
        if not img_data:
            return json({"error": "Missing img parameter"}, status=400)

        # Décodage base64 en image
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            return json({"error": "Invalid image data"}, status=400)

        # Redimensionner l'image
        img_resized = cv2.resize(img, (224, 224))
        img_resized = np.expand_dims(img_resized, axis=0)  # Ajout d'une dimension batch

        # Prédiction de l'âge
        age_prediction = model_img.predict(img_resized)[0].tolist()

        return json({"age_prediction": age_prediction})

    except Exception as e:
        return json({"error": str(e)}, status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
