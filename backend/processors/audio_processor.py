"""
Audio Analysis Processor
Handles audio transcription, silence analysis, emotion analysis, and filler word detection
"""

import os
import tempfile
import librosa
import numpy as np
from typing import Dict, List, Tuple
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self):
        """Initialize audio processor with sentiment analyzer and filler words"""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Common filler words and hesitation patterns
        self.filler_words = [
            'um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well',
            'actually', 'basically', 'literally', 'totally', 'really',
            'kind of', 'sort of', 'i mean', 'you see', 'right'
        ]
        
        # Silence threshold in seconds
        self.silence_threshold = 3.0
    
    def extract_audio_from_video(self, video_path: str) -> str:
        """Extract audio from video file"""
        try:
            temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            # Use librosa to load video and extract audio
            y, sr = librosa.load(video_path, sr=None)
            librosa.output.write_wav(temp_audio_path, y, sr)
            
            return temp_audio_path
            
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio to text using Whisper
        Note: This is a placeholder - in production, you'd use OpenAI Whisper API
        or run Whisper locally
        """
        try:
            # Placeholder transcription - replace with actual Whisper implementation
            # For now, return a sample transcript for testing
            sample_transcript = """
            Hello, my name is John Doe and I am applying for the software engineer position.
            I have five years of experience in Python development and machine learning.
            I have worked on various projects including web applications and data analysis.
            I am passionate about technology and always eager to learn new things.
            In my previous role, I developed several REST APIs and worked with databases.
            I believe I would be a great fit for this position because of my technical skills
            and my ability to work well in a team environment.
            """
            
            # TODO: Implement actual Whisper transcription
            # import whisper
            # model = whisper.load_model("base")
            # result = model.transcribe(audio_path)
            # return result["text"]
            
            return sample_transcript.strip()
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return ""
    
    def analyze_silence(self, audio_path: str) -> Dict:
        """Analyze silence patterns in audio"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path)
            
            # Calculate RMS energy
            rms = librosa.feature.rms(y=y)[0]
            
            # Define silence threshold (adjust based on your needs)
            silence_threshold = 0.01
            
            # Find silent segments
            silent_frames = rms < silence_threshold
            
            # Convert frames to time
            frame_length = len(y) / len(rms)
            silent_segments = []
            current_silence_start = None
            
            for i, is_silent in enumerate(silent_frames):
                time = i * frame_length / sr
                
                if is_silent and current_silence_start is None:
                    current_silence_start = time
                elif not is_silent and current_silence_start is not None:
                    silence_duration = time - current_silence_start
                    if silence_duration >= self.silence_threshold:
                        silent_segments.append({
                            'start': current_silence_start,
                            'end': time,
                            'duration': silence_duration
                        })
                    current_silence_start = None
            
            # Calculate silence metrics
            total_silence_duration = sum(seg['duration'] for seg in silent_segments)
            total_duration = len(y) / sr
            silence_ratio = total_silence_duration / total_duration if total_duration > 0 else 0
            
            # Confidence score based on silence (less silence = higher confidence)
            confidence_score = max(0, 100 - (silence_ratio * 100))
            
            return {
                'silent_segments': silent_segments,
                'total_silence_duration': total_silence_duration,
                'total_duration': total_duration,
                'silence_ratio': silence_ratio,
                'confidence_score': round(confidence_score, 2)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing silence: {str(e)}")
            return {'confidence_score': 50.0, 'error': str(e)}
    
    def analyze_sentiment(self, transcript: str) -> Dict:
        """Analyze sentiment of transcript using VADER"""
        try:
            if not transcript.strip():
                return {'sentiment_score': 50.0, 'sentiment': 'neutral'}
            
            # VADER sentiment analysis
            vader_scores = self.sentiment_analyzer.polarity_scores(transcript)
            
            # TextBlob sentiment analysis for comparison
            blob = TextBlob(transcript)
            textblob_polarity = blob.sentiment.polarity
            
            # Combine scores (VADER is more suitable for social media text)
            combined_score = (vader_scores['compound'] + textblob_polarity) / 2
            
            # Convert to 0-100 scale
            sentiment_score = ((combined_score + 1) / 2) * 100
            
            # Determine sentiment category
            if sentiment_score >= 60:
                sentiment = 'positive'
            elif sentiment_score <= 40:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment_score': round(sentiment_score, 2),
                'sentiment': sentiment,
                'vader_scores': vader_scores,
                'textblob_polarity': textblob_polarity
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {'sentiment_score': 50.0, 'sentiment': 'neutral', 'error': str(e)}
    
    def analyze_filler_words(self, transcript: str) -> Dict:
        """Analyze filler words and hesitation patterns"""
        try:
            if not transcript.strip():
                return {'filler_score': 100.0, 'filler_count': 0}
            
            # Convert to lowercase for analysis
            text_lower = transcript.lower()
            words = text_lower.split()
            total_words = len(words)
            
            if total_words == 0:
                return {'filler_score': 100.0, 'filler_count': 0}
            
            # Count filler words
            filler_count = 0
            filler_details = {}
            
            for filler in self.filler_words:
                if ' ' in filler:  # Multi-word fillers
                    count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
                else:  # Single word fillers
                    count = text_lower.split().count(filler)
                
                if count > 0:
                    filler_details[filler] = count
                    filler_count += count
            
            # Calculate filler ratio
            filler_ratio = filler_count / total_words
            
            # Score based on filler ratio (less fillers = higher score)
            filler_score = max(0, 100 - (filler_ratio * 200))  # Penalize heavily for fillers
            
            return {
                'filler_score': round(filler_score, 2),
                'filler_count': filler_count,
                'total_words': total_words,
                'filler_ratio': round(filler_ratio, 4),
                'filler_details': filler_details
            }
            
        except Exception as e:
            logger.error(f"Error analyzing filler words: {str(e)}")
            return {'filler_score': 50.0, 'filler_count': 0, 'error': str(e)}
    
    def process_audio(self, video_path: str) -> Dict:
        """Process audio from video and return comprehensive analysis"""
        try:
            # Extract audio from video
            audio_path = self.extract_audio_from_video(video_path)
            
            # Transcribe audio
            transcript = self.transcribe_audio(audio_path)
            
            # Perform various analyses
            silence_analysis = self.analyze_silence(audio_path)
            sentiment_analysis = self.analyze_sentiment(transcript)
            filler_analysis = self.analyze_filler_words(transcript)
            
            # Calculate overall audio confidence score (weighted average)
            silence_weight = 0.4
            sentiment_weight = 0.3
            filler_weight = 0.3
            
            overall_score = (
                silence_analysis.get('confidence_score', 50) * silence_weight +
                sentiment_analysis.get('sentiment_score', 50) * sentiment_weight +
                filler_analysis.get('filler_score', 50) * filler_weight
            )
            
            # Clean up temporary audio file
            try:
                os.unlink(audio_path)
            except:
                pass
            
            return {
                'transcript': transcript,
                'silence_analysis': silence_analysis,
                'sentiment_analysis': sentiment_analysis,
                'filler_analysis': filler_analysis,
                'overall_audio_score': round(overall_score, 2),
                'communication_level': self._get_communication_level(overall_score)
            }
            
        except Exception as e:
            logger.error(f"Error processing audio: {str(e)}")
            return {'error': str(e), 'overall_audio_score': 0.0}
    
    def _get_communication_level(self, score: float) -> str:
        """Get communication level description based on score"""
        if score >= 85:
            return "Excellent Communication"
        elif score >= 70:
            return "Good Communication"
        elif score >= 55:
            return "Average Communication"
        elif score >= 40:
            return "Below Average Communication"
        else:
            return "Poor Communication"
