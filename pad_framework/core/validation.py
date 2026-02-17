"""
Input Validation Framework
Comprehensive validation using Pydantic
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, validator, Field, constr
from enum import Enum
import re


class FlowStatus(str, Enum):
    """Valid flow statuses"""
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    PENDING = "pending"


class LogLevel(str, Enum):
    """Valid log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class FlowExecutionRequest(BaseModel):
    """Validated flow execution request"""
    flow_name: constr(min_length=1, max_length=255)
    input_variables: Dict[str, Any] = Field(default_factory=dict)
    timeout: Optional[int] = Field(None, ge=1, le=7200)  # Max 2 hours
    retry_count: int = Field(0, ge=0, le=10)
    priority: int = Field(5, ge=1, le=10)
    
    @validator('flow_name')
    def validate_flow_name(cls, v):
        """Validate flow name format"""
        # Allow alphanumeric, underscores, hyphens only
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                'Flow name must contain only alphanumeric characters, '
                'underscores, and hyphens'
            )
        return v
    
    @validator('input_variables')
    def validate_input_variables(cls, v):
        """Validate input variables"""
        # Check for maximum nesting depth
        def check_depth(obj, depth=0, max_depth=5):
            if depth > max_depth:
                raise ValueError(f'Input variables nested too deep (max {max_depth})')
            if isinstance(obj, dict):
                for value in obj.values():
                    check_depth(value, depth + 1, max_depth)
            elif isinstance(obj, list):
                for item in obj:
                    check_depth(item, depth + 1, max_depth)
        
        check_depth(v)
        return v
    
    class Config:
        use_enum_values = True


class FlowCreationRequest(BaseModel):
    """Validated flow creation request"""
    flow_name: constr(min_length=1, max_length=255)
    description: str = Field("", max_length=1000)
    template: Optional[str] = Field(None, max_length=100)
    enabled: bool = True
    timeout: int = Field(300, ge=1, le=7200)
    priority: int = Field(5, ge=1, le=10)
    
    @validator('flow_name')
    def validate_flow_name(cls, v):
        """Validate flow name format"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                'Flow name must contain only alphanumeric characters, '
                'underscores, and hyphens'
            )
        # Prevent reserved names
        reserved = ['config', 'test', 'system', 'admin']
        if v.lower() in reserved:
            raise ValueError(f'Flow name cannot be a reserved word: {", ".join(reserved)}')
        return v


class ScheduleRequest(BaseModel):
    """Validated schedule request"""
    flow_name: constr(min_length=1, max_length=255)
    schedule: str = Field(..., min_length=9, max_length=100)
    input_variables: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    timezone: str = Field("UTC", max_length=50)
    
    @validator('schedule')
    def validate_cron_expression(cls, v):
        """Validate cron expression format"""
        # Basic cron validation (5 fields)
        parts = v.split()
        if len(parts) != 5:
            raise ValueError(
                'Schedule must be a valid cron expression with 5 fields '
                '(minute hour day month weekday)'
            )
        
        # Validate each field
        ranges = [
            (0, 59),   # minute
            (0, 23),   # hour
            (1, 31),   # day
            (1, 12),   # month
            (0, 6)     # weekday
        ]
        
        for i, (part, (min_val, max_val)) in enumerate(zip(parts, ranges)):
            if part == '*':
                continue
            if '/' in part:
                continue  # Skip step values for now
            if '-' in part:
                continue  # Skip ranges for now
            if ',' in part:
                continue  # Skip lists for now
            
            try:
                val = int(part)
                if not min_val <= val <= max_val:
                    raise ValueError(
                        f'Cron field {i+1} value {val} out of range '
                        f'[{min_val}-{max_val}]'
                    )
            except ValueError:
                pass  # Allow named values (MON, TUE, etc.)
        
        return v


class ConfigUpdateRequest(BaseModel):
    """Validated configuration update"""
    key: constr(min_length=1, max_length=255)
    value: Any
    
    @validator('key')
    def validate_key(cls, v):
        """Validate configuration key format"""
        # Must be dot-separated alphanumeric
        if not re.match(r'^[a-zA-Z0-9_.]+$', v):
            raise ValueError(
                'Configuration key must contain only alphanumeric '
                'characters, dots, and underscores'
            )
        return v


class PathValidator:
    """Validate and sanitize file paths"""
    
    @staticmethod
    def validate_path(path: str, base_path: str) -> str:
        """
        Validate path to prevent traversal attacks
        
        Args:
            path: Path to validate
            base_path: Base directory path
            
        Returns:
            Sanitized absolute path
            
        Raises:
            ValueError: If path is invalid or outside base
        """
        from pathlib import Path
        
        try:
            # Resolve to absolute path
            abs_path = Path(path).resolve()
            abs_base = Path(base_path).resolve()
            
            # Check if path is within base directory
            if not str(abs_path).startswith(str(abs_base)):
                raise ValueError(
                    f'Path {path} is outside allowed directory {base_path}'
                )
            
            return str(abs_path)
            
        except Exception as e:
            raise ValueError(f'Invalid path: {str(e)}')
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent injection
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
        
        # Ensure not empty
        if not sanitized or sanitized.isspace():
            raise ValueError('Filename cannot be empty')
        
        return sanitized


class CommandValidator:
    """Validate command arguments to prevent injection"""
    
    # Dangerous characters that could enable command injection
    DANGEROUS_CHARS = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']
    
    # Dangerous command sequences
    DANGEROUS_SEQUENCES = ['&&', '||', '$(', '`']
    
    @classmethod
    def validate_args(cls, args: List[str]) -> List[str]:
        """
        Validate command arguments
        
        Args:
            args: List of command arguments
            
        Returns:
            Validated arguments
            
        Raises:
            ValueError: If dangerous patterns detected
        """
        for arg in args:
            # Check for dangerous characters
            for char in cls.DANGEROUS_CHARS:
                if char in arg:
                    raise ValueError(
                        f'Dangerous character detected in argument: {char}'
                    )
            
            # Check for dangerous sequences
            for seq in cls.DANGEROUS_SEQUENCES:
                if seq in arg:
                    raise ValueError(
                        f'Dangerous command sequence detected: {seq}'
                    )
        
        return args
    
    @classmethod
    def sanitize_arg(cls, arg: str) -> str:
        """
        Sanitize a single argument
        
        Args:
            arg: Argument to sanitize
            
        Returns:
            Sanitized argument
        """
        # Remove dangerous characters
        for char in cls.DANGEROUS_CHARS:
            arg = arg.replace(char, '')
        
        return arg


class InputSanitizer:
    """Sanitize various types of inputs"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 10000) -> str:
        """
        Sanitize string input
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Limit length
        if len(value) > max_length:
            value = value[:max_length]
        
        # Remove control characters except newline, tab
        value = ''.join(char for char in value if char.isprintable() or char in '\n\t')
        
        return value
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], max_depth: int = 5) -> Dict[str, Any]:
        """
        Sanitize dictionary recursively
        
        Args:
            data: Dictionary to sanitize
            max_depth: Maximum nesting depth
            
        Returns:
            Sanitized dictionary
        """
        def _sanitize(obj, depth=0):
            if depth > max_depth:
                raise ValueError(f'Dictionary nested too deep (max {max_depth})')
            
            if isinstance(obj, dict):
                return {
                    k: _sanitize(v, depth + 1)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [_sanitize(item, depth + 1) for item in obj]
            elif isinstance(obj, str):
                return InputSanitizer.sanitize_string(obj)
            else:
                return obj
        
        return _sanitize(data)


def validate_flow_execution(
    flow_name: str,
    input_variables: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
    retry_count: int = 0
) -> FlowExecutionRequest:
    """
    Validate flow execution parameters
    
    Args:
        flow_name: Name of flow to execute
        input_variables: Input variables
        timeout: Timeout in seconds
        retry_count: Retry attempts
        
    Returns:
        Validated FlowExecutionRequest
        
    Raises:
        ValidationError: If validation fails
    """
    return FlowExecutionRequest(
        flow_name=flow_name,
        input_variables=input_variables or {},
        timeout=timeout,
        retry_count=retry_count
    )


def validate_flow_creation(
    flow_name: str,
    description: str = "",
    template: Optional[str] = None
) -> FlowCreationRequest:
    """
    Validate flow creation parameters
    
    Args:
        flow_name: Name of new flow
        description: Flow description
        template: Template name
        
    Returns:
        Validated FlowCreationRequest
        
    Raises:
        ValidationError: If validation fails
    """
    return FlowCreationRequest(
        flow_name=flow_name,
        description=description,
        template=template
    )


def validate_schedule(
    flow_name: str,
    schedule: str,
    input_variables: Optional[Dict[str, Any]] = None
) -> ScheduleRequest:
    """
    Validate schedule parameters
    
    Args:
        flow_name: Name of flow to schedule
        schedule: Cron expression
        input_variables: Input variables
        
    Returns:
        Validated ScheduleRequest
        
    Raises:
        ValidationError: If validation fails
    """
    return ScheduleRequest(
        flow_name=flow_name,
        schedule=schedule,
        input_variables=input_variables or {}
    )
