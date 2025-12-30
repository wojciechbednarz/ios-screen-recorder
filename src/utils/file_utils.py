import base64
from pathlib import Path
from src.utils.logger import logger

def ensure_dir(path: Path) -> None:
    """Ensure that a directory exists."""
    if not path.exists():
        logger.info(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)

def save_video(base64_data: str, output_path: Path) -> None:
    """Decodes base64 video data and saves it to the specified path."""
    try:
        ensure_dir(output_path.parent)
        video_data = base64.b64decode(base64_data)
        with open(output_path, "wb") as f:
            f.write(video_data)
        logger.info(f"Video saved successfully to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save video: {e}")
        raise
