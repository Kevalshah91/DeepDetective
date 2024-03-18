from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

# Function to get image dimensions
def get_image_dimensions(image):
    with Image.open(image) as img:
        width, height = img.size
    return width, height

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')
        
        file = request.files['file']

        # Check if the file is an image
        if file.filename == '':
            return render_template('index.html', error='No file selected')
        
        if file:
            # Get the image dimensions
            width, height = get_image_dimensions(file)
            return render_template('index.html', width=width, height=height)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
