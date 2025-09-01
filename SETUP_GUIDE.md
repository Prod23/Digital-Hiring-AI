# Setup Guide - Digital Hiring Application

This guide will help you set up and run the Digital Hiring application locally or in production.

## 🚀 Quick Start (Recommended)

### Using Docker Compose
The fastest way to get the application running:

```bash
# 1. Clone and navigate to the project
cd /Users/rishirajdatta7/CascadeProjects/Digital-Hiring

# 2. Copy environment configuration
cp .env.example .env

# 3. Build and run the application
docker-compose up --build

# 4. Access the application
open http://localhost:8000
```

## 🛠️ Manual Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Git

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Copy model files**
Ensure these files are in the backend directory:
- `model.h5` (from Code/ directory)
- `haarcascade_frontalface_default.xml` (from Code/ directory)

```bash
cp ../Code/model.h5 ./
cp ../Code/haarcascade_frontalface_default.xml ./
```

5. **Run the backend server**
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Model paths (adjust if needed)
MODEL_PATH=/path/to/model.h5
CASCADE_PATH=/path/to/haarcascade_frontalface_default.xml

# File upload limits
MAX_VIDEO_SIZE=52428800  # 50MB
MAX_RESUME_SIZE=10485760  # 10MB

# API configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📝 Usage Instructions

### 1. Upload Files
- **Video**: Drag and drop interview video (MP4, AVI, MOV, MKV - max 50MB)
- **Resume**: Upload candidate resume (PDF, DOCX, TXT - max 10MB)
- **Job Description**: Paste the job requirements and description
- **LeetCode Username**: (Optional) For coding assessment

### 2. Processing
The system will process files in this order:
1. **Video Analysis** (0-40%): Emotion detection from facial expressions
2. **Audio Analysis** (40-70%): Communication assessment from speech
3. **Text Analysis** (70-90%): Skills matching between resume and job description
4. **Score Calculation** (90-100%): Final scoring and verdict generation

### 3. Results
View comprehensive results including:
- Individual scores with explanations
- Overall cumulative score
- AI-generated verdict and recommendations
- Detailed breakdowns and charts
- Strengths and improvement areas

## 🔍 Troubleshooting

### Common Issues

**1. Model file not found**
```
Error: Emotion detection model not found
```
**Solution**: Copy `model.h5` from `Code/` directory to `backend/`

**2. OpenCV issues**
```
ImportError: libGL.so.1: cannot open shared object file
```
**Solution**: Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# macOS
brew install opencv
```

**3. Frontend connection issues**
```
Network Error: Failed to fetch
```
**Solution**: Ensure backend is running on port 8000 and CORS is configured

**4. Large file upload failures**
```
413 Request Entity Too Large
```
**Solution**: Check file size limits in configuration

### Performance Optimization

**For better performance:**
1. Use SSD storage for temporary files
2. Ensure adequate RAM (minimum 8GB recommended)
3. Use GPU acceleration if available for video processing
4. Consider using Redis for production deployments

## 🚀 Production Deployment

### Docker Production Setup
```bash
# Build production image
docker build -t digital-hiring:prod .

# Run with production settings
docker run -d \
  --name digital-hiring \
  -p 8000:8000 \
  -v $(pwd)/uploads:/tmp/uploads \
  -e DEBUG=False \
  digital-hiring:prod
```

### Production Checklist
- [ ] Set `DEBUG=False` in environment
- [ ] Configure proper SECRET_KEY
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring and logging
- [ ] Configure backup procedures
- [ ] Implement rate limiting
- [ ] Set up database for persistent storage

## 📊 API Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload Test
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "video=@test_video.mp4" \
  -F "resume=@test_resume.pdf" \
  -F "job_description=Software Engineer position requiring Python skills"
```

### Status Check
```bash
curl http://localhost:8000/status/{process_id}
```

## 🔒 Security Considerations

### For Production Use:
1. **File Validation**: Only allow specific file types and sizes
2. **Input Sanitization**: Validate all user inputs
3. **Rate Limiting**: Prevent abuse with request throttling
4. **Authentication**: Implement user authentication if needed
5. **HTTPS**: Always use SSL/TLS in production
6. **File Storage**: Use secure, temporary file storage
7. **API Keys**: Protect external API keys with environment variables

## 📞 Support

### Getting Help
1. Check this setup guide first
2. Review the main README.md for detailed information
3. Check the troubleshooting section above
4. Ensure all dependencies are properly installed
5. Verify model files are in the correct locations

### System Requirements
- **Minimum**: 4GB RAM, 2 CPU cores, 10GB storage
- **Recommended**: 8GB RAM, 4 CPU cores, 20GB storage
- **OS**: Linux, macOS, or Windows with Docker support
