from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import cv2
import os
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load your model
model = tf.keras.models.load_model("model_air.h5")

def preprocess_image(img):
    img = cv2.resize(img, (800, 600))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = tf.image.resize(np.expand_dims(img, 0), (32, 32))
    return img / 255.0

def predict_images(images):
    predictions = []
    for img in images:
        img_preprocessed = preprocess_image(img)
        y_pred = model.predict(img_preprocessed)
        predictions.append(y_pred)
    return predictions

def classify_avg(predictions):
    avg_prediction = np.mean(predictions)
    return "REAL" if avg_prediction > 0.5 else "FAKE"

def extract_frames_from_video(url, output_folder, interval):
    try:
        # Download video and get its path
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download()

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Open video file
        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        img_count = 0
        img_paths = []  # List to store image paths

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            # Save frame every 'interval' frames
            if frame_count % interval == 0:
                img_path = os.path.join(output_folder, f"frame_{img_count}.jpg")
                cv2.imwrite(img_path, frame)
                img_paths.append(img_path)  # Append image path to the list
                img_count += 1

        cap.release()
        cv2.destroyAllWindows()

        print(f"Frames extracted successfully and saved in '{output_folder}' folder!")

        # Delete the video file after extracting frames
        os.remove(video_path)

        return img_paths

    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    try:
        video_url = request.form['video_url']
        output_folder = "img"  # Folder to save the extracted frames
        interval = 100  # Interval to extract frames (e.g., every 100 frames)

       