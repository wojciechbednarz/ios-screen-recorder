from datetime import datetime

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return datetime.now().isoformat()

def get_file_safe_timestamp() -> str:
    """Returns a file-name safe timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
