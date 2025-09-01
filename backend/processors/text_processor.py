"""
Text Analysis Processor
Handles resume analysis, job description matching, and skill assessment
"""

import os
import re
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import requests
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, leetcode_api_key: str = None):
        """Initialize text processor with optional LeetCode API key"""
        self.leetcode_api_key = leetcode_api_key
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        # Common technical skills keywords
        self.technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'django', 'flask', 'spring', 'sql', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning',
            'data science', 'artificial intelligence', 'deep learning', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'nlp',
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'devops',
            'ci/cd', 'jenkins', 'linux', 'unix', 'bash', 'powershell'
        ]
        
        # Soft skills keywords
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical', 'creative', 'adaptable', 'organized', 'detail oriented',
            'time management', 'project management', 'collaboration', 'mentoring',
            'presentation', 'negotiation', 'customer service', 'interpersonal'
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            return ""
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension == '.docx':
                return self.extract_text_from_docx(file_path)
            elif file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                logger.warning(f"Unsupported file format: {file_extension}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from file: {str(e)}")
            return ""
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        try:
            if not text1.strip() or not text2.strip():
                return 0.0
            
            # Vectorize texts
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    def extract_skills(self, text: str) -> Dict:
        """Extract technical and soft skills from text"""
        try:
            text_lower = text.lower()
            
            # Find technical skills
            found_technical = []
            for skill in self.technical_skills:
                if skill.lower() in text_lower:
                    found_technical.append(skill)
            
            # Find soft skills
            found_soft = []
            for skill in self.soft_skills:
                if skill.lower() in text_lower:
                    found_soft.append(skill)
            
            return {
                'technical_skills': found_technical,
                'soft_skills': found_soft,
                'total_skills': len(found_technical) + len(found_soft)
            }
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}")
            return {'technical_skills': [], 'soft_skills': [], 'total_skills': 0}
    
    def analyze_resume_job_match(self, resume_text: str, job_description: str) -> Dict:
        """Analyze how well resume matches job description"""
        try:
            # Calculate overall similarity
            overall_similarity = self.calculate_text_similarity(resume_text, job_description)
            
            # Extract skills from both texts
            resume_skills = self.extract_skills(resume_text)
            job_skills = self.extract_skills(job_description)
            
            # Calculate skill match percentage
            job_technical_skills = set(skill.lower() for skill in job_skills['technical_skills'])
            resume_technical_skills = set(skill.lower() for skill in resume_skills['technical_skills'])
            
            if job_technical_skills:
                technical_match = len(job_technical_skills.intersection(resume_technical_skills)) / len(job_technical_skills)
            else:
                technical_match = 0.0
            
            job_soft_skills = set(skill.lower() for skill in job_skills['soft_skills'])
            resume_soft_skills = set(skill.lower() for skill in resume_skills['soft_skills'])
            
            if job_soft_skills:
                soft_match = len(job_soft_skills.intersection(resume_soft_skills)) / len(job_soft_skills)
            else:
                soft_match = 0.0
            
            # Calculate weighted match score
            match_score = (
                overall_similarity * 0.4 +
                technical_match * 0.4 +
                soft_match * 0.2
            ) * 100
            
            return {
                'overall_similarity': round(overall_similarity, 4),
                'technical_match': round(technical_match, 4),
                'soft_match': round(soft_match, 4),
                'match_score': round(match_score, 2),
                'resume_skills': resume_skills,
                'job_skills': job_skills,
                'matching_technical_skills': list(job_technical_skills.intersection(resume_technical_skills)),
                'matching_soft_skills': list(job_soft_skills.intersection(resume_soft_skills)),
                'missing_technical_skills': list(job_technical_skills - resume_technical_skills),
                'missing_soft_skills': list(job_soft_skills - resume_soft_skills)
            }
        except Exception as e:
            logger.error(f"Error analyzing resume-job match: {str(e)}")
            return {'match_score': 0.0, 'error': str(e)}
    
    def analyze_transcript_job_match(self, transcript: str, job_description: str) -> Dict:
        """Analyze how well interview transcript matches job description"""
        try:
            # Calculate similarity between transcript and job description
            similarity = self.calculate_text_similarity(transcript, job_description)
            
            # Extract skills mentioned in transcript
            transcript_skills = self.extract_skills(transcript)
            job_skills = self.extract_skills(job_description)
            
            # Calculate comprehension score based on skill discussion
            comprehension_score = min(100, transcript_skills['total_skills'] * 10)  # Cap at 100
            
            # Calculate match score
            match_score = (similarity * 0.6 + (comprehension_score / 100) * 0.4) * 100
            
            return {
                'similarity': round(similarity, 4),
                'comprehension_score': round(comprehension_score, 2),
                'match_score': round(match_score, 2),
                'transcript_skills': transcript_skills,
                'job_skills': job_skills
            }
        except Exception as e:
            logger.error(f"Error analyzing transcript-job match: {str(e)}")
            return {'match_score': 0.0, 'error': str(e)}
    
    def get_leetcode_stats(self, username: str) -> Dict:
        """Get LeetCode statistics for a user (placeholder implementation)"""
        try:
            # Placeholder implementation - replace with actual LeetCode API call
            # Note: LeetCode doesn't have an official public API
            # You might need to use web scraping or third-party APIs
            
            # Mock data for demonstration
            mock_stats = {
                'username': username,
                'total_solved': 150,
                'easy_solved': 80,
                'medium_solved': 55,
                'hard_solved': 15,
                'acceptance_rate': 65.5,
                'ranking': 25000,
                'coding_score': 75.0  # Calculated based on problems solved
            }
            
            return mock_stats
        except Exception as e:
            logger.error(f"Error getting LeetCode stats: {str(e)}")
            return {'coding_score': 0.0, 'error': str(e)}
    
    def process_text_analysis(self, resume_path: str, job_description: str, 
                            transcript: str = "", leetcode_username: str = "") -> Dict:
        """Comprehensive text analysis combining all components"""
        try:
            # Extract resume text
            resume_text = self.extract_text_from_file(resume_path) if resume_path else ""
            
            # Analyze resume-job match
            resume_analysis = self.analyze_resume_job_match(resume_text, job_description)
            
            # Analyze transcript-job match if transcript is provided
            transcript_analysis = {}
            if transcript.strip():
                transcript_analysis = self.analyze_transcript_job_match(transcript, job_description)
            
            # Get LeetCode stats if username is provided
            leetcode_stats = {}
            if leetcode_username.strip():
                leetcode_stats = self.get_leetcode_stats(leetcode_username)
            
            # Calculate overall text score
            resume_weight = 0.5
            transcript_weight = 0.3
            leetcode_weight = 0.2
            
            overall_score = (
                resume_analysis.get('match_score', 0) * resume_weight +
                transcript_analysis.get('match_score', 0) * transcript_weight +
                leetcode_stats.get('coding_score', 0) * leetcode_weight
            )
            
            return {
                'resume_analysis': resume_analysis,
                'transcript_analysis': transcript_analysis,
                'leetcode_stats': leetcode_stats,
                'overall_text_score': round(overall_score, 2),
                'skill_match_level': self._get_skill_match_level(overall_score)
            }
        except Exception as e:
            logger.error(f"Error in text analysis: {str(e)}")
            return {'error': str(e), 'overall_text_score': 0.0}
    
    def _get_skill_match_level(self, score: float) -> str:
        """Get skill match level description based on score"""
        if score >= 85:
            return "Excellent Match"
        elif score >= 70:
            return "Good Match"
        elif score >= 55:
            return "Average Match"
        elif score >= 40:
            return "Below Average Match"
        else:
            return "Poor Match"
