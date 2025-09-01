"""
Scoring Engine
Combines all processor results into individual and cumulative scores with explanations
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class ScoringEngine:
    def __init__(self):
        """Initialize scoring engine with weights and explanations"""
        # Scoring weights for cumulative score
        self.weights = {
            'video': 0.40,  # 40% weight for video emotion analysis
            'audio': 0.30,  # 30% weight for audio communication
            'text': 0.30    # 30% weight for text/skill matching
        }
        
        # Score explanations for UI
        self.explanations = {
            'emotion_score': {
                'title': 'Emotion & Confidence Score',
                'description': 'Measures emotional stability and confidence based on facial expressions during the interview.',
                'ranges': {
                    (80, 100): 'Excellent - Shows high confidence, positive demeanor, and emotional stability.',
                    (65, 79): 'Good - Demonstrates confidence with occasional neutral expressions.',
                    (50, 64): 'Average - Balanced emotional state with mixed expressions.',
                    (35, 49): 'Below Average - Shows signs of nervousness or uncertainty.',
                    (0, 34): 'Poor - Displays significant anxiety, fear, or negative emotions.'
                }
            },
            'audio_score': {
                'title': 'Communication & Speaking Skills',
                'description': 'Evaluates speaking clarity, confidence, and communication effectiveness.',
                'ranges': {
                    (85, 100): 'Excellent - Clear speech, minimal hesitation, positive tone.',
                    (70, 84): 'Good - Effective communication with minor filler words.',
                    (55, 69): 'Average - Adequate communication with some hesitation.',
                    (40, 54): 'Below Average - Frequent pauses, filler words, or unclear speech.',
                    (0, 39): 'Poor - Significant communication challenges, excessive hesitation.'
                }
            },
            'text_score': {
                'title': 'Skills & Qualifications Match',
                'description': 'Assesses how well candidate skills align with job requirements.',
                'ranges': {
                    (85, 100): 'Excellent - Strong alignment with job requirements and skills.',
                    (70, 84): 'Good - Most required skills present with good experience.',
                    (55, 69): 'Average - Some relevant skills but gaps in key areas.',
                    (40, 54): 'Below Average - Limited alignment with job requirements.',
                    (0, 39): 'Poor - Significant skill gaps and poor job fit.'
                }
            },
            'cumulative_score': {
                'title': 'Overall Candidate Score',
                'description': 'Weighted combination of all assessment metrics (40% emotion, 30% communication, 30% skills).',
                'ranges': {
                    (85, 100): 'Excellent Candidate - Highly recommended for the position.',
                    (70, 84): 'Good Candidate - Recommended with minor considerations.',
                    (55, 69): 'Average Candidate - Consider based on specific role needs.',
                    (40, 54): 'Below Average - May need additional training or different role.',
                    (0, 39): 'Poor Fit - Not recommended for this position.'
                }
            }
        }
    
    def get_score_explanation(self, score_type: str, score: float) -> Dict:
        """Get explanation for a specific score"""
        if score_type not in self.explanations:
            return {'title': 'Unknown Score', 'description': '', 'interpretation': ''}
        
        explanation = self.explanations[score_type]
        interpretation = ''
        
        # Find the appropriate range interpretation
        for (min_score, max_score), desc in explanation['ranges'].items():
            if min_score <= score <= max_score:
                interpretation = desc
                break
        
        return {
            'title': explanation['title'],
            'description': explanation['description'],
            'interpretation': interpretation
        }
    
    def calculate_scores(self, video_results: Dict, audio_results: Dict, text_results: Dict) -> Dict:
        """Calculate individual and cumulative scores from processor results"""
        try:
            # Extract individual scores
            emotion_score = video_results.get('emotion_score', 0.0)
            audio_score = audio_results.get('overall_audio_score', 0.0)
            text_score = text_results.get('overall_text_score', 0.0)
            
            # Calculate cumulative score
            cumulative_score = (
                emotion_score * self.weights['video'] +
                audio_score * self.weights['audio'] +
                text_score * self.weights['text']
            )
            
            # Generate score explanations
            emotion_explanation = self.get_score_explanation('emotion_score', emotion_score)
            audio_explanation = self.get_score_explanation('audio_score', audio_score)
            text_explanation = self.get_score_explanation('text_score', text_score)
            cumulative_explanation = self.get_score_explanation('cumulative_score', cumulative_score)
            
            return {
                'individual_scores': {
                    'emotion_score': {
                        'value': round(emotion_score, 2),
                        'explanation': emotion_explanation,
                        'weight': self.weights['video']
                    },
                    'audio_score': {
                        'value': round(audio_score, 2),
                        'explanation': audio_explanation,
                        'weight': self.weights['audio']
                    },
                    'text_score': {
                        'value': round(text_score, 2),
                        'explanation': text_explanation,
                        'weight': self.weights['text']
                    }
                },
                'cumulative_score': {
                    'value': round(cumulative_score, 2),
                    'explanation': cumulative_explanation,
                    'weights_used': self.weights
                }
            }
        except Exception as e:
            logger.error(f"Error calculating scores: {str(e)}")
            return {'error': str(e)}
    
    def generate_verdict(self, scores: Dict, video_results: Dict, 
                        audio_results: Dict, text_results: Dict) -> Dict:
        """Generate AI verdict based on all analysis results"""
        try:
            cumulative_score = scores['cumulative_score']['value']
            individual_scores = scores['individual_scores']
            
            # Determine overall recommendation
            if cumulative_score >= 85:
                recommendation = "HIGHLY RECOMMENDED"
                recommendation_color = "green"
            elif cumulative_score >= 70:
                recommendation = "RECOMMENDED"
                recommendation_color = "blue"
            elif cumulative_score >= 55:
                recommendation = "CONDITIONAL"
                recommendation_color = "orange"
            else:
                recommendation = "NOT RECOMMENDED"
                recommendation_color = "red"
            
            # Identify strengths
            strengths = []
            if individual_scores['emotion_score']['value'] >= 70:
                strengths.append("Strong emotional intelligence and confidence")
            if individual_scores['audio_score']['value'] >= 70:
                strengths.append("Excellent communication skills")
            if individual_scores['text_score']['value'] >= 70:
                strengths.append("Good alignment with job requirements")
            
            # Add specific strengths from detailed analysis
            if video_results.get('positive_count', 0) > video_results.get('negative_count', 0):
                strengths.append("Positive demeanor throughout interview")
            
            if audio_results.get('sentiment_analysis', {}).get('sentiment') == 'positive':
                strengths.append("Positive and enthusiastic communication")
            
            if text_results.get('resume_analysis', {}).get('technical_match', 0) >= 0.7:
                strengths.append("Strong technical skill alignment")
            
            # Identify areas for improvement
            improvements = []
            if individual_scores['emotion_score']['value'] < 50:
                improvements.append("Work on confidence and emotional regulation during interviews")
            if individual_scores['audio_score']['value'] < 50:
                improvements.append("Improve communication clarity and reduce hesitation")
            if individual_scores['text_score']['value'] < 50:
                improvements.append("Develop skills that better match job requirements")
            
            # Add specific improvements from detailed analysis
            if audio_results.get('filler_analysis', {}).get('filler_count', 0) > 10:
                improvements.append("Reduce use of filler words in speech")
            
            missing_skills = text_results.get('resume_analysis', {}).get('missing_technical_skills', [])
            if missing_skills:
                improvements.append(f"Consider developing skills in: {', '.join(missing_skills[:3])}")
            
            # Generate summary
            summary_parts = []
            
            if cumulative_score >= 85:
                summary_parts.append("This candidate demonstrates exceptional qualifications across all evaluation criteria.")
            elif cumulative_score >= 70:
                summary_parts.append("This candidate shows strong potential with good performance in most areas.")
            elif cumulative_score >= 55:
                summary_parts.append("This candidate has average qualifications with some areas needing attention.")
            else:
                summary_parts.append("This candidate may not be the best fit for this role at this time.")
            
            # Add specific insights
            highest_score = max(individual_scores.values(), key=lambda x: x['value'])
            lowest_score = min(individual_scores.values(), key=lambda x: x['value'])
            
            for score_name, score_data in individual_scores.items():
                if score_data == highest_score:
                    if score_name == 'emotion_score':
                        summary_parts.append("Shows excellent emotional stability and confidence.")
                    elif score_name == 'audio_score':
                        summary_parts.append("Demonstrates strong communication abilities.")
                    elif score_name == 'text_score':
                        summary_parts.append("Has excellent skill alignment with the role.")
                    break
            
            summary = " ".join(summary_parts)
            
            return {
                'recommendation': recommendation,
                'recommendation_color': recommendation_color,
                'summary': summary,
                'strengths': strengths[:5],  # Limit to top 5 strengths
                'improvements': improvements[:5],  # Limit to top 5 improvements
                'confidence_level': self._get_verdict_confidence(cumulative_score, individual_scores)
            }
            
        except Exception as e:
            logger.error(f"Error generating verdict: {str(e)}")
            return {
                'recommendation': 'ANALYSIS ERROR',
                'recommendation_color': 'gray',
                'summary': f'Unable to generate verdict due to error: {str(e)}',
                'strengths': [],
                'improvements': [],
                'confidence_level': 'Low'
            }
    
    def _get_verdict_confidence(self, cumulative_score: float, individual_scores: Dict) -> str:
        """Determine confidence level of the verdict"""
        # Check if scores are consistent (low variance)
        scores = [score_data['value'] for score_data in individual_scores.values()]
        score_variance = max(scores) - min(scores)
        
        if score_variance <= 15 and cumulative_score >= 70:
            return "High"
        elif score_variance <= 25 and cumulative_score >= 50:
            return "Medium"
        else:
            return "Low"
    
    def get_detailed_breakdown(self, video_results: Dict, audio_results: Dict, text_results: Dict) -> Dict:
        """Get detailed breakdown of all analysis components"""
        return {
            'video_analysis': {
                'emotion_counts': video_results.get('emotion_counts', {}),
                'confidence_level': video_results.get('confidence_level', 'Unknown'),
                'total_faces_detected': video_results.get('total_faces', 0)
            },
            'audio_analysis': {
                'communication_level': audio_results.get('communication_level', 'Unknown'),
                'sentiment': audio_results.get('sentiment_analysis', {}).get('sentiment', 'neutral'),
                'silence_ratio': audio_results.get('silence_analysis', {}).get('silence_ratio', 0),
                'filler_count': audio_results.get('filler_analysis', {}).get('filler_count', 0)
            },
            'text_analysis': {
                'skill_match_level': text_results.get('skill_match_level', 'Unknown'),
                'technical_skills_found': len(text_results.get('resume_analysis', {}).get('resume_skills', {}).get('technical_skills', [])),
                'soft_skills_found': len(text_results.get('resume_analysis', {}).get('resume_skills', {}).get('soft_skills', [])),
                'leetcode_score': text_results.get('leetcode_stats', {}).get('coding_score', 0)
            }
        }
