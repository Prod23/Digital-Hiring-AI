from flask import Flask, jsonify, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/run_app')
def process_video_and_run_main():
    # Get the video path from the URL parameter
    video_path = request.args.get('video_path')

    if not video_path:
        return jsonify({"message": "Video path not provided."}), 400

    # Run image_frames.py with the video path as an argument
    print("Running image_frames.py...")
    subprocess.run(["python", "image_frames.py", video_path])

    # Run main.py
    print("Running main.py...")
    subprocess.run(["python", "main.py"])
    
    # You can return a JSON response or any other response here
    return jsonify({"message": "Processing video and running main."})

@app.route('/')
def hello_world():
    return 'Hey'

if __name__ == '__main__':
    app.run(debug=True,port = 5001)

