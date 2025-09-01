# Digital Hiring - AI Candidate Evaluation

![Digital Hiring App Screenshot](app_screenshot.png)

A comprehensive, production-ready web application that evaluates job candidates using AI analysis of video interviews, resumes, and job descriptions. This system provides objective, data-driven insights to streamline the hiring process.

## 🚀 Key Features

### Core Capabilities
- **Video Emotion Analysis**: CNN-based facial expression detection to assess confidence and emotional stability
- **Audio Communication Assessment**: Speech pattern analysis including silence detection, sentiment analysis, and filler word identification  
- **Text & Skills Matching**: Semantic analysis of resumes against job descriptions with skill gap identification
- **LeetCode Integration**: Coding ability assessment through LeetCode profile analysis
- **Comprehensive Scoring**: Weighted scoring system with individual metrics and cumulative evaluation
- **AI-Generated Verdicts**: Intelligent recommendations with strengths and improvement areas

## 🎯 How to Use

### 1. Upload Candidate Materials
- **Interview Video**: Record or upload a video interview (MP4, MOV, or AVI format)
- **Resume/CV**: Upload the candidate's resume in PDF or DOCX format
- **Job Description**: Paste the job description text or upload a document
- **LeetCode Username**: (Optional) Enter the candidate's LeetCode username for coding assessment

### 2. Processing and Analysis
- The system will automatically process all uploaded materials
- Real-time progress tracking is displayed during analysis
- Processing time depends on video length and system resources

### 3. Review Results
- **Dashboard**: View the overall score and key metrics at a glance
- **Detailed Breakdown**: Explore individual component scores (Video, Audio, Text)
- **AI Verdict**: Read the comprehensive assessment and recommendations
- **Comparison**: Compare multiple candidates side by side (pro feature)

### 4. Make Decisions
- Use the scoring system to shortlist candidates
- Review detailed feedback for interview questions
- Export reports for record-keeping and sharing

### Technical Features
- **Modern Web Interface**: React.js frontend with Material-UI components
- **RESTful API**: FastAPI backend with async processing
- **Real-time Progress**: Live status updates during processing
- **File Upload Support**: Drag-and-drop interface for videos (.mp4, .avi, .mov) and resumes (.pdf, .docx, .txt)
- **Responsive Design**: Mobile-friendly interface
- **Docker Ready**: Containerized deployment with docker-compose
- **Production Security**: Input validation, file size limits, CORS protection

## 🧩 Scoring System & Components

### 1. Video Emotion Analysis (40% weight)
- **Emotion Detection**: Analyzes facial expressions to detect emotions (happy, neutral, surprised, etc.)
- **Engagement Score**: Measures candidate's engagement level throughout the interview
- **Confidence Indicators**: Assesses non-verbal confidence cues
- **Key Metrics**:
  - Positive emotion ratio
  - Engagement consistency
  - Eye contact analysis
  - Posture and body language

### 2. Audio Communication Assessment (30% weight)
- **Speech Clarity**: Evaluates speech clarity and pace
- **Sentiment Analysis**: Assesses positive/negative sentiment in responses
- **Filler Word Detection**: Identifies and counts filler words ("um", "uh", etc.)
- **Silence Analysis**: Measures response times and awkward pauses
- **Key Metrics**:
  - Words per minute
  - Filler word frequency
  - Sentiment score
  - Response time consistency

### 3. Text & Skills Matching (30% weight)
- **Resume Parsing**: Extracts skills, experience, and education
- **Job Description Matching**: Compares candidate's profile with job requirements
- **Keyword Analysis**: Identifies key terms and their relevance
- **LeetCode Integration**: Fetches coding challenge statistics
- **Key Metrics**:
  - Skills match percentage
  - Experience relevance
  - Education level match
  - Coding proficiency score (if applicable)

### Scoring Formula
```
Total Score = (Video_Score × 0.40) + (Audio_Score × 0.30) + (Text_Score × 0.30)
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI        │    │   AI Processors │
│   Frontend      │◄──►│   Backend        │◄──►│                 │
│                 │    │                  │    │ • Video         │
│ • File Upload   │    │ • /upload        │    │ • Audio         │
│ • Progress      │    │ • /status        │    │ • Text          │
│ • Results       │    │ • /results       │    │ • Scoring       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📊 Scoring System

### Individual Metrics (0-100 scale)
1. **Emotion Score (40% weight)**: Confidence and emotional stability based on facial expressions
2. **Communication Score (30% weight)**: Speaking clarity, sentiment, and hesitation patterns  
3. **Skills Match Score (30% weight)**: Resume-job description alignment and technical competency

### Cumulative Score
Weighted average providing overall candidate assessment with AI-generated verdict and recommendations.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)

### Quick Start with Docker
```bash
# Clone the repository
git clone <repository-url>
cd Digital-Hiring

# Copy environment file
cp .env.example .env

# Build and run with Docker Compose
docker-compose up --build

# Access the application
open http://localhost:8000
```

### Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Ensure model files are in place
# model.h5 and haarcascade_frontalface_default.xml should be in backend/

python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
Digital-Hiring/
├── backend/
│   ├── processors/
│   │   ├── video_processor.py      # Emotion detection
│   │   ├── audio_processor.py      # Communication analysis
│   │   └── text_processor.py       # Skills matching
│   ├── main.py                     # FastAPI application
│   ├── scoring_engine.py           # Score calculation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js       # File upload interface
│   │   │   ├── ProcessingStatus.js # Progress tracking
│   │   │   └── ResultsDisplay.js   # Results visualization
│   │   ├── App.js                  # Main application
│   │   └── index.js
│   └── package.json
├── Code/                           # Original model files
│   ├── model.h5                    # Trained CNN model
│   └── haarcascade_frontalface_default.xml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔧 API Endpoints

### Core Endpoints
- `POST /upload` - Upload files and start processing
- `GET /status/{process_id}` - Check processing status
- `GET /results/{process_id}` - Retrieve evaluation results
- `DELETE /results/{process_id}` - Clean up processing data

### Utility Endpoints
- `GET /health` - Health check with processor status
- `GET /active-processes` - List all active processing sessions

## 📈 Usage Workflow

1. **Upload Files**: Drag and drop interview video, resume, and enter job description
2. **Processing**: Real-time progress tracking through video → audio → text → scoring phases
3. **Results**: Comprehensive dashboard with:
   - Individual scores with explanations
   - Visual charts and progress bars
   - AI-generated verdict with recommendations
   - Detailed analysis breakdowns
   - Strengths and improvement areas

## 🔒 Security Features

- File type validation and size limits
- Input sanitization and validation
- CORS protection for API endpoints
- Secure file handling with temporary storage cleanup
- Environment-based configuration

## 🚀 Deployment

### Production Considerations
- Replace in-memory storage with Redis/Database
- Implement user authentication and authorization
- Add rate limiting and request throttling
- Set up proper logging and monitoring
- Configure SSL/TLS certificates
- Implement backup and recovery procedures

### Environment Variables
See `.env.example` for complete configuration options including:
- Model paths and API keys
- File upload limits and directories
- Database and Redis connections
- Security settings

## 📊 Model Information

### Video Analysis
- **Model**: CNN trained on emotion recognition dataset
- **Classes**: Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise
- **Input**: 48x48 grayscale face images extracted at 3 FPS

### Audio Analysis
- **Transcription**: OpenAI Whisper (configurable)
- **Sentiment**: VADER + TextBlob combination
- **Features**: Silence detection, filler word counting, emotion analysis

### Text Analysis
- **Similarity**: TF-IDF with cosine similarity
- **Skills**: Predefined technical and soft skills matching
- **Integration**: LeetCode API for coding assessment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 🚀 Future Improvements

### 1. Enhanced AI Capabilities
- **Advanced Emotion Recognition**: Implement transformer-based models for more accurate emotion detection
- **Multimodal Analysis**: Combine video, audio, and text analysis for deeper insights
- **Behavioral Analysis**: Detect micro-expressions and subtle behavioral cues
- **Cultural Sensitivity**: Adapt scoring models for different cultural contexts

### 2. Expanded Integration
- **ATS Integration**: Connect with popular Applicant Tracking Systems (Greenhouse, Lever, etc.)
- **Video Interview Platforms**: Native integration with Zoom, MS Teams, and Google Meet
- **Code Assessment**: Direct integration with coding platforms (LeetCode, HackerRank, CodeSignal)
- **Reference Checking**: Automated reference collection and analysis

### 3. Advanced Analytics
- **Team Fit Analysis**: Match candidates with team dynamics and culture
- **Predictive Analytics**: Forecast candidate success based on historical hiring data
- **Bias Detection**: Identify and mitigate potential biases in the evaluation process
- **Custom Scoring Models**: Allow companies to define their own scoring weights and criteria

### 4. User Experience
- **Mobile App**: Native mobile applications for iOS and Android
- **Offline Mode**: Basic functionality without internet connection
- **Custom Reports**: Create and save custom report templates
- **Collaboration Tools**: Team-based candidate evaluation and feedback

### 5. Enterprise Features
- **SSO Integration**: Support for enterprise authentication (SAML, OAuth)
- **Audit Logs**: Comprehensive activity tracking and reporting
- **GDPR Compliance**: Enhanced data protection and privacy controls
- **API Access**: Full API for custom integrations and automation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for audio transcription
- Kaggle emotion recognition dataset
- Material-UI for React components
- FastAPI framework for backend development

---

**Note**: This system is designed for evaluation purposes. Ensure compliance with local employment laws and ethical AI practices when using for actual hiring decisions.
