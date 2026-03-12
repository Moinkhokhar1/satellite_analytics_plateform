from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
from ndvi import calculate_indices

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    if 'file' not in request.files:
        return jsonify({"error":"No file uploaded"})

    file = request.files['file']
    filename = file.filename

    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    original, ndvi, ndwi, classification = calculate_indices(path)

    return jsonify({
        "original": f"http://127.0.0.1:5000/results/{original}",
        "ndvi": f"http://127.0.0.1:5000/results/{ndvi}",
        "ndwi": f"http://127.0.0.1:5000/results/{ndwi}",
        "classification": f"http://127.0.0.1:5000/results/{classification}"
    })

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory('results', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
