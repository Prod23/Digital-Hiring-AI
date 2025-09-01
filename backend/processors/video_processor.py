"""
Video Emotion Detection Processor
Extracts frames from video and analyzes facial emotions using CNN model
"""

import cv2
import os
import numpy as np
import tempfile
from typing import Dict, List, Tuple
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, model_path: str = None, cascade_path: str = None):
        """Initialize video processor with model and cascade classifier"""
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        
        # Load face classifier
        if cascade_path and os.path.exists(cascade_path):
            self.face_classifier = cv2.CascadeClassifier(cascade_path)
        else:
            # Try default OpenCV cascade
            cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
            default_path = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
            self.face_classifier = cv2.CascadeClassifier(default_path)
        
        # Load emotion detection model
        if model_path and os.path.exists(model_path):
            self.classifier = load_model(model_path)
        else:
            raise FileNotFoundError("Emotion detection model not found")
    
    def extract_frames(self, video_path: str, frame_rate: int = 3) -> List[str]:
        """Extract frames from video at specified frame rate"""
        temp_dir = tempfile.mkdtemp()
        frame_paths = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps / frame_rate) if fps > 0 else 30
            frame_number = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_number % frame_interval == 0:
                    frame_path = os.path.join(temp_dir, f'frame_{frame_number}.jpg')
                    cv2.imwrite(frame_path, frame)
                    frame_paths.append(frame_path)
                
                frame_number += 1
            
            cap.release()
            return frame_paths
            
        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            raise
    
    def detect_emotions_in_frame(self, frame_path: str) -> List[str]:
        """Detect emotions in a single frame"""
        emotions = []
        
        try:
            frame = cv2.imread(frame_path)
            if frame is None:
                return emotions
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                
                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)
                    
                    prediction = self.classifier.predict(roi)[0]
                    emotion = self.emotion_labels[prediction.argmax()]
                    emotions.append(emotion)
            
            return emotions
            
        except Exception as e:
            logger.error(f"Error detecting emotions in frame {frame_path}: {str(e)}")
            return emotions
    
    def process_video(self, video_path: str) -> Dict:
        """Process entire video and return emotion analysis"""
        try:
            # Extract frames
            frame_paths = self.extract_frames(video_path)
            
            if not frame_paths:
                return {"error": "No frames extracted from video"}
            
            # Initialize emotion counts
            emotion_count = {label: 0 for label in self.emotion_labels}
            total_faces = 0
            
            # Process each frame
            for frame_path in frame_paths:
                emotions = self.detect_emotions_in_frame(frame_path)
                for emotion in emotions:
                    emotion_count[emotion] += 1
                    total_faces += 1
            
            # Clean up temporary files
            for frame_path in frame_paths:
                try:
                    os.remove(frame_path)
                except:
                    pass
            
            if total_faces == 0:
                return {"error": "No faces detected in video"}
            
            # Calculate scores
            positive_emotions = emotion_count['Happy'] + emotion_count['Surprise']
            negative_emotions = (emotion_count['Angry'] + emotion_count['Disgust'] + 
                               emotion_count['Fear'] + emotion_count['Sad'])
            neutral_emotions = emotion_count['Neutral']
            
            # Emotion score calculation (0-100 scale)
            emotion_score = self._calculate_emotion_score(positive_emotions, negative_emotions, neutral_emotions)
            
            return {
                "emotion_counts": emotion_count,
                "total_faces": total_faces,
                "positive_count": positive_emotions,
                "negative_count": negative_emotions,
                "neutral_count": neutral_emotions,
                "emotion_score": emotion_score,
                "confidence_level": self._get_confidence_level(emotion_score)
            }
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_emotion_score(self, positive: int, negative: int, neutral: int) -> float:
        """Calculate emotion score on 0-100 scale"""
        total = positive + negative + neutral
        if total == 0:
            return 50.0  # Neutral score if no emotions detected
        
        # Weighted score: positive emotions boost score, negative reduce it, neutral is slightly negative
        weighted_score = positive - negative + (neutral * -0.5)
        
        # Normalize to 0-100 scale
        max_possible = total  # If all emotions were positive
        min_possible = -total  # If all emotions were negative
        
        # Map to 0-100 scale
        normalized_score = ((weighted_score - min_possible) / (max_possible - min_possible)) * 100
        
        return round(max(0, min(100, normalized_score)), 2)
    
    def _get_confidence_level(self, score: float) -> str:
        """Get confidence level description based on score"""
        if score >= 80:
            return "Very Confident"
        elif score >= 65:
            return "Confident"
        elif score >= 50:
            return "Moderately Confident"
        elif score >= 35:
            return "Low Confidence"
        else:
            return "Very Low Confidence"
