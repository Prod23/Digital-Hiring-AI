import cv2
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python image_frames.py <video_path>")
    sys.exit(1)

# Get the video path from the command-line argument
video_path = sys.argv[1]

# Frame rate for sampling (e.g., 1 frame per second)
frame_rate = 3  # Adjust this value as needed

# Directory to save the frames as images
output_directory = '/Users/rishirajdatta7/Desktop/frames'  # Replace with your desired directory name

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Create a VideoCapture object to open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit(1)

frame_number = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        break

    # Sample frames based on frame rate
    if frame_number % int(cap.get(cv2.CAP_PROP_FPS) / frame_rate) == 0:
        # Define the file path to save the frame as an image
        output_filename = os.path.join(output_directory, f'frame_{frame_number}.jpg')

        # Save the frame as an image
        cv2.imwrite(output_filename, frame)

        # Display the frame (optional)
        cv2.imshow('Video Frame', frame)

    frame_number += 1

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()

