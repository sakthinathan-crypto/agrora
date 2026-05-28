import tensorflow as tf
import numpy as np
import cv2

# Load trained model
model = tf.keras.models.load_model("models/disease_model.h5")

# Class labels
CLASS_NAMES = [
    "healthy",
    "leaf_blight",
    "other_disease"
]

# Image path
IMAGE_PATH = "test.jpg"

# Load image
image = cv2.imread(IMAGE_PATH)

# Resize image
image = cv2.resize(image, (224, 224))

# Normalize image
image = image / 255.0

# Expand dimensions
image = np.expand_dims(image, axis=0)

# Predict
prediction = model.predict(image)

# Get predicted class
predicted_index = np.argmax(prediction)

# Confidence score
confidence = np.max(prediction) * 100

# Final result
predicted_class = CLASS_NAMES[predicted_index]

print("\nPrediction Result")
print("-------------------")
print(f"Disease Status : {predicted_class}")
print(f"Confidence     : {confidence:.2f}%")