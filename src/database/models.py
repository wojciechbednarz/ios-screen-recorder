import uuid
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RecordingStatus(str, enum.Enum):
    """Recording status enumeration"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Recording(Base):
    """Recording model for storing screen recording metadata"""
    __tablename__ = "recordings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), unique=True, nullable=False, index=True)
    size_bytes = Column(BigInteger, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    device_name = Column(String(100), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    status = Column(SQLEnum(RecordingStatus), nullable=False, default=RecordingStatus.IN_PROGRESS)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "filename": self.filename,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.timestamp() if self.created_at else None,
            "device_name": self.device_name,
            "duration_seconds": self.duration_seconds,
            "status": self.status.value,
            "download_url": f"/recordings/{self.filename}"
        }
