"""
Error Codes and Enhanced Exception System
Structured error handling with codes and context
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
import traceback


class ErrorCode(str, Enum):
    """Standardized error codes"""
    
    # General errors (E0xx)
    UNKNOWN_ERROR = "E000"
    INTERNAL_ERROR = "E001"
    NOT_IMPLEMENTED = "E002"
    
    # Configuration errors (E1xx)
    CONFIGURATION_ERROR = "E100"
    INVALID_CONFIGURATION = "E101"
    MISSING_CONFIGURATION = "E102"
    CONFIGURATION_LOAD_FAILED = "E103"
    
    # Validation errors (E2xx)
    VALIDATION_ERROR = "E200"
    INVALID_INPUT = "E201"
    INVALID_FLOW_NAME = "E202"
    INVALID_SCHEDULE = "E203"
    INVALID_PATH = "E204"
    
    # Flow errors (E3xx)
    FLOW_NOT_FOUND = "E300"
    FLOW_ALREADY_EXISTS = "E301"
    FLOW_VALIDATION_FAILED = "E302"
    FLOW_CREATION_FAILED = "E303"
    FLOW_DELETION_FAILED = "E304"
    FLOW_IMPORT_FAILED = "E305"
    FLOW_EXPORT_FAILED = "E306"
    
    # Execution errors (E4xx)
    EXECUTION_FAILED = "E400"
    EXECUTION_TIMEOUT = "E401"
    EXECUTION_CANCELLED = "E402"
    PROCESS_START_FAILED = "E403"
    PROCESS_TERMINATED = "E404"
    RETRY_EXHAUSTED = "E405"
    
    # Permission errors (E5xx)
    PERMISSION_DENIED = "E500"
    AUTHENTICATION_FAILED = "E501"
    AUTHORIZATION_FAILED = "E502"
    ACCESS_DENIED = "E503"
    
    # Resource errors (E6xx)
    RESOURCE_NOT_FOUND = "E600"
    RESOURCE_BUSY = "E601"
    RESOURCE_EXHAUSTED = "E602"
    DISK_FULL = "E603"
    MEMORY_EXCEEDED = "E604"
    
    # Integration errors (E7xx)
    INTEGRATION_ERROR = "E700"
    DATABASE_ERROR = "E701"
    API_ERROR = "E702"
    EMAIL_ERROR = "E703"
    NETWORK_ERROR = "E704"
    CONNECTION_FAILED = "E705"
    
    # Security errors (E8xx)
    SECURITY_ERROR = "E800"
    INJECTION_DETECTED = "E801"
    PATH_TRAVERSAL_DETECTED = "E802"
    INVALID_CREDENTIALS = "E803"
    ENCRYPTION_FAILED = "E804"
    
    # Schedule errors (E9xx)
    SCHEDULE_ERROR = "E900"
    SCHEDULE_NOT_FOUND = "E901"
    SCHEDULE_CONFLICT = "E902"
    INVALID_CRON_EXPRESSION = "E903"


class ErrorSeverity(str, Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PADError(Exception):
    """
    Base exception for PAD Framework with structured error information
    """
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        original_exception: Optional[Exception] = None
    ):
        """
        Initialize PAD Error
        
        Args:
            code: Error code from ErrorCode enum
            message: Human-readable error message
            context: Additional context about the error
            severity: Error severity level
            original_exception: Original exception if wrapped
        """
        self.code = code
        self.message = message
        self.context = context or {}
        self.severity = severity
        self.original_exception = original_exception
        self.timestamp = datetime.now()
        self.traceback_str = traceback.format_exc() if original_exception else None
        
        # Build full error message
        full_message = f"[{code.value}] {message}"
        if context:
            full_message += f" | Context: {context}"
        
        super().__init__(full_message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary"""
        return {
            "code": self.code.value,
            "message": self.message,
            "context": self.context,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback_str
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"[{self.code.value}] {self.message}"


# Specific exception classes

class ConfigurationError(PADError):
    """Configuration-related errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            code=ErrorCode.CONFIGURATION_ERROR,
            message=message,
            context=context,
            severity=ErrorSeverity.HIGH
        )


class ValidationError(PADError):
    """Validation errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            code=ErrorCode.VALIDATION_ERROR,
            message=message,
            context=context,
            severity=ErrorSeverity.MEDIUM
        )


class FlowNotFoundError(PADError):
    """Flow not found"""
    def __init__(self, flow_name: str):
        super().__init__(
            code=ErrorCode.FLOW_NOT_FOUND,
            message=f"Flow '{flow_name}' not found",
            context={"flow_name": flow_name},
            severity=ErrorSeverity.MEDIUM
        )


class FlowExecutionError(PADError):
    """Flow execution errors"""
    def __init__(
        self,
        flow_name: str,
        message: str,
        context: Optional[Dict] = None,
        original_exception: Optional[Exception] = None
    ):
        ctx = {"flow_name": flow_name}
        if context:
            ctx.update(context)
        
        super().__init__(
            code=ErrorCode.EXECUTION_FAILED,
            message=message,
            context=ctx,
            severity=ErrorSeverity.HIGH,
            original_exception=original_exception
        )


class ExecutionTimeoutError(PADError):
    """Execution timeout"""
    def __init__(self, flow_name: str, timeout: int):
        super().__init__(
            code=ErrorCode.EXECUTION_TIMEOUT,
            message=f"Flow execution timed out after {timeout} seconds",
            context={"flow_name": flow_name, "timeout": timeout},
            severity=ErrorSeverity.HIGH
        )


class SecurityError(PADError):
    """Security-related errors"""
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            code=ErrorCode.SECURITY_ERROR,
            message=message,
            context=context,
            severity=ErrorSeverity.CRITICAL
        )


class ResourceError(PADError):
    """Resource-related errors"""
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        context: Optional[Dict] = None
    ):
        super().__init__(
            code=code,
            message=message,
            context=context,
            severity=ErrorSeverity.HIGH
        )


class IntegrationError(PADError):
    """Integration errors"""
    def __init__(
        self,
        service: str,
        message: str,
        context: Optional[Dict] = None
    ):
        ctx = {"service": service}
        if context:
            ctx.update(context)
        
        super().__init__(
            code=ErrorCode.INTEGRATION_ERROR,
            message=message,
            context=ctx,
            severity=ErrorSeverity.MEDIUM
        )


def handle_exception(
    exc: Exception,
    logger,
    context: Optional[Dict[str, Any]] = None
) -> PADError:
    """
    Handle and convert exceptions to PADError
    
    Args:
        exc: Exception to handle
        logger: Logger instance
        context: Additional context
        
    Returns:
        PADError instance
    """
    if isinstance(exc, PADError):
        # Already a PADError, just log it
        logger.error(f"Error occurred: {exc}")
        return exc
    
    # Convert to PADError
    pad_error = PADError(
        code=ErrorCode.UNKNOWN_ERROR,
        message=str(exc),
        context=context,
        severity=ErrorSeverity.MEDIUM,
        original_exception=exc
    )
    
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return pad_error


# Error code descriptions for documentation
ERROR_DESCRIPTIONS = {
    ErrorCode.FLOW_NOT_FOUND: "The specified flow does not exist",
    ErrorCode.EXECUTION_TIMEOUT: "Flow execution exceeded the specified timeout",
    ErrorCode.VALIDATION_ERROR: "Input validation failed",
    ErrorCode.CONFIGURATION_ERROR: "Configuration is invalid or missing",
    ErrorCode.SECURITY_ERROR: "Security violation detected",
    # Add more as needed
}


def get_error_description(code: ErrorCode) -> str:
    """Get human-readable description for error code"""
    return ERROR_DESCRIPTIONS.get(code, "No description available")
