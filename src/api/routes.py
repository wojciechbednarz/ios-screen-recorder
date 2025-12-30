import os
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import List
from pathlib import Path
from sqlalchemy.orm import Session

from src.api.models import RecordingStatus, RecordingResponse, StartRecordingRequest
from src.api.dependencies import get_recorder
from src.core.recorder import ScreenRecorder
from src.utils.time_utils import get_file_safe_timestamp
from src.database import get_db, Recording as DBRecording, RecordingStatus as DBRecordingStatus
from src.database import crud

router = APIRouter()

# Global state to track active recording (in-memory for simplicity)
# In production with multiple workers, use Redis or database
ACTIVE_RECORDING = {
    "is_recording": False,
    "filename": None,
    "start_time": None,
    "db_id": None
}

OUTPUT_DIR = Path("output/recordings")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/recording/start", response_model=RecordingStatus)
async def start_recording(
    req: StartRecordingRequest,
    recorder: ScreenRecorder = Depends(get_recorder),
    db: Session = Depends(get_db)
):
    """Start a new screen recording"""
    if ACTIVE_RECORDING["is_recording"]:
        raise HTTPException(status_code=400, detail="Recording already in progress")
    
    try:
        # Generate filename
        filename = f"{req.filename_prefix}_{get_file_safe_timestamp()}.mp4"
        
        # Create database entry
        db_recording = crud.create_recording(
            db=db,
            filename=filename,
            device_name=None  # Can be populated from device info if available
        )
        
        # Start actual recording
        recorder.start_recording()
        
        # Update global state
        ACTIVE_RECORDING["is_recording"] = True
        ACTIVE_RECORDING["filename"] = filename
        ACTIVE_RECORDING["start_time"] = time.time()
        ACTIVE_RECORDING["db_id"] = str(db_recording.id)
        
        return RecordingStatus(
            is_recording=True,
            filename=filename
        )
    except Exception as e:
        ACTIVE_RECORDING["is_recording"] = False
        # Update DB status to failed if entry was created
        if ACTIVE_RECORDING.get("db_id"):
            crud.update_recording(
                db=db,
                recording_id=ACTIVE_RECORDING["db_id"],
                status=DBRecordingStatus.FAILED
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recording/stop", response_model=RecordingResponse)
async def stop_recording(
    recorder: ScreenRecorder = Depends(get_recorder),
    db: Session = Depends(get_db)
):
    """Stop the current recording"""
    if not ACTIVE_RECORDING["is_recording"]:
        raise HTTPException(status_code=400, detail="No recording in progress")
    
    try:
        filename = ACTIVE_RECORDING["filename"]
        output_path = OUTPUT_DIR / filename
        start_time = ACTIVE_RECORDING["start_time"]
        db_id = ACTIVE_RECORDING["db_id"]
        
        # Stop recording and save file
        saved_path = recorder.stop_recording(output_path)
        
        # Calculate duration
        duration_seconds = int(time.time() - start_time) if start_time else None
        
        # Update database with file info
        db_recording = crud.update_recording(
            db=db,
            recording_id=db_id,
            size_bytes=saved_path.stat().st_size if saved_path else 0,
            duration_seconds=duration_seconds,
            status=DBRecordingStatus.COMPLETED
        )
        
        # Reset global state
        ACTIVE_RECORDING["is_recording"] = False
        ACTIVE_RECORDING["filename"] = None
        ACTIVE_RECORDING["start_time"] = None
        ACTIVE_RECORDING["db_id"] = None
        
        if db_recording:
            return RecordingResponse(
                filename=db_recording.filename,
                size_bytes=db_recording.size_bytes,
                created_at=str(db_recording.created_at.timestamp()),
                download_url=f"/recordings/{db_recording.filename}"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to update recording in database")
            
    except Exception as e:
        # Attempt cleanup
        ACTIVE_RECORDING["is_recording"] = False
        if ACTIVE_RECORDING.get("db_id"):
            crud.update_recording(
                db=db,
                recording_id=ACTIVE_RECORDING["db_id"],
                status=DBRecordingStatus.FAILED
            )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recordings", response_model=List[RecordingResponse])
async def list_recordings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all recordings from database"""
    try:
        db_recordings = crud.get_recordings(db=db, skip=skip, limit=limit)
        
        recordings = []
        for db_rec in db_recordings:
            recordings.append(RecordingResponse(
                filename=db_rec.filename,
                size_bytes=db_rec.size_bytes,
                created_at=str(db_rec.created_at.timestamp()),
                download_url=f"/recordings/{db_rec.filename}"
            ))
        
        return recordings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recordings: {str(e)}")

@router.get("/recordings/{filename}")
async def download_recording(filename: str, db: Session = Depends(get_db)):
    """Download a specific recording file"""
    # Verify file exists in database
    db_recording = crud.get_recording_by_filename(db=db, filename=filename)
    if not db_recording:
        raise HTTPException(status_code=404, detail="Recording not found in database")
    
    # Check if file exists on disk
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Recording file not found on disk")
    
    return FileResponse(file_path, media_type="video/mp4", filename=filename)

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        total_recordings = crud.get_total_recordings_count(db=db)
        return {
            "status": "ok",
            "environment": os.getenv("PLATFORM_TYPE", "unknown"),
            "database": "connected",
            "total_recordings": total_recordings
        }
    except Exception as e:
        return {
            "status": "degraded",
            "environment": os.getenv("PLATFORM_TYPE", "unknown"),
            "database": "disconnected",
            "error": str(e)
        }
