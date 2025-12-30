import os
from typing import Optional
from appium import webdriver
from appium.options.common import AppiumOptions
from src.config.capabilities import get_ios_capabilities
from src.utils.logger import logger

class MobileDriver:
    _instance: Optional[webdriver.Remote] = None

    @classmethod
    def get_driver(cls) -> object:
        """Returns the singleton driver instance, creating it if needed."""
        if cls._instance is None:
            try:
                # Check for Mock Mode
                if os.getenv("MOCK_MODE", "false").lower() == "true":
                    from src.simulation.mock_driver import MockDriver
                    logger.info("MOCK_MODE is enabled. Initializing MockDriver.")
                    cls._instance = MockDriver()
                    return cls._instance

                logger.info("Initializing Appium Driver...")
                caps = get_ios_capabilities()
                server_url = os.getenv("APPIUM_SERVER_URL", "http://localhost:4723")
                
                # Appium 2.x standard way
                options = AppiumOptions()
                options.load_capabilities(caps)
                
                cls._instance = webdriver.Remote(server_url, options=options)
                logger.info("Driver initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize driver: {e}")
                if "WinError 10061" in str(e) or "Connection refused" in str(e):
                    logger.warning("\n\n(Hint) Connection refused. If you are running locally on Windows without a real device, try running in Mock Mode:\n    $env:MOCK_MODE='true'; pytest\n")
                raise

        return cls._instance

    @classmethod
    def quit_driver(cls) -> None:
        """Quits the driver instance."""
        if cls._instance:
            try:
                logger.info("Quitting Appium Driver...")
                cls._instance.quit()
                cls._instance = None
                logger.info("Driver quit successfully.")
            except Exception as e:
                logger.error(f"Error while quitting driver: {e}")
                cls._instance = None
