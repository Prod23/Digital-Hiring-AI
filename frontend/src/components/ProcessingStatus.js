import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  Alert,
  Card,
  CardContent,
  Stepper,
  Step,
  StepLabel,
  CircularProgress
} from '@mui/material';
import {
  VideoFile as VideoIcon,
  AudioFile as AudioIcon,
  Description as TextIcon,
  Assessment as ScoreIcon
} from '@mui/icons-material';
import axios from 'axios';

const ProcessingStatus = ({ processId, onComplete, onError }) => {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState('');
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    { label: 'Video Analysis', icon: <VideoIcon />, description: 'Analyzing facial expressions and emotions' },
    { label: 'Audio Analysis', icon: <AudioIcon />, description: 'Processing speech patterns and communication' },
    { label: 'Text Analysis', icon: <TextIcon />, description: 'Matching skills with job requirements' },
    { label: 'Score Calculation', icon: <ScoreIcon />, description: 'Generating final assessment' }
  ];

  useEffect(() => {
    if (!processId) return;

    const pollStatus = async () => {
      try {
        const response = await axios.get(`/status/${processId}`);
        const statusData = response.data;
        setStatus(statusData);

        // Update active step based on progress
        if (statusData.progress <= 25) {
          setActiveStep(0);
        } else if (statusData.progress <= 50) {
          setActiveStep(1);
        } else if (statusData.progress <= 75) {
          setActiveStep(2);
        } else if (statusData.progress < 100) {
          setActiveStep(3);
        }

        if (statusData.status === 'completed') {
          // Fetch results
          try {
            const resultsResponse = await axios.get(`/results/${processId}`);
            onComplete(resultsResponse.data);
          } catch (err) {
            setError('Failed to fetch results');
            onError();
          }
        } else if (statusData.status === 'error') {
          setError(statusData.message || 'Processing failed');
          onError();
        }
      } catch (err) {
        setError('Failed to check processing status');
        onError();
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    
    // Initial poll
    pollStatus();

    return () => clearInterval(interval);
  }, [processId, onComplete, onError]);

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      </Box>
    );
  }

  if (!status) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Processing Your Application
      </Typography>
      <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
        Our AI is analyzing your interview video, resume, and job requirements.
        This typically takes 2-5 minutes.
      </Typography>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Overall Progress
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {status.progress}%
            </Typography>
          </Box>
          
          <LinearProgress
            variant="determinate"
            value={status.progress}
            sx={{ height: 8, borderRadius: 4, mb: 2 }}
          />
          
          <Typography variant="body2" color="text.secondary">
            {status.message}
          </Typography>
        </CardContent>
      </Card>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Processing Steps
        </Typography>
        
        <Stepper activeStep={activeStep} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel
                icon={
                  index < activeStep ? (
                    <Box
                      sx={{
                        width: 24,
                        height: 24,
                        borderRadius: '50%',
                        backgroundColor: 'success.main',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontSize: '0.75rem'
                      }}
                    >
                      ✓
                    </Box>
                  ) : index === activeStep ? (
                    <CircularProgress size={24} />
                  ) : (
                    step.icon
                  )
                }
              >
                <Typography variant="subtitle1" sx={{ fontWeight: index <= activeStep ? 600 : 400 }}>
                  {step.label}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {step.description}
                </Typography>
              </StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      <Box sx={{ mt: 3, p: 2, backgroundColor: 'info.light', borderRadius: 1 }}>
        <Typography variant="body2" color="info.contrastText">
          <strong>What's happening:</strong> Our AI is analyzing multiple aspects of your application 
          including facial expressions, speech patterns, communication clarity, and skill alignment 
          with the job requirements.
        </Typography>
      </Box>
    </Box>
  );
};

export default ProcessingStatus;
