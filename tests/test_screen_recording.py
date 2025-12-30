import pytest
from pathlib import Path
from src.core.driver import MobileDriver
from src.core.recorder import ScreenRecorder
from src.utils.time_utils import get_file_safe_timestamp

@pytest.fixture(scope="module")
def driver():
    """Validates driver initialization."""
    driver = MobileDriver.get_driver()
    yield driver
    MobileDriver.quit_driver()

def test_screen_recording(driver):
    """Verifies screen recording start, stop and save."""
    recorder = ScreenRecorder(driver)
    
    # Generate output path
    timestamp = get_file_safe_timestamp()
    output_dir = Path("output/recordings")
    output_path = output_dir / f"test_recording_{timestamp}.mp4"
    
    # Start Recording
    recorder.start_recording()
    
    # Wait for a few seconds to record something
    # Doing a simple action or just waiting
    import time
    time.sleep(5)
    
    # Stop Recording
    saved_path = recorder.stop_recording(output_path)
    
    # Assertions
    assert saved_path.exists(), "Video file was not created"
    assert saved_path.stat().st_size > 0, "Video file is empty"
