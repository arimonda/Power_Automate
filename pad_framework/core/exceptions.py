"""
Custom Exceptions
Framework-specific exception classes
"""


class PADException(Exception):
    """Base exception for PAD Framework"""
    pass


class FlowExecutionError(PADException):
    """Raised when flow execution fails"""
    pass


class FlowNotFoundError(PADException):
    """Raised when flow is not found"""
    pass


class ConfigurationError(PADException):
    """Raised when configuration is invalid"""
    pass


class ValidationError(PADException):
    """Raised when validation fails"""
    pass


class TimeoutError(PADException):
    """Raised when operation times out"""
    pass


class RetryExhaustedError(PADException):
    """Raised when retry attempts are exhausted"""
    pass


class IntegrationError(PADException):
    """Raised when integration fails"""
    pass


class DatabaseError(PADException):
    """Raised when database operation fails"""
    pass


class AuthenticationError(PADException):
    """Raised when authentication fails"""
    pass


class PermissionError(PADException):
    """Raised when permission is denied"""
    pass
