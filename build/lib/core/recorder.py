from pathlib import Path
from typing import Optional
from appium.webdriver.webdriver import WebDriver
from src.core.driver import MobileDriver
from src.utils.file_utils import save_video
from src.utils.logger import logger

class ScreenRecorder:
    def __init__(self, driver: WebDriver = None):
        self.driver = driver or MobileDriver.get_driver()

    def start_recording(self, video_type: str = "mp4", time_limit: int = 180, video_quality: str = "medium") -> None:
        """
        Starts screen recording on the iOS device.
        
        Args:
            video_type: Video format (default: mp4/h264)
            time_limit: Max recording time in seconds (max 1800s for iOS)
            video_quality: low, medium, or high
        """
        try:
            logger.info("Starting screen recording...")
            self.driver.start_recording_screen(
                videoType=video_type,
                timeLimit=time_limit,
                videoQuality=video_quality,
                forceRestart=True
            )
            logger.info("Screen recording started.")
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            raise

    def stop_recording(self, output_path: Path) -> Path:
        """
        Stops screen recording and saves the file.
        
        Args:
            output_path: The file path where the video should be saved.
            
        Returns:
            The absolute path to the saved video file.
        """
        try:
            logger.info("Stopping screen recording...")
            video_base64 = self.driver.stop_recording_screen()
            
            if not video_base64:
                logger.warning("No video data returned from stop_recording_screen")
                return None

            save_video(video_base64, output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            raise
