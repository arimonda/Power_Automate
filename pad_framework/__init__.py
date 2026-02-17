"""
Power Automate Desktop Framework
Main package initialization
"""

from .core.framework import PADFramework
from .core.config import Config, FlowConfig
from .core.exceptions import (
    PADException,
    FlowExecutionError,
    FlowNotFoundError,
    ConfigurationError,
    ValidationError
)
from .core.error_codes import (
    PADError,
    ErrorCode,
    ErrorSeverity
)
from .core.validation import (
    validate_flow_execution,
    validate_flow_creation,
    validate_schedule,
    FlowExecutionRequest,
    PathValidator,
    CommandValidator,
    InputSanitizer
)
from .flows.flow_manager import FlowManager
from .flows.flow_executor import FlowExecutor, FlowExecutionResult
from .flows.async_executor import AsyncFlowExecutor
from .testing.test_runner import TestRunner
from .testing.assertions import Assertions, AssertionSeverity, assert_flow_execution
from .utils.logger import Logger
from .reporting import (
    ReportGenerator,
    ReportFormat,
    ReportType,
    ExecutionReport,
    ValidationReport,
    PerformanceReport
)
from .monitoring.metrics import MetricsCollector, get_metrics_collector

__version__ = "1.1.0"
__author__ = "Power Automate Desktop Framework Team"
__all__ = [
    # Core
    "PADFramework",
    "Config",
    "FlowConfig",
    
    # Flows
    "FlowManager",
    "FlowExecutor",
    "FlowExecutionResult",
    "AsyncFlowExecutor",
    
    # Testing
    "TestRunner",
    "Assertions",
    "AssertionSeverity",
    "assert_flow_execution",
    
    # Reporting
    "ReportGenerator",
    "ReportFormat",
    "ReportType",
    "ExecutionReport",
    "ValidationReport",
    "PerformanceReport",
    
    # Validation
    "validate_flow_execution",
    "validate_flow_creation",
    "validate_schedule",
    "FlowExecutionRequest",
    "PathValidator",
    "CommandValidator",
    "InputSanitizer",
    
    # Errors
    "PADException",
    "PADError",
    "ErrorCode",
    "ErrorSeverity",
    "FlowExecutionError",
    "FlowNotFoundError",
    "ConfigurationError",
    "ValidationError",
    
    # Utilities
    "Logger",
    "MetricsCollector",
    "get_metrics_collector"
]
