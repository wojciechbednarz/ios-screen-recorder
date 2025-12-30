import base64
import time
from src.utils.logger import logger

class MockDriver:
    """Simulates the Appium driver behavior for testing purposes."""
    
    def __init__(self, *args, **kwargs):
        self.session_id = "mock_session_123"
        logger.info("MockDriver initialized.")

    def start_recording_screen(self, **kwargs):
        """Simulates starting the recording."""
        logger.info(f"MockDriver: start_recording_screen called with args: {kwargs}")
        # Simulate some latency
        time.sleep(0.1)
        return True

    def stop_recording_screen(self, **kwargs):
        """Simulates stopping the recording and returning video data."""
        logger.info("MockDriver: stop_recording_screen called.")
        # Return a larger dummy base64 string (approx 1.5 MB)
        # 1.5 * 1024 * 1024 = 1,572,864 bytes
        dummy_content = b"0" * 1572864
        return base64.b64encode(dummy_content).decode('utf-8')

    def quit(self):
        """Simulates quitting the driver."""
        logger.info("MockDriver: quit called.")
