from src.core.driver import MobileDriver
from src.core.recorder import ScreenRecorder
from fastapi import HTTPException

def get_driver():
    try:
        if not MobileDriver._instance:
            # Auto-initialize if not ready (useful for first request)
            # In a real app we might want explicit initialization
            return MobileDriver.get_driver()
        return MobileDriver.get_driver()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize driver: {str(e)}")

def get_recorder():
    driver = get_driver()
    return ScreenRecorder(driver)
