from pydantic import BaseModel
from typing import Optional, List

class RecordingStatus(BaseModel):
    is_recording: bool
    filename: Optional[str] = None
    duration: Optional[float] = None

class RecordingResponse(BaseModel):
    filename: str
    size_bytes: int
    created_at: str
    download_url: str

class StartRecordingRequest(BaseModel):
    filename_prefix: Optional[str] = "recording"

class ErrorResponse(BaseModel):
    detail: str
