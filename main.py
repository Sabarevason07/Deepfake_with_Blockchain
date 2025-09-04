from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
import json
from time import time as current_time
import hashlib
from blockchain import Blockchain
from deepfake_detector import run as video_run  # Deepfake video analysis function
import importlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages

# Folder for uploaded videos
UPLOAD_FOLDER = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed video extensions (ensure "p4" is replaced by the correct "mp4" if needed)
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'mkv', 'flv', 'mpeg', '3gp', 'p4'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the blockchain
blockchain = Blockchain()

def generate_file_hash(file_path):
    """
    Generate a SHA-256 hash for a file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part in the request.")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash("No file selected.")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Save the uploaded file with a timestamp in its filename
        original_extension = file.filename.rsplit('.', 1)[1].lower()
        timestamp = int(current_time())
        filename = f"uploaded_video_{timestamp}.{original_extension}"
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)

        # Ensure the file is fully written before generating the hash
        file_hash = generate_file_hash(video_path)
        print("Generated file hash:", file_hash)  # Debug: Check the hash in console

        # Processed video path (we save processed videos as mp4 for consistency)
        video_path2 = os.path.join(app.config['UPLOAD_FOLDER'], f"processed_uploaded_video_{timestamp}.mp4")

        # --- Video Analysis ---
        video_accuracy = video_run(video_path, video_path2)

        # --- Audio Analysis ---
        audio_module = importlib.import_module("audio_analyzer")
        audio_function = getattr(audio_module, "analyze_audio")
        audio_accuracy = audio_function(video_path)

        # --- Combine Results ---
        final_accuracy = (video_accuracy + audio_accuracy) / 2
        final_result = "Fake" if final_accuracy > 50 else "Real"

        # Prepare video information
        video_info = {
            'name': file.filename,
            'size': f"{os.path.getsize(video_path) / 1024:.2f} KB",
            'user': 'Guest',
            'source': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
            'video_accuracy': video_accuracy,
            'audio_accuracy': audio_accuracy,
            'final_accuracy': final_accuracy,
            'final_result': final_result,
            'file_hash': file_hash
        }

        # Record analysis in the blockchain (now including uploader and location)
        blockchain.new_transaction(
            video_info['name'], 
            video_info['video_accuracy'],
            video_info['audio_accuracy'], 
            video_info['file_hash'],
            video_info['user'], 
            "Unknown"
        )
        blockchain.new_block(proof=12345)  # Demo proof value
        blockchain.log_ai_model(model_name="Deepfake Detector v1.0", dataset="DFDC", version="1.0")

        video_info_json = json.dumps(video_info)
        # Redirect to the result page, passing video information and processed video path
        return redirect(url_for('result', video_info=video_info_json, video_path2=video_path2))
    else:
        flash("File type not allowed. Please upload a video file with one of the following extensions: " + ", ".join(ALLOWED_EXTENSIONS))
        return redirect(request.url)

@app.route('/result')
def result():
    video_info_json = request.args.get('video_info')
    video_path2 = request.args.get('video_path2')
    video_info = json.loads(video_info_json)
    return render_template('result.html', video_url=video_path2, video_info=video_info, blockchain=blockchain)

@app.route('/blockchain')
def show_blockchain():
    """
    Display the blockchain data.
    """
    return {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

if __name__ == '__main__':
    app.run(debug=True)
