import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
from src.utils.logger import logger

# Database configuration
# Priority:
# 1. DATABASE_URL environment variable (handles Postgres or SQLite)
# 2. AWS RDS individual environment variables
# 3. Local Postgres default
def get_database_url():
    # Try the explicit URL first
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    
    # Try AWS RDS specific variables
    user = os.getenv("RDS_USERNAME")
    password = os.getenv("RDS_PASSWORD")
    host = os.getenv("RDS_HOSTNAME")
    port = os.getenv("RDS_PORT", "5432")
    db_name = os.getenv("RDS_DB_NAME")
    
    if all([user, password, host, db_name]):
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    # Fallback to local postgres for development
    return "postgresql://localhost/appium_recorder"

DATABASE_URL = get_database_url()

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use with FastAPI Depends or as context manager.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager for database session.
    
    Usage:
        with get_db_context() as db:
            # Use db session
            pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from src.database.models import Base
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

def check_db_connection() -> bool:
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
