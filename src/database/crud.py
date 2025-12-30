import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.database.models import Recording, RecordingStatus
from src.utils.logger import logger

def create_recording(
    db: Session,
    filename: str,
    device_name: Optional[str] = None
) -> Recording:
    """
    Create a new recording entry in the database.
    
    Args:
        db: Database session
        filename: Name of the recording file
        device_name: Optional device name
        
    Returns:
        Created Recording object
    """
    recording = Recording(
        filename=filename,
        device_name=device_name,
        status=RecordingStatus.IN_PROGRESS
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)
    logger.info(f"Created recording: {filename}")
    return recording

def get_recordings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[RecordingStatus] = None
) -> List[Recording]:
    """
    Get list of recordings with optional filtering and pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        status: Optional status filter
        
    Returns:
        List of Recording objects
    """
    query = db.query(Recording)
    
    if status:
        query = query.filter(Recording.status == status)
    
    recordings = query.order_by(desc(Recording.created_at)).offset(skip).limit(limit).all()
    return recordings

def get_recording_by_id(db: Session, recording_id: str) -> Optional[Recording]:
    """
    Get a recording by its ID.
    
    Args:
        db: Database session
        recording_id: UUID of the recording
        
    Returns:
        Recording object or None if not found
    """
    try:
        if isinstance(recording_id, str):
            recording_id = uuid.UUID(recording_id)
    except ValueError:
        logger.warning(f"Invalid UUID format: {recording_id}")
        return None
        
    return db.query(Recording).filter(Recording.id == recording_id).first()

def get_recording_by_filename(db: Session, filename: str) -> Optional[Recording]:
    """
    Get a recording by its filename.
    
    Args:
        db: Database session
        filename: Name of the recording file
        
    Returns:
        Recording object or None if not found
    """
    return db.query(Recording).filter(Recording.filename == filename).first()

def update_recording(
    db: Session,
    recording_id: str,
    size_bytes: Optional[int] = None,
    duration_seconds: Optional[int] = None,
    status: Optional[RecordingStatus] = None
) -> Optional[Recording]:
    """
    Update a recording's metadata.
    
    Args:
        db: Database session
        recording_id: UUID of the recording
        size_bytes: Optional file size in bytes
        duration_seconds: Optional duration in seconds
        status: Optional status update
        
    Returns:
        Updated Recording object or None if not found
    """
    recording = get_recording_by_id(db, recording_id)
    if not recording:
        return None
    
    if size_bytes is not None:
        recording.size_bytes = size_bytes
    if duration_seconds is not None:
        recording.duration_seconds = duration_seconds
    if status is not None:
        recording.status = status
    
    db.commit()
    db.refresh(recording)
    logger.info(f"Updated recording: {recording.filename}")
    return recording

def update_recording_by_filename(
    db: Session,
    filename: str,
    size_bytes: Optional[int] = None,
    duration_seconds: Optional[int] = None,
    status: Optional[RecordingStatus] = None
) -> Optional[Recording]:
    """
    Update a recording's metadata by filename.
    
    Args:
        db: Database session
        filename: Name of the recording file
        size_bytes: Optional file size in bytes
        duration_seconds: Optional duration in seconds
        status: Optional status update
        
    Returns:
        Updated Recording object or None if not found
    """
    recording = get_recording_by_filename(db, filename)
    if not recording:
        return None
    
    if size_bytes is not None:
        recording.size_bytes = size_bytes
    if duration_seconds is not None:
        recording.duration_seconds = duration_seconds
    if status is not None:
        recording.status = status
    
    db.commit()
    db.refresh(recording)
    logger.info(f"Updated recording: {recording.filename}")
    return recording

def delete_recording(db: Session, recording_id: str) -> bool:
    """
    Delete a recording from the database.
    
    Args:
        db: Database session
        recording_id: UUID of the recording
        
    Returns:
        True if deleted, False if not found
    """
    recording = get_recording_by_id(db, recording_id)
    if not recording:
        return False
    
    db.delete(recording)
    db.commit()
    logger.info(f"Deleted recording: {recording.filename}")
    return True

def get_total_recordings_count(db: Session) -> int:
    """
    Get total count of recordings.
    
    Args:
        db: Database session
        
    Returns:
        Total number of recordings
    """
    return db.query(Recording).count()

def get_total_size(db: Session) -> int:
    """
    Get total size of all recordings in bytes.
    
    Args:
        db: Database session
        
    Returns:
        Total size in bytes
    """
    from sqlalchemy import func
    result = db.query(func.sum(Recording.size_bytes)).scalar()
    return result or 0
