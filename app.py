from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from PIL import Image
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return render_template('index.html', result="No file uploaded.")
    file = request.files['image']
    if file.filename == '':
        return render_template('index.html', result="No selected file.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result = analyze_image(filepath)
    return render_template('index.html', result=result)

def analyze_image(image_path):
    # Dummy logic to simulate conservation detection
    img = Image.open(image_path)
    width, height = img.size
    score = random.random()

    if score > 0.5:
        return "✅ Conservation NOT Needed"
    else:
        return "⚠️ Conservation Needed"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # get PORT from Render
    app.run(host="0.0.0.0", port=port)
