import os
from dotenv import load_dotenv

load_dotenv()

# WinAppDriver settings
WINAPPDRIVER_URL = os.getenv("WINAPPDRIVER_URL", "http://127.0.0.1:4723")

# Default implicit wait (seconds)
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))

# Screenshot directory
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")

# Logs directory
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

# Application paths — override via .env or environment variables
APP_PATHS = {
    "calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    "notepad": "C:\\Windows\\System32\\notepad.exe",
    # Add more applications here
}


def get_app_path(app_name: str) -> str:
    """Return the application path/identifier for a given app name."""
    path = APP_PATHS.get(app_name.lower())
    if not path:
        raise ValueError(f"Unknown application: '{app_name}'. Add it to APP_PATHS in config/settings.py")
    return path
