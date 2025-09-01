"""
FastAPI Backend for Digital Hiring Application
Provides endpoints for file upload, processing, and results retrieval
"""

import os
import tempfile
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging
import asyncio
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from processors.video_processor import VideoProcessor
from processors.audio_processor import AudioProcessor
from processors.text_processor import TextProcessor
from scoring_engine import ScoringEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Digital Hiring API",
    description="AI-powered candidate evaluation system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors independently so failures don't take down the whole app
video_processor = None
audio_processor = None
text_processor = None
scoring_engine = None

# Resolve model paths via environment variables or default to this repo's Code/ directory
root_dir = Path(__file__).resolve().parents[1]
model_path = os.getenv("MODEL_PATH") or os.path.join(root_dir, "Code", "model.h5")
cascade_path = os.getenv("CASCADE_PATH") or os.path.join(root_dir, "Code", "haarcascade_frontalface_default.xml")

try:
    video_processor = VideoProcessor(model_path=model_path, cascade_path=cascade_path)
    logger.info("Video processor initialized")
except Exception as e:
    logger.warning(f"Video processor unavailable: {e}")

try:
    audio_processor = AudioProcessor()
    logger.info("Audio processor initialized")
except Exception as e:
    logger.warning(f"Audio processor unavailable: {e}")

try:
    text_processor = TextProcessor()
    logger.info("Text processor initialized")
except Exception as e:
    logger.warning(f"Text processor unavailable: {e}")

try:
    scoring_engine = ScoringEngine()
    logger.info("Scoring engine initialized")
except Exception as e:
    logger.warning(f"Scoring engine unavailable: {e}")

# In-memory storage for processing results (use Redis/DB in production)
processing_results = {}
processing_status = {}

class ProcessingStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Digital Hiring API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    processors_status = {
        "video_processor": video_processor is not None,
        "audio_processor": audio_processor is not None,
        "text_processor": text_processor is not None,
        "scoring_engine": scoring_engine is not None
    }
    
    return {
        "status": "healthy" if all(processors_status.values()) else "degraded",
        "processors": processors_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/upload")
async def upload_files(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    leetcode_username: Optional[str] = Form(None)
):
    """Upload files and start processing"""
    
    # Validate file types
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid video format. Supported: mp4, avi, mov, mkv")
    
    if not resume.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid resume format. Supported: pdf, docx, txt")
    
    # Validate file sizes (50MB for video, 10MB for resume)
    if video.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Video file too large. Maximum size: 50MB")
    
    if resume.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Resume file too large. Maximum size: 10MB")
    
    # Generate unique processing ID
    process_id = str(uuid.uuid4())
    
    try:
        # Create temporary directory for this processing session
        temp_dir = tempfile.mkdtemp(prefix=f"hiring_{process_id}_")
        
        # Save uploaded files
        video_path = os.path.join(temp_dir, f"video_{video.filename}")
        resume_path = os.path.join(temp_dir, f"resume_{resume.filename}")
        
        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)
        
        with open(resume_path, "wb") as f:
            content = await resume.read()
            f.write(content)
        
        # Initialize processing status
        processing_status[process_id] = {
            "status": ProcessingStatus.PENDING,
            "progress": 0,
            "message": "Files uploaded successfully",
            "started_at": datetime.now().isoformat()
        }
        
        # Start background processing
        background_tasks.add_task(
            process_candidate,
            process_id,
            video_path,
            resume_path,
            job_description,
            leetcode_username or "",
            temp_dir
        )
        
        return {
            "process_id": process_id,
            "message": "Files uploaded successfully. Processing started.",
            "status": ProcessingStatus.PENDING
        }
        
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

async def process_candidate(
    process_id: str,
    video_path: str,
    resume_path: str,
    job_description: str,
    leetcode_username: str,
    temp_dir: str
):
    """Background task to process candidate data"""
    
    try:
        # Update status
        processing_status[process_id].update({
            "status": ProcessingStatus.PROCESSING,
            "progress": 10,
            "message": "Starting video analysis..."
        })
        
        # Process video
        logger.info(f"Processing video for {process_id}")
        video_results = video_processor.process_video(video_path)
        
        processing_status[process_id].update({
            "progress": 40,
            "message": "Video analysis complete. Starting audio analysis..."
        })
        
        # Process audio
        logger.info(f"Processing audio for {process_id}")
        audio_results = audio_processor.process_audio(video_path)
        
        processing_status[process_id].update({
            "progress": 70,
            "message": "Audio analysis complete. Starting text analysis..."
        })
        
        # Process text
        logger.info(f"Processing text for {process_id}")
        transcript = audio_results.get('transcript', '')
        text_results = text_processor.process_text_analysis(
            resume_path, job_description, transcript, leetcode_username
        )
        
        processing_status[process_id].update({
            "progress": 90,
            "message": "Text analysis complete. Calculating scores..."
        })
        
        # Calculate scores
        logger.info(f"Calculating scores for {process_id}")
        scores = scoring_engine.calculate_scores(video_results, audio_results, text_results)
        
        # Generate verdict
        verdict = scoring_engine.generate_verdict(scores, video_results, audio_results, text_results)
        
        # Get detailed breakdown
        breakdown = scoring_engine.get_detailed_breakdown(video_results, audio_results, text_results)
        
        # Store results
        processing_results[process_id] = {
            "scores": scores,
            "verdict": verdict,
            "breakdown": breakdown,
            "raw_results": {
                "video": video_results,
                "audio": audio_results,
                "text": text_results
            },
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "video_filename": os.path.basename(video_path),
                "resume_filename": os.path.basename(resume_path),
                "job_description_length": len(job_description),
                "leetcode_username": leetcode_username
            }
        }
        
        # Update final status
        processing_status[process_id].update({
            "status": ProcessingStatus.COMPLETED,
            "progress": 100,
            "message": "Processing completed successfully",
            "completed_at": datetime.now().isoformat()
        })
        
        logger.info(f"Processing completed for {process_id}")
        
    except Exception as e:
        logger.error(f"Error processing candidate {process_id}: {str(e)}")
        processing_status[process_id].update({
            "status": ProcessingStatus.ERROR,
            "message": f"Processing failed: {str(e)}",
            "error_at": datetime.now().isoformat()
        })
    
    finally:
        # Clean up temporary files
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory {temp_dir}: {str(e)}")

@app.get("/status/{process_id}")
async def get_processing_status(process_id: str):
    """Get processing status for a specific process ID"""
    
    if process_id not in processing_status:
        raise HTTPException(status_code=404, detail="Process ID not found")
    
    return processing_status[process_id]

@app.get("/results/{process_id}")
async def get_results(process_id: str):
    """Get processing results for a specific process ID"""
    
    if process_id not in processing_status:
        raise HTTPException(status_code=404, detail="Process ID not found")
    
    status = processing_status[process_id]
    
    if status["status"] == ProcessingStatus.PROCESSING:
        raise HTTPException(status_code=202, detail="Processing still in progress")
    
    if status["status"] == ProcessingStatus.ERROR:
        raise HTTPException(status_code=500, detail=status.get("message", "Processing failed"))
    
    if process_id not in processing_results:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return processing_results[process_id]

@app.delete("/results/{process_id}")
async def delete_results(process_id: str):
    """Delete processing results and status for a specific process ID"""
    
    deleted_items = []
    
    if process_id in processing_status:
        del processing_status[process_id]
        deleted_items.append("status")
    
    if process_id in processing_results:
        del processing_results[process_id]
        deleted_items.append("results")
    
    if not deleted_items:
        raise HTTPException(status_code=404, detail="Process ID not found")
    
    return {
        "message": f"Deleted {', '.join(deleted_items)} for process {process_id}",
        "deleted_items": deleted_items
    }

@app.get("/active-processes")
async def get_active_processes():
    """Get list of all active processes"""
    
    active = []
    for process_id, status in processing_status.items():
        active.append({
            "process_id": process_id,
            "status": status["status"],
            "progress": status.get("progress", 0),
            "started_at": status.get("started_at"),
            "message": status.get("message", "")
        })
    
    return {"active_processes": active, "count": len(active)}

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("backend/processors", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
