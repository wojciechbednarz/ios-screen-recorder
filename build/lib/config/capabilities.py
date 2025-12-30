import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_ios_capabilities() -> Dict[str, Any]:
    """Returns Appium capabilities for iOS real device."""
    
    server_url = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
    
    caps = {
        "platformName": "iOS",
        "appium:automationName": "XCUITest",
        "appium:deviceName": os.getenv("DEVICE_NAME", "iPhone"),
        "appium:platformVersion": os.getenv("PLATFORM_VERSION", "17.0"),
        "appium:udid": os.getenv("UDID", "auto"),
        "appium:bundleId": os.getenv("BUNDLE_ID", "com.apple.Settings"),
        "appium:xcodeOrgId": os.getenv("XCODE_ORG_ID"),
        "appium:xcodeSigningId": os.getenv("XCODE_SIGNING_ID", "iPhone Developer"),
        "appium:updatedWDABundleId": os.getenv("UPDATED_WDA_BUNDLE_ID"),
        "appium:noReset": True,
        "appium:newCommandTimeout": 3600,
    }

    # Filter out None values
    return {k: v for k, v in caps.items() if v is not None}
