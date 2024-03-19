from flask import Flask, render_template, request
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("E:\code\Projects\Gemini\imageauth\E_model.h5")

def process_image(image_path):
    img = cv2.imread(image_path)
    resize = tf.image.resize(img, (32, 32))
    y_pred = model.predict(np.expand_dims(resize/255, 0))
    label = "REAL" if y_pred[0][0] > 1.42 else "FAKE"
    return label

@app.route('/', methods=['GET', 'POST'])
def index():
    label = ""
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            image_path = "temp_image.jpg"  # Save the uploaded image temporarily
            image_file.save(image_path)
            label = process_image(image_path)

    return render_template('index.html', label=label)

if __name__ == '__main__':
    app.run(debug=True)
