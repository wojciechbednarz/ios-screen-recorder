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
        # Return a dummy base64 string (valid base64 but garbage content)
        # This is enough to pass the file_utils.save_video decoding step
        dummy_content = b"Mock Video Content"
        return base64.b64encode(dummy_content).decode('utf-8')

    def quit(self):
        """Simulates quitting the driver."""
        logger.info("MockDriver: quit called.")
