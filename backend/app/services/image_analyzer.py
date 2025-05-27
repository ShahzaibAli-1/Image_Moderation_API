import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Load pre-trained model (using MobileNetV2 for demonstration)
model = tf.keras.applications.MobileNetV2(weights='imagenet')
preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
decode_predictions = tf.keras.applications.mobilenet_v2.decode_predictions

async def analyze_image(image: Image.Image) -> dict:
    """
    Analyze an image for potentially harmful content.
    Returns confidence scores for various safety categories.
    """
    # Resize image to model's expected size
    image = image.convert('RGB')
    image = image.resize((224, 224))
    
    # Convert to array and preprocess
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = preprocess_input(img_array)
    img_array = tf.expand_dims(img_array, 0)
    
    # Get predictions
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=5)[0]
    
    # Convert predictions to safety categories
    # This is a simplified example - in production, you'd want a more sophisticated
    # content classification model specifically trained for harmful content detection
    categories = {
        "violence": 0.0,
        "nudity": 0.0,
        "hate_symbols": 0.0,
        "self_harm": 0.0,
        "extremist_content": 0.0
    }
    
    # Map ImageNet categories to safety categories (simplified example)
    for _, label, confidence in decoded_predictions:
        label = label.lower()
        if any(word in label for word in ["weapon", "knife", "gun"]):
            categories["violence"] = max(categories["violence"], confidence)
        elif any(word in label for word in ["flesh", "body"]):
            categories["nudity"] = max(categories["nudity"], confidence)
        # Add more mappings as needed
    
    # Calculate overall safety score
    max_risk = max(categories.values())
    is_safe = max_risk < 0.5  # Threshold can be adjusted
    
    return {
        "safe": is_safe,
        "categories": categories,
        "confidence": 1 - max_risk,
        "labels": [label for _, label, _ in decoded_predictions]
    } 