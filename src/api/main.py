from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.routes import router
from src.utils.logger import logger
from src.database import init_db, check_db_connection
import os
from pathlib import Path

app = FastAPI(
    title="Appium iOS Screen Recorder API",
    description="API for controlling iOS screen recording via Appium",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serve recordings as static files (already handled by route, but this is another way if needed)
# app.mount("/static/recordings", StaticFiles(directory="output/recordings"), name="recordings")

# Mount frontend static files
# We check if the dist directory exists before mounting
frontend_path = Path("frontend/dist")
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
    
    # Catch-all route to serve index.html for React Router
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        index_file = frontend_path / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"error": "Frontend not found"}
else:
    logger.warning("Frontend dist directory not found. API running in standalone mode.")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up API Server...")
    
    # Initialize database
    try:
        if check_db_connection():
            init_db()
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database connection failed - running without database")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        logger.warning("Continuing without database...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API Server...")
    from src.core.driver import MobileDriver
    MobileDriver.quit_driver()
