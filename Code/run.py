import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: python run.py <video_path>")
    sys.exit(1)

# Get the video path from the command-line argument
video_path = sys.argv[1]

# Run image_frames.py with the video path as an argument
print("Running image_frames.py...")
subprocess.run(["python", "image_frames.py", video_path])

# Run main.py
print("Running main.py...")
subprocess.run(["python", "main.py"])
