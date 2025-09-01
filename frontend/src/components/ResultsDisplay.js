import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  LinearProgress
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  Psychology as PsychologyIcon,
  RecordVoiceOver as VoiceIcon,
  Assignment as AssignmentIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const ResultsDisplay = ({ results, onStartOver }) => {
  const [expandedPanel, setExpandedPanel] = useState(false);

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedPanel(isExpanded ? panel : false);
  };

  const getScoreColor = (score) => {
    if (score >= 85) return '#4caf50'; // Green
    if (score >= 70) return '#2196f3'; // Blue
    if (score >= 55) return '#ff9800'; // Orange
    return '#f44336'; // Red
  };

  const getRecommendationStyle = (recommendation) => {
    const styles = {
      'HIGHLY RECOMMENDED': { backgroundColor: '#e8f5e8', color: '#2e7d32' },
      'RECOMMENDED': { backgroundColor: '#e3f2fd', color: '#1565c0' },
      'CONDITIONAL': { backgroundColor: '#fff3e0', color: '#ef6c00' },
      'NOT RECOMMENDED': { backgroundColor: '#ffebee', color: '#c62828' }
    };
    return styles[recommendation] || styles['CONDITIONAL'];
  };

  // Prepare chart data
  const scoresChartData = {
    labels: ['Emotion & Confidence', 'Communication', 'Skills Match'],
    datasets: [
      {
        label: 'Score',
        data: [
          results.scores.individual_scores.emotion_score.value,
          results.scores.individual_scores.audio_score.value,
          results.scores.individual_scores.text_score.value
        ],
        backgroundColor: [
          getScoreColor(results.scores.individual_scores.emotion_score.value),
          getScoreColor(results.scores.individual_scores.audio_score.value),
          getScoreColor(results.scores.individual_scores.text_score.value)
        ],
        borderRadius: 8,
      }
    ]
  };

  const cumulativeScoreData = {
    labels: ['Score', 'Remaining'],
    datasets: [
      {
        data: [results.scores.cumulative_score.value, 100 - results.scores.cumulative_score.value],
        backgroundColor: [
          getScoreColor(results.scores.cumulative_score.value),
          '#e0e0e0'
        ],
        borderWidth: 0,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        }
      }
    }
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    },
    cutout: '70%'
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Candidate Evaluation Results
      </Typography>

      {/* Overall Verdict */}
      <Card sx={{ mb: 4, border: `2px solid ${results.verdict.recommendation_color}` }}>
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <Chip
            label={results.verdict.recommendation}
            sx={{
              ...getRecommendationStyle(results.verdict.recommendation),
              fontSize: '1rem',
              fontWeight: 'bold',
              py: 2,
              px: 3,
              mb: 2
            }}
          />
          
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
            Overall Score: {results.scores.cumulative_score.value}%
          </Typography>
          
          <Box sx={{ position: 'relative', width: 200, height: 200, mx: 'auto', mb: 3 }}>
            <Doughnut data={cumulativeScoreData} options={doughnutOptions} />
            <Box
              sx={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center'
              }}
            >
              <Typography variant="h4" sx={{ fontWeight: 'bold', color: getScoreColor(results.scores.cumulative_score.value) }}>
                {results.scores.cumulative_score.value}%
              </Typography>
            </Box>
          </Box>
          
          <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            {results.verdict.summary}
          </Typography>
        </CardContent>
      </Card>

      {/* Individual Scores */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <PsychologyIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Emotion & Confidence
              </Typography>
              <Typography 
                variant="h4" 
                sx={{ 
                  fontWeight: 'bold', 
                  color: getScoreColor(results.scores.individual_scores.emotion_score.value),
                  mb: 1 
                }}
              >
                {results.scores.individual_scores.emotion_score.value}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={results.scores.individual_scores.emotion_score.value}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'grey.200',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: getScoreColor(results.scores.individual_scores.emotion_score.value)
                  }
                }}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Weight: {(results.scores.individual_scores.emotion_score.weight * 100).toFixed(0)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <VoiceIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Communication
              </Typography>
              <Typography 
                variant="h4" 
                sx={{ 
                  fontWeight: 'bold', 
                  color: getScoreColor(results.scores.individual_scores.audio_score.value),
                  mb: 1 
                }}
              >
                {results.scores.individual_scores.audio_score.value}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={results.scores.individual_scores.audio_score.value}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'grey.200',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: getScoreColor(results.scores.individual_scores.audio_score.value)
                  }
                }}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Weight: {(results.scores.individual_scores.audio_score.weight * 100).toFixed(0)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <AssignmentIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Skills Match
              </Typography>
              <Typography 
                variant="h4" 
                sx={{ 
                  fontWeight: 'bold', 
                  color: getScoreColor(results.scores.individual_scores.text_score.value),
                  mb: 1 
                }}
              >
                {results.scores.individual_scores.text_score.value}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={results.scores.individual_scores.text_score.value}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'grey.200',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: getScoreColor(results.scores.individual_scores.text_score.value)
                  }
                }}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Weight: {(results.scores.individual_scores.text_score.weight * 100).toFixed(0)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Scores Chart */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Score Breakdown
          </Typography>
          <Box sx={{ height: 300 }}>
            <Bar data={scoresChartData} options={chartOptions} />
          </Box>
        </CardContent>
      </Card>

      {/* Strengths and Improvements */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckCircleIcon sx={{ mr: 1, color: 'success.main' }} />
                Key Strengths
              </Typography>
              <List>
                {results.verdict.strengths.map((strength, index) => (
                  <ListItem key={index} sx={{ py: 0.5 }}>
                    <ListItemIcon>
                      <TrendingUpIcon sx={{ color: 'success.main' }} />
                    </ListItemIcon>
                    <ListItemText primary={strength} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <WarningIcon sx={{ mr: 1, color: 'warning.main' }} />
                Areas for Improvement
              </Typography>
              <List>
                {results.verdict.improvements.map((improvement, index) => (
                  <ListItem key={index} sx={{ py: 0.5 }}>
                    <ListItemIcon>
                      <WarningIcon sx={{ color: 'warning.main' }} />
                    </ListItemIcon>
                    <ListItemText primary={improvement} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Detailed Analysis Accordions */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Detailed Analysis
      </Typography>

      {/* Emotion Analysis */}
      <Accordion expanded={expandedPanel === 'emotion'} onChange={handleAccordionChange('emotion')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Emotion & Confidence Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" color="text.secondary" paragraph>
            {results.scores.individual_scores.emotion_score.explanation.description}
          </Typography>
          <Typography variant="body1" paragraph>
            <strong>Assessment:</strong> {results.scores.individual_scores.emotion_score.explanation.interpretation}
          </Typography>
          <Typography variant="body2">
            <strong>Confidence Level:</strong> {results.breakdown.video_analysis.confidence_level}
          </Typography>
          <Typography variant="body2">
            <strong>Faces Detected:</strong> {results.breakdown.video_analysis.total_faces_detected}
          </Typography>
        </AccordionDetails>
      </Accordion>

      {/* Communication Analysis */}
      <Accordion expanded={expandedPanel === 'communication'} onChange={handleAccordionChange('communication')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Communication Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" color="text.secondary" paragraph>
            {results.scores.individual_scores.audio_score.explanation.description}
          </Typography>
          <Typography variant="body1" paragraph>
            <strong>Assessment:</strong> {results.scores.individual_scores.audio_score.explanation.interpretation}
          </Typography>
          <Typography variant="body2">
            <strong>Communication Level:</strong> {results.breakdown.audio_analysis.communication_level}
          </Typography>
          <Typography variant="body2">
            <strong>Sentiment:</strong> {results.breakdown.audio_analysis.sentiment}
          </Typography>
          <Typography variant="body2">
            <strong>Filler Words:</strong> {results.breakdown.audio_analysis.filler_count}
          </Typography>
        </AccordionDetails>
      </Accordion>

      {/* Skills Analysis */}
      <Accordion expanded={expandedPanel === 'skills'} onChange={handleAccordionChange('skills')}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Skills & Qualifications Analysis</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="body2" color="text.secondary" paragraph>
            {results.scores.individual_scores.text_score.explanation.description}
          </Typography>
          <Typography variant="body1" paragraph>
            <strong>Assessment:</strong> {results.scores.individual_scores.text_score.explanation.interpretation}
          </Typography>
          <Typography variant="body2">
            <strong>Skill Match Level:</strong> {results.breakdown.text_analysis.skill_match_level}
          </Typography>
          <Typography variant="body2">
            <strong>Technical Skills Found:</strong> {results.breakdown.text_analysis.technical_skills_found}
          </Typography>
          <Typography variant="body2">
            <strong>Soft Skills Found:</strong> {results.breakdown.text_analysis.soft_skills_found}
          </Typography>
          <Typography variant="body2">
            <strong>Coding Score:</strong> {results.breakdown.text_analysis.leetcode_score}%
          </Typography>
        </AccordionDetails>
      </Accordion>

      <Divider sx={{ my: 4 }} />

      {/* Action Buttons */}
      <Box sx={{ textAlign: 'center' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<RefreshIcon />}
          onClick={onStartOver}
          sx={{ minWidth: 200 }}
        >
          Evaluate Another Candidate
        </Button>
      </Box>
    </Box>
  );
};

export default ResultsDisplay;
