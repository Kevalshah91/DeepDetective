import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the Keras model
model = tf.keras.models.load_model("model_mark3.keras")

img_p = "nature_form.jpg"  
try:
    img = cv2.imread(img_p)
    if img is None:
        raise FileNotFoundError("File not found")

    img = cv2.resize(img, (800, 600))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()

    # Resize the image
    resized_img = cv2.resize(img, (32, 32))

    # Perform prediction
    y_pred = model.predict(np.expand_dims(resized_img / 255, 0))
    if y_pred > 0.5:
        print(f'Predicted class: REAL')
    else:
        print(f'Predicted class: AI')

except Exception as e:
    print(f"Error: {e}")
