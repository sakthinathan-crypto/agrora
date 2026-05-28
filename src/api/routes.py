from flask import request, jsonify
import tensorflow as tf
import numpy as np
import cv2
import os
model = tf.keras.models.load_model("models/disease_model.h5")

CLASS_NAMES = [
    "healthy",
    "leaf_blight",
    "other_disease"
]
def predict_disease():
    print(request.files)
    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]
    image_path = "temp.jpg"
    file.save(image_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    predicted_index = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    predicted_class = CLASS_NAMES[predicted_index]
    os.remove(image_path)
    return jsonify({
        "disease": predicted_class,
        "confidence": round(confidence, 2)
    })