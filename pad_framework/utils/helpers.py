"""
Helper Utilities
Common utility functions used across the framework
"""

import os
import json
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
from datetime import datetime
import hashlib


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str, indent: int = 2) -> None:
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to save file
        indent: JSON indentation
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load YAML file
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to YAML file
    
    Args:
        data: Data to save
        file_path: Path to save file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False)


def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID
    
    Args:
        prefix: Optional prefix for ID
        
    Returns:
        Unique ID string
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp


def hash_string(text: str) -> str:
    """
    Generate hash of string
    
    Args:
        text: Text to hash
        
    Returns:
        SHA256 hash
    """
    return hashlib.sha256(text.encode()).hexdigest()


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.2f}h"


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes in human-readable format
    
    Args:
        bytes_value: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f}PB"


def safe_get(dictionary: Dict, key_path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value
    
    Args:
        dictionary: Dictionary to search
        key_path: Dot-separated key path (e.g., "level1.level2.key")
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    keys = key_path.split('.')
    value = dictionary
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def timestamp() -> str:
    """
    Get current timestamp
    
    Returns:
        ISO format timestamp
    """
    return datetime.now().isoformat()


def parse_cron(cron_expression: str) -> Dict[str, Any]:
    """
    Parse cron expression
    
    Args:
        cron_expression: Cron expression (e.g., "0 9 * * *")
        
    Returns:
        Parsed cron components
    """
    parts = cron_expression.split()
    
    if len(parts) != 5:
        raise ValueError("Invalid cron expression")
    
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day": parts[2],
        "month": parts[3],
        "weekday": parts[4]
    }


def validate_email(email: str) -> bool:
    """
    Validate email address
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe use
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    return sanitized
