"""
Comprehensive Tests for Assertion Framework
Tests all assertion types and edge cases
"""

import pytest
from datetime import datetime
from dataclasses import dataclass

from pad_framework.testing.assertions import (
    Assertions,
    AssertionResult,
    AssertionSuite,
    AssertionSeverity,
    assert_flow_execution
)


# Mock FlowExecutionResult for testing
@dataclass
class MockFlowResult:
    """Mock flow execution result"""
    flow_name: str = "TestFlow"
    execution_id: str = "test-123"
    status: str = "success"
    duration: float = 10.5
    output: dict = None
    error: str = None
    
    def __post_init__(self):
        if self.output is None:
            self.output = {"stdout": "output", "stderr": ""}


class TestAssertionResult:
    """Test AssertionResult class"""
    
    def test_assertion_result_passed(self):
        """Test passed assertion result"""
        result = AssertionResult(
            name="test",
            passed=True,
            message="Test passed",
            severity=AssertionSeverity.ERROR,
            expected="expected",
            actual="expected"
        )
        
        assert result.passed is True
        assert "✓ PASS" in str(result)
    
    def test_assertion_result_failed(self):
        """Test failed assertion result"""
        result = AssertionResult(
            name="test",
            passed=False,
            message="Test failed",
            severity=AssertionSeverity.ERROR,
            expected="expected",
            actual="actual"
        )
        
        assert result.passed is False
        assert "✗ FAIL" in str(result)
    
    def test_assertion_result_timestamp(self):
        """Test assertion result has timestamp"""
        result = AssertionResult(
            name="test",
            passed=True,
            message="Test"
        )
        
        assert isinstance(result.timestamp, datetime)


class TestAssertionSuite:
    """Test AssertionSuite class"""
    
    def test_suite_creation(self):
        """Test suite creation"""
        suite = AssertionSuite(name="Test Suite")
        
        assert suite.name == "Test Suite"
        assert suite.total_assertions == 0
        assert suite.passed is True
    
    def test_suite_add_result(self):
        """Test adding results to suite"""
        suite = AssertionSuite(name="Test")
        
        result1 = AssertionResult("test1", True, "Passed")
        result2 = AssertionResult("test2", False, "Failed")
        
        suite.add_result(result1)
        suite.add_result(result2)
        
        assert suite.total_assertions == 2
        assert suite.passed_assertions == 1
        assert suite.failed_assertions == 1
    
    def test_suite_passed_property(self):
        """Test suite passed property"""
        suite = AssertionSuite(name="Test")
        
        # All passed
        suite.add_result(AssertionResult("test1", True, "Passed"))
        suite.add_result(AssertionResult("test2", True, "Passed"))
        assert suite.passed is True
        
        # One failed
        suite.add_result(AssertionResult("test3", False, "Failed"))
        assert suite.passed is False
    
    def test_suite_success_rate(self):
        """Test suite success rate calculation"""
        suite = AssertionSuite(name="Test")
        
        suite.add_result(AssertionResult("test1", True, "Passed"))
        suite.add_result(AssertionResult("test2", True, "Passed"))
        suite.add_result(AssertionResult("test3", False, "Failed"))
        suite.add_result(AssertionResult("test4", False, "Failed"))
        
        assert suite.success_rate == 50.0
    
    def test_suite_get_failures(self):
        """Test getting only failures"""
        suite = AssertionSuite(name="Test")
        
        result1 = AssertionResult("test1", True, "Passed")
        result2 = AssertionResult("test2", False, "Failed")
        result3 = AssertionResult("test3", False, "Failed")
        
        suite.add_result(result1)
        suite.add_result(result2)
        suite.add_result(result3)
        
        failures = suite.get_failures()
        assert len(failures) == 2
        assert all(not f.passed for f in failures)
    
    def test_suite_get_by_severity(self):
        """Test getting assertions by severity"""
        suite = AssertionSuite(name="Test")
        
        suite.add_result(AssertionResult("test1", True, "Critical", AssertionSeverity.CRITICAL))
        suite.add_result(AssertionResult("test2", True, "Error", AssertionSeverity.ERROR))
        suite.add_result(AssertionResult("test3", True, "Warning", AssertionSeverity.WARNING))
        
        criticals = suite.get_by_severity(AssertionSeverity.CRITICAL)
        errors = suite.get_by_severity(AssertionSeverity.ERROR)
        
        assert len(criticals) == 1
        assert len(errors) == 1
    
    def test_suite_summary(self):
        """Test suite summary string"""
        suite = AssertionSuite(name="Test Suite")
        
        suite.add_result(AssertionResult("test1", True, "Passed"))
        suite.add_result(AssertionResult("test2", False, "Failed"))
        
        summary = suite.summary()
        
        assert "Test Suite" in summary
        assert "2" in summary  # Total
        assert "1" in summary  # Passed
        assert "1" in summary  # Failed
    
    def test_suite_complete(self):
        """Test marking suite as complete"""
        suite = AssertionSuite(name="Test")
        
        assert suite.end_time is None
        suite.complete()
        assert suite.end_time is not None


class TestBasicAssertions:
    """Test basic assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Basic Tests")
    
    def test_assert_true_pass(self, assertions):
        """Test assert_true passes"""
        result = assertions.assert_true(True, "Should be true")
        assert result.passed is True
    
    def test_assert_true_fail(self, assertions):
        """Test assert_true fails"""
        result = assertions.assert_true(False, "Should be true")
        assert result.passed is False
    
    def test_assert_false_pass(self, assertions):
        """Test assert_false passes"""
        result = assertions.assert_false(False, "Should be false")
        assert result.passed is True
    
    def test_assert_false_fail(self, assertions):
        """Test assert_false fails"""
        result = assertions.assert_false(True, "Should be false")
        assert result.passed is False
    
    def test_assert_equal_pass(self, assertions):
        """Test assert_equal passes"""
        result = assertions.assert_equal(10, 10, "Should be equal")
        assert result.passed is True
    
    def test_assert_equal_fail(self, assertions):
        """Test assert_equal fails"""
        result = assertions.assert_equal(10, 20, "Should be equal")
        assert result.passed is False
    
    def test_assert_not_equal_pass(self, assertions):
        """Test assert_not_equal passes"""
        result = assertions.assert_not_equal(10, 20, "Should not be equal")
        assert result.passed is True
    
    def test_assert_not_equal_fail(self, assertions):
        """Test assert_not_equal fails"""
        result = assertions.assert_not_equal(10, 10, "Should not be equal")
        assert result.passed is False
    
    def test_assert_is_none_pass(self, assertions):
        """Test assert_is_none passes"""
        result = assertions.assert_is_none(None, "Should be None")
        assert result.passed is True
    
    def test_assert_is_none_fail(self, assertions):
        """Test assert_is_none fails"""
        result = assertions.assert_is_none("value", "Should be None")
        assert result.passed is False
    
    def test_assert_is_not_none_pass(self, assertions):
        """Test assert_is_not_none passes"""
        result = assertions.assert_is_not_none("value", "Should not be None")
        assert result.passed is True
    
    def test_assert_is_not_none_fail(self, assertions):
        """Test assert_is_not_none fails"""
        result = assertions.assert_is_not_none(None, "Should not be None")
        assert result.passed is False


class TestComparisonAssertions:
    """Test comparison assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Comparison Tests")
    
    def test_assert_greater_pass(self, assertions):
        """Test assert_greater passes"""
        result = assertions.assert_greater(20, 10, "Should be greater")
        assert result.passed is True
    
    def test_assert_greater_fail(self, assertions):
        """Test assert_greater fails"""
        result = assertions.assert_greater(5, 10, "Should be greater")
        assert result.passed is False
    
    def test_assert_less_pass(self, assertions):
        """Test assert_less passes"""
        result = assertions.assert_less(5, 10, "Should be less")
        assert result.passed is True
    
    def test_assert_less_fail(self, assertions):
        """Test assert_less fails"""
        result = assertions.assert_less(20, 10, "Should be less")
        assert result.passed is False
    
    def test_assert_in_range_pass(self, assertions):
        """Test assert_in_range passes"""
        result = assertions.assert_in_range(7, 5, 10, "Should be in range")
        assert result.passed is True
    
    def test_assert_in_range_fail_below(self, assertions):
        """Test assert_in_range fails (below)"""
        result = assertions.assert_in_range(3, 5, 10, "Should be in range")
        assert result.passed is False
    
    def test_assert_in_range_fail_above(self, assertions):
        """Test assert_in_range fails (above)"""
        result = assertions.assert_in_range(15, 5, 10, "Should be in range")
        assert result.passed is False
    
    def test_assert_in_range_boundary(self, assertions):
        """Test assert_in_range boundary values"""
        result1 = assertions.assert_in_range(5, 5, 10, "Min boundary")
        result2 = assertions.assert_in_range(10, 5, 10, "Max boundary")
        
        assert result1.passed is True
        assert result2.passed is True


class TestCollectionAssertions:
    """Test collection assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Collection Tests")
    
    def test_assert_contains_pass(self, assertions):
        """Test assert_contains passes"""
        result = assertions.assert_contains([1, 2, 3], 2, "Should contain")
        assert result.passed is True
    
    def test_assert_contains_fail(self, assertions):
        """Test assert_contains fails"""
        result = assertions.assert_contains([1, 2, 3], 5, "Should contain")
        assert result.passed is False
    
    def test_assert_not_contains_pass(self, assertions):
        """Test assert_not_contains passes"""
        result = assertions.assert_not_contains([1, 2, 3], 5, "Should not contain")
        assert result.passed is True
    
    def test_assert_not_contains_fail(self, assertions):
        """Test assert_not_contains fails"""
        result = assertions.assert_not_contains([1, 2, 3], 2, "Should not contain")
        assert result.passed is False
    
    def test_assert_length_pass(self, assertions):
        """Test assert_length passes"""
        result = assertions.assert_length([1, 2, 3], 3, "Should have length 3")
        assert result.passed is True
    
    def test_assert_length_fail(self, assertions):
        """Test assert_length fails"""
        result = assertions.assert_length([1, 2, 3], 5, "Should have length 5")
        assert result.passed is False
    
    def test_assert_empty_pass(self, assertions):
        """Test assert_empty passes"""
        result = assertions.assert_empty([], "Should be empty")
        assert result.passed is True
    
    def test_assert_empty_fail(self, assertions):
        """Test assert_empty fails"""
        result = assertions.assert_empty([1, 2, 3], "Should be empty")
        assert result.passed is False
    
    def test_assert_not_empty_pass(self, assertions):
        """Test assert_not_empty passes"""
        result = assertions.assert_not_empty([1, 2, 3], "Should not be empty")
        assert result.passed is True
    
    def test_assert_not_empty_fail(self, assertions):
        """Test assert_not_empty fails"""
        result = assertions.assert_not_empty([], "Should not be empty")
        assert result.passed is False


class TestStringAssertions:
    """Test string assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="String Tests")
    
    def test_assert_starts_with_pass(self, assertions):
        """Test assert_starts_with passes"""
        result = assertions.assert_starts_with("Hello World", "Hello", "Should start with")
        assert result.passed is True
    
    def test_assert_starts_with_fail(self, assertions):
        """Test assert_starts_with fails"""
        result = assertions.assert_starts_with("Hello World", "World", "Should start with")
        assert result.passed is False
    
    def test_assert_ends_with_pass(self, assertions):
        """Test assert_ends_with passes"""
        result = assertions.assert_ends_with("Hello World", "World", "Should end with")
        assert result.passed is True
    
    def test_assert_ends_with_fail(self, assertions):
        """Test assert_ends_with fails"""
        result = assertions.assert_ends_with("Hello World", "Hello", "Should end with")
        assert result.passed is False
    
    def test_assert_matches_pattern_pass(self, assertions):
        """Test assert_matches_pattern passes"""
        result = assertions.assert_matches_pattern("test123", r"test\d+", "Should match")
        assert result.passed is True
    
    def test_assert_matches_pattern_fail(self, assertions):
        """Test assert_matches_pattern fails"""
        result = assertions.assert_matches_pattern("testABC", r"test\d+", "Should match")
        assert result.passed is False


class TestTypeAssertions:
    """Test type assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Type Tests")
    
    def test_assert_type_string(self, assertions):
        """Test assert_type for string"""
        result = assertions.assert_type("text", str, "Should be string")
        assert result.passed is True
    
    def test_assert_type_int(self, assertions):
        """Test assert_type for int"""
        result = assertions.assert_type(123, int, "Should be int")
        assert result.passed is True
    
    def test_assert_type_fail(self, assertions):
        """Test assert_type fails"""
        result = assertions.assert_type("123", int, "Should be int")
        assert result.passed is False
    
    def test_assert_type_list(self, assertions):
        """Test assert_type for list"""
        result = assertions.assert_type([1, 2, 3], list, "Should be list")
        assert result.passed is True
    
    def test_assert_type_dict(self, assertions):
        """Test assert_type for dict"""
        result = assertions.assert_type({"key": "value"}, dict, "Should be dict")
        assert result.passed is True


class TestFlowAssertions:
    """Test flow-specific assertion methods"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Flow Tests")
    
    def test_assert_flow_success_pass(self, assertions):
        """Test assert_flow_success passes"""
        result_obj = MockFlowResult(status="success")
        result = assertions.assert_flow_success(result_obj, "Should succeed")
        assert result.passed is True
    
    def test_assert_flow_success_fail(self, assertions):
        """Test assert_flow_success fails"""
        result_obj = MockFlowResult(status="failed")
        result = assertions.assert_flow_success(result_obj, "Should succeed")
        assert result.passed is False
    
    def test_assert_flow_failed_pass(self, assertions):
        """Test assert_flow_failed passes"""
        result_obj = MockFlowResult(status="failed")
        result = assertions.assert_flow_failed(result_obj, "Should fail")
        assert result.passed is True
    
    def test_assert_duration_within_pass(self, assertions):
        """Test assert_duration_within passes"""
        result_obj = MockFlowResult(duration=30.0)
        result = assertions.assert_duration_within(result_obj, 60, "Should be within")
        assert result.passed is True
    
    def test_assert_duration_within_fail(self, assertions):
        """Test assert_duration_within fails"""
        result_obj = MockFlowResult(duration=90.0)
        result = assertions.assert_duration_within(result_obj, 60, "Should be within")
        assert result.passed is False
    
    def test_assert_output_contains_pass(self, assertions):
        """Test assert_output_contains passes"""
        result_obj = MockFlowResult(output={"key": "value", "data": [1, 2, 3]})
        result = assertions.assert_output_contains(result_obj, "key", "Should contain")
        assert result.passed is True
    
    def test_assert_output_contains_fail(self, assertions):
        """Test assert_output_contains fails"""
        result_obj = MockFlowResult(output={"key": "value"})
        result = assertions.assert_output_contains(result_obj, "missing", "Should contain")
        assert result.passed is False
    
    def test_assert_no_error_pass(self, assertions):
        """Test assert_no_error passes"""
        result_obj = MockFlowResult(error=None)
        result = assertions.assert_no_error(result_obj, "Should have no error")
        assert result.passed is True
    
    def test_assert_no_error_fail(self, assertions):
        """Test assert_no_error fails"""
        result_obj = MockFlowResult(error="Something went wrong")
        result = assertions.assert_no_error(result_obj, "Should have no error")
        assert result.passed is False


class TestCustomAssertions:
    """Test custom assertion functionality"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Custom Tests")
    
    def test_assert_custom_pass(self, assertions):
        """Test assert_custom passes"""
        def check():
            return True
        
        result = assertions.assert_custom(check, "custom_test", "Custom check")
        assert result.passed is True
    
    def test_assert_custom_fail(self, assertions):
        """Test assert_custom fails"""
        def check():
            return False
        
        result = assertions.assert_custom(check, "custom_test", "Custom check")
        assert result.passed is False
    
    def test_assert_custom_exception(self, assertions):
        """Test assert_custom handles exceptions"""
        def check():
            raise ValueError("Test error")
        
        result = assertions.assert_custom(check, "custom_test", "Custom check")
        assert result.passed is False
        assert "Test error" in result.message


class TestAssertionSeverity:
    """Test assertion severity levels"""
    
    @pytest.fixture
    def assertions(self):
        return Assertions(suite_name="Severity Tests")
    
    def test_critical_severity(self, assertions):
        """Test critical severity"""
        result = assertions.assert_true(
            True,
            "Critical check",
            severity=AssertionSeverity.CRITICAL
        )
        assert result.severity == AssertionSeverity.CRITICAL
    
    def test_error_severity(self, assertions):
        """Test error severity"""
        result = assertions.assert_true(
            True,
            "Error check",
            severity=AssertionSeverity.ERROR
        )
        assert result.severity == AssertionSeverity.ERROR
    
    def test_warning_severity(self, assertions):
        """Test warning severity"""
        result = assertions.assert_true(
            True,
            "Warning check",
            severity=AssertionSeverity.WARNING
        )
        assert result.severity == AssertionSeverity.WARNING
    
    def test_info_severity(self, assertions):
        """Test info severity"""
        result = assertions.assert_true(
            True,
            "Info check",
            severity=AssertionSeverity.INFO
        )
        assert result.severity == AssertionSeverity.INFO


class TestAssertionsSuiteManagement:
    """Test assertions suite management"""
    
    def test_get_suite(self):
        """Test getting suite"""
        assertions = Assertions(suite_name="Test")
        assertions.assert_true(True, "Test")
        
        suite = assertions.get_suite()
        assert suite.name == "Test"
        assert suite.total_assertions == 1
    
    def test_complete_suite(self):
        """Test completing suite"""
        assertions = Assertions(suite_name="Test")
        assertions.assert_true(True, "Test")
        
        suite = assertions.complete()
        assert suite.end_time is not None
    
    def test_reset_suite(self):
        """Test resetting suite"""
        assertions = Assertions(suite_name="Test1")
        assertions.assert_true(True, "Test")
        
        assert assertions.get_suite().total_assertions == 1
        
        assertions.reset(suite_name="Test2")
        assert assertions.get_suite().total_assertions == 0
        assert assertions.get_suite().name == "Test2"


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_assert_flow_execution(self):
        """Test assert_flow_execution convenience function"""
        result_obj = MockFlowResult(
            status="success",
            duration=10.5,
            error=None
        )
        
        assertions = assert_flow_execution(result_obj)
        suite = assertions.get_suite()
        
        # Should perform multiple checks
        assert suite.total_assertions > 0
        assert "Flow Execution" in suite.name


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
