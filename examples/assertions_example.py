"""
Assertions Examples
Demonstrates assertion framework capabilities
"""

from pad_framework import PADFramework
from pad_framework.testing.assertions import (
    Assertions,
    AssertionSeverity,
    assert_flow_execution
)


def example_basic_assertions():
    """Basic assertion examples"""
    print("="*60)
    print("EXAMPLE 1: Basic Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="Basic Tests")
    
    # Boolean assertions
    assertions.assert_true(True, "True should be true")
    assertions.assert_false(False, "False should be false")
    
    # Equality assertions
    assertions.assert_equal(10, 10, "10 should equal 10")
    assertions.assert_not_equal(5, 10, "5 should not equal 10")
    
    # None assertions
    assertions.assert_is_none(None, "None should be None")
    assertions.assert_is_not_none("value", "String should not be None")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_comparison_assertions():
    """Comparison assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Comparison Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="Comparison Tests")
    
    # Numeric comparisons
    assertions.assert_greater(15, 10, "15 is greater than 10")
    assertions.assert_less(5, 10, "5 is less than 10")
    assertions.assert_in_range(7, 5, 10, "7 is in range [5, 10]")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_collection_assertions():
    """Collection assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Collection Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="Collection Tests")
    
    my_list = [1, 2, 3, 4, 5]
    empty_list = []
    
    # Collection checks
    assertions.assert_contains(my_list, 3, "List should contain 3")
    assertions.assert_not_contains(my_list, 10, "List should not contain 10")
    assertions.assert_length(my_list, 5, "List should have 5 elements")
    assertions.assert_empty(empty_list, "Empty list should be empty")
    assertions.assert_not_empty(my_list, "List should not be empty")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_string_assertions():
    """String assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 4: String Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="String Tests")
    
    text = "Hello, World!"
    
    # String checks
    assertions.assert_starts_with(text, "Hello", "Should start with 'Hello'")
    assertions.assert_ends_with(text, "World!", "Should end with 'World!'")
    assertions.assert_matches_pattern(text, r"Hello.*", "Should match pattern")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_type_assertions():
    """Type assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Type Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="Type Tests")
    
    # Type checks
    assertions.assert_type("text", str, "Should be string")
    assertions.assert_type(123, int, "Should be integer")
    assertions.assert_type(12.5, float, "Should be float")
    assertions.assert_type([1, 2, 3], list, "Should be list")
    assertions.assert_type({"key": "value"}, dict, "Should be dict")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_flow_assertions():
    """Flow-specific assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Flow Assertions")
    print("="*60)
    
    pad = PADFramework()
    assertions = Assertions(suite_name="Flow Tests")
    
    # Execute flow
    print("Executing ExampleFlow...")
    result = pad.execute_flow("ExampleFlow", {"inputParam1": "test", "inputParam2": 1})
    
    # Flow assertions
    assertions.assert_flow_success(result, "Flow should succeed")
    assertions.assert_no_error(result, "Should have no errors")
    assertions.assert_duration_within(result, 60, "Should complete within 60s")
    assertions.assert_output_contains(result, "stdout", "Output should have stdout")
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())
    
    if not suite.passed:
        print("\nFailures:")
        for failure in suite.get_failures():
            print(f"  - {failure}")


def example_severity_levels():
    """Severity level examples"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Severity Levels")
    print("="*60)
    
    assertions = Assertions(suite_name="Severity Tests")
    
    # Critical - Must pass
    assertions.assert_true(
        True,
        "Critical check",
        severity=AssertionSeverity.CRITICAL
    )
    
    # Error - Test failure
    assertions.assert_equal(
        10, 10,
        "Important check",
        severity=AssertionSeverity.ERROR
    )
    
    # Warning - Non-critical
    assertions.assert_not_empty(
        [1, 2, 3],
        "Should have data",
        severity=AssertionSeverity.WARNING
    )
    
    # Info - Informational
    assertions.assert_type(
        "text", str,
        "Type information",
        severity=AssertionSeverity.INFO
    )
    
    # Get results by severity
    suite = assertions.get_suite()
    
    print("\nResults by Severity:")
    for severity in AssertionSeverity:
        results = suite.get_by_severity(severity)
        print(f"  {severity.value.upper()}: {len(results)} assertions")
    
    print(suite.summary())


def example_custom_assertions():
    """Custom assertion examples"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Custom Assertions")
    print("="*60)
    
    assertions = Assertions(suite_name="Custom Tests")
    
    # Custom validation logic
    def validate_data_format():
        data = {"name": "test", "value": 123}
        return "name" in data and "value" in data and isinstance(data["value"], int)
    
    def validate_file_exists():
        import os
        return os.path.exists("flows/example_flow.json")
    
    # Use custom assertions
    assertions.assert_custom(
        condition=validate_data_format,
        name="data_format_validation",
        message="Data should have correct format",
        severity=AssertionSeverity.ERROR
    )
    
    assertions.assert_custom(
        condition=validate_file_exists,
        name="file_existence_check",
        message="Example flow should exist",
        severity=AssertionSeverity.WARNING
    )
    
    # Get results
    suite = assertions.get_suite()
    print(suite.summary())


def example_complete_test_suite():
    """Complete test suite with reporting"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Complete Test Suite with Reporting")
    print("="*60)
    
    pad = PADFramework()
    assertions = Assertions(suite_name="Complete Integration Test")
    generator = ReportGenerator(output_dir="reports")
    
    # Test 1: Flow exists
    print("1. Checking flow exists...")
    flows = pad.list_flows()
    assertions.assert_contains(flows, "ExampleFlow", "ExampleFlow should exist")
    
    # Test 2: Flow is valid
    print("2. Validating flow...")
    validation = pad.validate_flow("ExampleFlow")
    assertions.assert_true(validation["valid"], "Flow should be valid")
    
    # Test 3: Execute flow
    print("3. Executing flow...")
    start_time = datetime.now()
    result = pad.execute_flow("ExampleFlow", {"inputParam1": "test", "inputParam2": 42})
    end_time = datetime.now()
    
    # Assertions
    assertions.assert_flow_success(result, "Execution should succeed")
    assertions.assert_duration_within(result, 120, "Should complete within 2 minutes")
    assertions.assert_no_error(result, "Should have no errors")
    
    # Test 4: Performance check
    print("4. Checking performance...")
    stats = pad.get_performance_stats("ExampleFlow")
    if stats:
        assertions.assert_true(
            stats.get("avg_duration", 999) < 60,
            "Average duration should be < 60s"
        )
    
    # Complete suite
    suite = assertions.complete()
    
    # Generate validation report
    validation_report = ValidationReport(
        flow_name="ExampleFlow",
        timestamp=datetime.now(),
        valid=validation["valid"],
        errors=validation.get("errors", []),
        warnings=validation.get("warnings", []),
        info=validation.get("info", []),
        checks_performed=suite.total_assertions,
        checks_passed=suite.passed_assertions,
        checks_failed=suite.failed_assertions
    )
    
    val_report_path = generator.generate_validation_report(
        validation_report,
        format=ReportFormat.HTML
    )
    
    # Generate execution report
    exec_report = ExecutionReport(
        flow_name=result.flow_name,
        execution_id=result.execution_id,
        status=result.status,
        start_time=start_time,
        end_time=end_time,
        duration=result.duration,
        input_variables={"inputParam1": "test", "inputParam2": 42},
        output=result.output,
        error=result.error
    )
    
    exec_report_path = generator.generate_execution_report(
        exec_report,
        format=ReportFormat.HTML
    )
    
    # Print summary
    print("\n" + "="*60)
    print(suite.summary())
    print("="*60)
    
    print(f"\nReports Generated:")
    print(f"  Validation: {val_report_path}")
    print(f"  Execution: {exec_report_path}")
    
    if suite.passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed:")
        for failure in suite.get_failures():
            print(f"  - {failure}")
        return 1


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("REPORTING & ASSERTIONS EXAMPLES")
    print("="*60)
    print()
    
    try:
        example_execution_report()
        example_validation_report()
        example_performance_report()
        example_summary_report()
        
        example_basic_assertions()
        example_comparison_assertions()
        example_collection_assertions()
        example_string_assertions()
        example_type_assertions()
        example_flow_assertions()
        example_severity_levels()
        example_custom_assertions()
        
        exit_code = example_complete_test_suite()
        
        print("\n" + "="*60)
        print("✓ All examples completed!")
        print("="*60)
        print("\nCheck the 'reports/' folder for generated reports.")
        print()
        
        return exit_code
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
