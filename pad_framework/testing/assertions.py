"""
Assertion Framework
Comprehensive assertion and validation utilities for testing
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AssertionSeverity(str, Enum):
    """Assertion severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class AssertionResult:
    """Result of an assertion"""
    name: str
    passed: bool
    message: str
    severity: AssertionSeverity = AssertionSeverity.ERROR
    expected: Any = None
    actual: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"[{self.severity.value.upper()}] {status}: {self.name} - {self.message}"


@dataclass
class AssertionSuite:
    """Collection of assertion results"""
    name: str
    results: List[AssertionResult] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def passed(self) -> bool:
        """Check if all assertions passed"""
        return all(r.passed for r in self.results)
    
    @property
    def total_assertions(self) -> int:
        """Total number of assertions"""
        return len(self.results)
    
    @property
    def passed_assertions(self) -> int:
        """Number of passed assertions"""
        return sum(1 for r in self.results if r.passed)
    
    @property
    def failed_assertions(self) -> int:
        """Number of failed assertions"""
        return sum(1 for r in self.results if not r.passed)
    
    @property
    def success_rate(self) -> float:
        """Success rate percentage"""
        if self.total_assertions == 0:
            return 0.0
        return (self.passed_assertions / self.total_assertions) * 100
    
    def add_result(self, result: AssertionResult) -> None:
        """Add assertion result to suite"""
        self.results.append(result)
    
    def complete(self) -> None:
        """Mark suite as complete"""
        self.end_time = datetime.now()
    
    def get_failures(self) -> List[AssertionResult]:
        """Get only failed assertions"""
        return [r for r in self.results if not r.passed]
    
    def get_by_severity(self, severity: AssertionSeverity) -> List[AssertionResult]:
        """Get assertions by severity"""
        return [r for r in self.results if r.severity == severity]
    
    def summary(self) -> str:
        """Get summary string"""
        return f"""
Assertion Suite: {self.name}
Total Assertions: {self.total_assertions}
Passed: {self.passed_assertions}
Failed: {self.failed_assertions}
Success Rate: {self.success_rate:.1f}%
Status: {'✓ PASSED' if self.passed else '✗ FAILED'}
"""


class Assertions:
    """
    Comprehensive assertion utilities
    """
    
    def __init__(self, suite_name: str = "Default"):
        """
        Initialize assertions
        
        Args:
            suite_name: Name of assertion suite
        """
        self.suite = AssertionSuite(name=suite_name)
    
    # Basic Assertions
    
    def assert_true(
        self,
        condition: bool,
        message: str = "Condition should be true",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that condition is true"""
        result = AssertionResult(
            name="assert_true",
            passed=condition is True,
            message=message,
            severity=severity,
            expected=True,
            actual=condition
        )
        self.suite.add_result(result)
        return result
    
    def assert_false(
        self,
        condition: bool,
        message: str = "Condition should be false",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that condition is false"""
        result = AssertionResult(
            name="assert_false",
            passed=condition is False,
            message=message,
            severity=severity,
            expected=False,
            actual=condition
        )
        self.suite.add_result(result)
        return result
    
    def assert_equal(
        self,
        actual: Any,
        expected: Any,
        message: str = "Values should be equal",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that values are equal"""
        result = AssertionResult(
            name="assert_equal",
            passed=actual == expected,
            message=message,
            severity=severity,
            expected=expected,
            actual=actual
        )
        self.suite.add_result(result)
        return result
    
    def assert_not_equal(
        self,
        actual: Any,
        expected: Any,
        message: str = "Values should not be equal",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that values are not equal"""
        result = AssertionResult(
            name="assert_not_equal",
            passed=actual != expected,
            message=message,
            severity=severity,
            expected=f"!= {expected}",
            actual=actual
        )
        self.suite.add_result(result)
        return result
    
    def assert_is_none(
        self,
        value: Any,
        message: str = "Value should be None",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is None"""
        result = AssertionResult(
            name="assert_is_none",
            passed=value is None,
            message=message,
            severity=severity,
            expected=None,
            actual=value
        )
        self.suite.add_result(result)
        return result
    
    def assert_is_not_none(
        self,
        value: Any,
        message: str = "Value should not be None",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is not None"""
        result = AssertionResult(
            name="assert_is_not_none",
            passed=value is not None,
            message=message,
            severity=severity,
            expected="not None",
            actual=value
        )
        self.suite.add_result(result)
        return result
    
    # Comparison Assertions
    
    def assert_greater(
        self,
        actual: Any,
        threshold: Any,
        message: str = "Value should be greater",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is greater than threshold"""
        result = AssertionResult(
            name="assert_greater",
            passed=actual > threshold,
            message=message,
            severity=severity,
            expected=f"> {threshold}",
            actual=actual
        )
        self.suite.add_result(result)
        return result
    
    def assert_less(
        self,
        actual: Any,
        threshold: Any,
        message: str = "Value should be less",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is less than threshold"""
        result = AssertionResult(
            name="assert_less",
            passed=actual < threshold,
            message=message,
            severity=severity,
            expected=f"< {threshold}",
            actual=actual
        )
        self.suite.add_result(result)
        return result
    
    def assert_in_range(
        self,
        value: float,
        min_value: float,
        max_value: float,
        message: str = "Value should be in range",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is within range"""
        result = AssertionResult(
            name="assert_in_range",
            passed=min_value <= value <= max_value,
            message=message,
            severity=severity,
            expected=f"[{min_value}, {max_value}]",
            actual=value
        )
        self.suite.add_result(result)
        return result
    
    # Collection Assertions
    
    def assert_contains(
        self,
        collection: Any,
        item: Any,
        message: str = "Collection should contain item",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that collection contains item"""
        result = AssertionResult(
            name="assert_contains",
            passed=item in collection,
            message=message,
            severity=severity,
            expected=f"contains {item}",
            actual=collection
        )
        self.suite.add_result(result)
        return result
    
    def assert_not_contains(
        self,
        collection: Any,
        item: Any,
        message: str = "Collection should not contain item",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that collection does not contain item"""
        result = AssertionResult(
            name="assert_not_contains",
            passed=item not in collection,
            message=message,
            severity=severity,
            expected=f"not contains {item}",
            actual=collection
        )
        self.suite.add_result(result)
        return result
    
    def assert_length(
        self,
        collection: Any,
        expected_length: int,
        message: str = "Collection should have expected length",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that collection has expected length"""
        actual_length = len(collection)
        result = AssertionResult(
            name="assert_length",
            passed=actual_length == expected_length,
            message=message,
            severity=severity,
            expected=expected_length,
            actual=actual_length
        )
        self.suite.add_result(result)
        return result
    
    def assert_empty(
        self,
        collection: Any,
        message: str = "Collection should be empty",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that collection is empty"""
        result = AssertionResult(
            name="assert_empty",
            passed=len(collection) == 0,
            message=message,
            severity=severity,
            expected=0,
            actual=len(collection)
        )
        self.suite.add_result(result)
        return result
    
    def assert_not_empty(
        self,
        collection: Any,
        message: str = "Collection should not be empty",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that collection is not empty"""
        result = AssertionResult(
            name="assert_not_empty",
            passed=len(collection) > 0,
            message=message,
            severity=severity,
            expected="> 0",
            actual=len(collection)
        )
        self.suite.add_result(result)
        return result
    
    # String Assertions
    
    def assert_starts_with(
        self,
        string: str,
        prefix: str,
        message: str = "String should start with prefix",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that string starts with prefix"""
        result = AssertionResult(
            name="assert_starts_with",
            passed=string.startswith(prefix),
            message=message,
            severity=severity,
            expected=f"starts with '{prefix}'",
            actual=string
        )
        self.suite.add_result(result)
        return result
    
    def assert_ends_with(
        self,
        string: str,
        suffix: str,
        message: str = "String should end with suffix",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that string ends with suffix"""
        result = AssertionResult(
            name="assert_ends_with",
            passed=string.endswith(suffix),
            message=message,
            severity=severity,
            expected=f"ends with '{suffix}'",
            actual=string
        )
        self.suite.add_result(result)
        return result
    
    def assert_matches_pattern(
        self,
        string: str,
        pattern: str,
        message: str = "String should match pattern",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that string matches regex pattern"""
        import re
        result = AssertionResult(
            name="assert_matches_pattern",
            passed=bool(re.match(pattern, string)),
            message=message,
            severity=severity,
            expected=f"matches '{pattern}'",
            actual=string
        )
        self.suite.add_result(result)
        return result
    
    # Type Assertions
    
    def assert_type(
        self,
        value: Any,
        expected_type: type,
        message: str = "Value should be of expected type",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that value is of expected type"""
        result = AssertionResult(
            name="assert_type",
            passed=isinstance(value, expected_type),
            message=message,
            severity=severity,
            expected=expected_type.__name__,
            actual=type(value).__name__
        )
        self.suite.add_result(result)
        return result
    
    # Flow-Specific Assertions
    
    def assert_flow_success(
        self,
        result: Any,
        message: str = "Flow should succeed",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that flow execution succeeded"""
        status = getattr(result, 'status', None)
        result_obj = AssertionResult(
            name="assert_flow_success",
            passed=status == "success",
            message=message,
            severity=severity,
            expected="success",
            actual=status
        )
        self.suite.add_result(result_obj)
        return result_obj
    
    def assert_flow_failed(
        self,
        result: Any,
        message: str = "Flow should fail",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that flow execution failed"""
        status = getattr(result, 'status', None)
        result_obj = AssertionResult(
            name="assert_flow_failed",
            passed=status == "failed",
            message=message,
            severity=severity,
            expected="failed",
            actual=status
        )
        self.suite.add_result(result_obj)
        return result_obj
    
    def assert_duration_within(
        self,
        result: Any,
        max_duration: float,
        message: str = "Flow should complete within time limit",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that flow completed within duration"""
        duration = getattr(result, 'duration', None)
        result_obj = AssertionResult(
            name="assert_duration_within",
            passed=duration is not None and duration <= max_duration,
            message=message,
            severity=severity,
            expected=f"<= {max_duration}s",
            actual=f"{duration}s" if duration else "None"
        )
        self.suite.add_result(result_obj)
        return result_obj
    
    def assert_output_contains(
        self,
        result: Any,
        key: str,
        message: str = "Output should contain key",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that flow output contains key"""
        output = getattr(result, 'output', {})
        result_obj = AssertionResult(
            name="assert_output_contains",
            passed=key in output,
            message=message,
            severity=severity,
            expected=f"contains '{key}'",
            actual=list(output.keys()) if output else []
        )
        self.suite.add_result(result_obj)
        return result_obj
    
    def assert_no_error(
        self,
        result: Any,
        message: str = "Flow should have no errors",
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Assert that flow has no errors"""
        error = getattr(result, 'error', None)
        result_obj = AssertionResult(
            name="assert_no_error",
            passed=error is None or error == "",
            message=message,
            severity=severity,
            expected="None",
            actual=error
        )
        self.suite.add_result(result_obj)
        return result_obj
    
    # Custom Assertion
    
    def assert_custom(
        self,
        condition: Callable[[], bool],
        name: str,
        message: str,
        severity: AssertionSeverity = AssertionSeverity.ERROR
    ) -> AssertionResult:
        """Execute custom assertion function"""
        try:
            passed = condition()
        except Exception as e:
            passed = False
            message = f"{message} (Exception: {str(e)})"
        
        result = AssertionResult(
            name=name,
            passed=passed,
            message=message,
            severity=severity
        )
        self.suite.add_result(result)
        return result
    
    # Suite Management
    
    def get_suite(self) -> AssertionSuite:
        """Get the assertion suite"""
        return self.suite
    
    def complete(self) -> AssertionSuite:
        """Complete the assertion suite"""
        self.suite.complete()
        return self.suite
    
    def reset(self, suite_name: str = "Default") -> None:
        """Reset assertions with new suite"""
        self.suite = AssertionSuite(name=suite_name)


# Convenience functions

def assert_flow_execution(result: Any) -> Assertions:
    """
    Convenience function to assert common flow execution conditions
    
    Args:
        result: Flow execution result
        
    Returns:
        Assertions instance with results
    """
    assertions = Assertions(suite_name=f"Flow Execution: {getattr(result, 'flow_name', 'Unknown')}")
    
    # Basic checks
    assertions.assert_flow_success(result, "Flow should execute successfully")
    assertions.assert_no_error(result, "Flow should have no errors")
    assertions.assert_is_not_none(result, "Result should not be None")
    
    # Duration check
    duration = getattr(result, 'duration', None)
    if duration is not None:
        assertions.assert_greater(duration, 0, "Duration should be positive")
    
    return assertions
