from pytube import YouTube
import cv2
import os
import gc
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("model_air.h5")

def extract_frames_from_video(url, output_folder, interval):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_path = stream.download()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        img_count = 0
        img_paths = []

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_count += 1

            if frame_count % interval == 0:
                img_path = os.path.join(output_folder, f"frame_{img_count}.jpg")
                cv2.imwrite(img_path, frame)
                img_paths.append(img_path)
                img_count += 1

        cap.release()
        cv2.destroyAllWindows()

        os.remove(video_path)

        return img_paths

    except Exception as e:
        print(f"Error extracting frames: {e}")
        return []

if __name__ == "__main__":
    video_url = 'https://www.youtube.com/shorts/agJ0CvXXNRo'
    output_folder = "img"
    interval = 100

    image_paths = extract_frames_from_video(video_url, output_folder, interval)

    images = [cv2.imread(img_path) for img_path in image_paths]

    predictions = []
    for img in images:
        img_preprocessed = cv2.resize(img, (32, 32))
        img_preprocessed = cv2.cvtColor(img_preprocessed, cv2.COLOR_BGR2RGB)
        img_preprocessed = np.expand_dims(img_preprocessed, 0) / 255.0
        y_pred = model.predict(img_preprocessed)
        predictions.append(y_pred)

    avg_prediction = np.mean(predictions)
    classification = "REAL" if avg_prediction > 0.5 else "FAKE"
    print(f"Overall prediction: {classification} based on average response")

    for x in image_paths:
        os.remove(x)

    del images
    gc.collect()
