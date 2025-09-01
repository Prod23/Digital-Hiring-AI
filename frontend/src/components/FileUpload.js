import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Grid,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  VideoFile as VideoFileIcon,
  Description as DescriptionIcon
} from '@mui/icons-material';
import axios from 'axios';

const FileUpload = ({ onUploadSuccess }) => {
  const [videoFile, setVideoFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [leetcodeUsername, setLeetcodeUsername] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const onVideoDropAccepted = (acceptedFiles) => {
    setVideoFile(acceptedFiles[0]);
    setError('');
  };

  const onResumeDropAccepted = (acceptedFiles) => {
    setResumeFile(acceptedFiles[0]);
    setError('');
  };

  const {
    getRootProps: getVideoRootProps,
    getInputProps: getVideoInputProps,
    isDragActive: isVideoDragActive
  } = useDropzone({
    onDrop: onVideoDropAccepted,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.mkv']
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false
  });

  const {
    getRootProps: getResumeRootProps,
    getInputProps: getResumeInputProps,
    isDragActive: isResumeDragActive
  } = useDropzone({
    onDrop: onResumeDropAccepted,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  });

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleSubmit = async () => {
    if (!videoFile || !resumeFile || !jobDescription.trim()) {
      setError('Please provide all required files and job description.');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('video', videoFile);
      formData.append('resume', resumeFile);
      formData.append('job_description', jobDescription);
      if (leetcodeUsername.trim()) {
        formData.append('leetcode_username', leetcodeUsername);
      }

      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onUploadSuccess(response.data.process_id);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Upload failed. Please check your files and try again.'
      );
    } finally {
      setUploading(false);
    }
  };

  const removeVideoFile = () => {
    setVideoFile(null);
  };

  const removeResumeFile = () => {
    setResumeFile(null);
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        AI-Powered Candidate Evaluation
      </Typography>
      <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 4 }}>
        Upload candidate materials for comprehensive AI analysis including emotion detection,
        communication assessment, and skill matching.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Video Upload */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <VideoFileIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Interview Video
              </Typography>
              
              {!videoFile ? (
                <Paper
                  {...getVideoRootProps()}
                  sx={{
                    p: 3,
                    textAlign: 'center',
                    cursor: 'pointer',
                    border: '2px dashed',
                    borderColor: isVideoDragActive ? 'primary.main' : 'grey.300',
                    backgroundColor: isVideoDragActive ? 'action.hover' : 'background.paper',
                    '&:hover': {
                      borderColor: 'primary.main',
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <input {...getVideoInputProps()} />
                  <CloudUploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" gutterBottom>
                    {isVideoDragActive
                      ? 'Drop the video file here...'
                      : 'Drag & drop interview video here, or click to select'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Supported formats: MP4, AVI, MOV, MKV (Max: 50MB)
                  </Typography>
                </Paper>
              ) : (
                <Box sx={{ p: 2, backgroundColor: 'success.light', borderRadius: 1 }}>
                  <Typography variant="body2" gutterBottom>
                    <strong>{videoFile.name}</strong>
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Size: {formatFileSize(videoFile.size)}
                  </Typography>
                  <Button size="small" onClick={removeVideoFile} color="error">
                    Remove
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Resume Upload */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <DescriptionIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Resume/CV
              </Typography>
              
              {!resumeFile ? (
                <Paper
                  {...getResumeRootProps()}
                  sx={{
                    p: 3,
                    textAlign: 'center',
                    cursor: 'pointer',
                    border: '2px dashed',
                    borderColor: isResumeDragActive ? 'primary.main' : 'grey.300',
                    backgroundColor: isResumeDragActive ? 'action.hover' : 'background.paper',
                    '&:hover': {
                      borderColor: 'primary.main',
                      backgroundColor: 'action.hover',
                    },
                  }}
                >
                  <input {...getResumeInputProps()} />
                  <CloudUploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" gutterBottom>
                    {isResumeDragActive
                      ? 'Drop the resume file here...'
                      : 'Drag & drop resume here, or click to select'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Supported formats: PDF, DOCX, TXT (Max: 10MB)
                  </Typography>
                </Paper>
              ) : (
                <Box sx={{ p: 2, backgroundColor: 'success.light', borderRadius: 1 }}>
                  <Typography variant="body2" gutterBottom>
                    <strong>{resumeFile.name}</strong>
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Size: {formatFileSize(resumeFile.size)}
                  </Typography>
                  <Button size="small" onClick={removeResumeFile} color="error">
                    Remove
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Job Description */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Job Description
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={6}
                variant="outlined"
                placeholder="Paste the job description here. Include required skills, responsibilities, and qualifications..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                required
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Optional LeetCode Username */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                LeetCode Username
                <Chip label="Optional" size="small" sx={{ ml: 1 }} />
              </Typography>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Enter LeetCode username for coding assessment"
                value={leetcodeUsername}
                onChange={(e) => setLeetcodeUsername(e.target.value)}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Used to evaluate coding skills and problem-solving abilities
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Submit Button */}
        <Grid item xs={12}>
          <Box sx={{ textAlign: 'center', mt: 3 }}>
            <Button
              variant="contained"
              size="large"
              onClick={handleSubmit}
              disabled={uploading || !videoFile || !resumeFile || !jobDescription.trim()}
              sx={{ minWidth: 200, py: 1.5 }}
            >
              {uploading ? (
                <>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  Processing...
                </>
              ) : (
                'Start AI Analysis'
              )}
            </Button>
          </Box>
          
          {(videoFile || resumeFile || jobDescription) && (
            <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 2 }}>
              Analysis includes: Emotion Detection • Communication Assessment • Skill Matching
            </Typography>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default FileUpload;
