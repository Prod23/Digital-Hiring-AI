import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import ResultsDisplay from './components/ResultsDisplay';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [processId, setProcessId] = useState(null);
  const [currentStep, setCurrentStep] = useState('upload'); // upload, processing, results
  const [results, setResults] = useState(null);

  const handleUploadSuccess = (id) => {
    setProcessId(id);
    setCurrentStep('processing');
  };

  const handleProcessingComplete = (resultData) => {
    setResults(resultData);
    setCurrentStep('results');
  };

  const handleStartOver = () => {
    setProcessId(null);
    setCurrentStep('upload');
    setResults(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <AppBar position="static" elevation={2}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Digital Hiring - AI Candidate Evaluation
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="lg" className="main-content">
          <Box sx={{ py: 4 }}>
            {currentStep === 'upload' && (
              <FileUpload onUploadSuccess={handleUploadSuccess} />
            )}

            {currentStep === 'processing' && (
              <ProcessingStatus
                processId={processId}
                onComplete={handleProcessingComplete}
                onError={() => setCurrentStep('upload')}
              />
            )}

            {currentStep === 'results' && (
              <ResultsDisplay
                results={results}
                onStartOver={handleStartOver}
              />
            )}
          </Box>
        </Container>

        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[200]
                : theme.palette.grey[800],
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body2" color="text.secondary" align="center">
              © 2024 Digital Hiring System. Powered by AI.
            </Typography>
          </Container>
        </Box>
      </div>
    </ThemeProvider>
  );
}

export default App;
