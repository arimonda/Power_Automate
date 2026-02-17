# Reporting and Assertions Guide

## 📊 Comprehensive Reporting & Validation Features

**Version**: 1.1.0  
**Last Updated**: February 11, 2026  
**Status**: ✅ Fully Implemented

---

## Overview

The PAD Framework now includes comprehensive **reporting** and **assertion/validation** capabilities for testing, monitoring, and documenting flow executions.

---

## 📊 Reporting System

### Features

✅ **Multiple Report Formats**: HTML, JSON, Markdown, CSV, Text  
✅ **Report Types**: Execution, Validation, Performance, Summary  
✅ **Professional Templates**: Beautiful HTML reports  
✅ **Automated Generation**: Generate reports programmatically  
✅ **Customizable**: Flexible report configuration

---

## 📝 Report Types

### 1. Execution Report

Detailed report of a single flow execution.

**Usage**:
```python
from pad_framework.reporting import ReportGenerator, ExecutionReport, ReportFormat
from datetime import datetime

# Create report data
report_data = ExecutionReport(
    flow_name="DataProcessor",
    execution_id="abc-123",
    status="success",
    start_time=datetime.now(),
    end_time=datetime.now(),
    duration=45.5,
    input_variables={"file": "data.csv"},
    output={"records_processed": 1250},
    retry_attempts=0
)

# Generate report
generator = ReportGenerator(output_dir="reports")
report_path = generator.generate_execution_report(
    report_data,
    format=ReportFormat.HTML
)

print(f"Report saved to: {report_path}")
```

**Includes**:
- Execution details (status, duration, timestamps)
- Input variables
- Output data
- Errors and warnings
- Retry information

---

### 2. Validation Report

Report on flow validation results.

**Usage**:
```python
from pad_framework.reporting import ValidationReport

# Create validation report
validation_data = ValidationReport(
    flow_name="MyFlow",
    timestamp=datetime.now(),
    valid=True,
    errors=[],
    warnings=["Flow has no description"],
    info=["Flow validation completed"],
    checks_performed=10,
    checks_passed=9,
    checks_failed=1
)

# Generate report
report_path = generator.generate_validation_report(
    validation_data,
    format=ReportFormat.MARKDOWN
)
```

**Includes**:
- Validation status
- Success rate
- Errors, warnings, and info
- Checks summary
- Detailed results

---

### 3. Performance Report

Comprehensive performance analysis.

**Usage**:
```python
from pad_framework.reporting import PerformanceReport

# Create performance report
perf_data = PerformanceReport(
    flow_name="DataProcessor",
    period_start=datetime.now(),
    period_end=datetime.now(),
    total_executions=100,
    successful_executions=95,
    failed_executions=5,
    avg_duration=12.5,
    min_duration=8.2,
    max_duration=45.7,
    p50_duration=11.3,
    p95_duration=25.8,
    p99_duration=42.1,
    avg_memory_mb=125.5,
    max_memory_mb=256.0,
    avg_cpu_percent=35.2,
    error_rate=5.0
)

# Generate report
report_path = generator.generate_performance_report(
    perf_data,
    format=ReportFormat.HTML
)
```

**Includes**:
- Execution statistics
- Duration percentiles (P50, P95, P99)
- Resource usage (CPU, memory)
- Success/error rates
- Performance trends

---

### 4. Summary Report

Overview of multiple flows.

**Usage**:
```python
# Create summary data
flows_data = [
    {
        "name": "Flow1",
        "executions": 100,
        "success_rate": 95.0,
        "avg_duration": 12.5,
        "last_execution": "2026-02-11 10:30:00"
    },
    {
        "name": "Flow2",
        "executions": 50,
        "success_rate": 98.0,
        "avg_duration": 8.3,
        "last_execution": "2026-02-11 09:15:00"
    }
]

# Generate summary
report_path = generator.generate_summary_report(
    flows_data,
    format=ReportFormat.HTML
)
```

**Includes**:
- All flows overview
- Key metrics comparison
- Status summary
- Performance comparison

---

## 🧪 Assertion Framework

### Features

✅ **Comprehensive Assertions**: 20+ assertion types  
✅ **Flow-Specific**: Assertions for flow executions  
✅ **Severity Levels**: Critical, Error, Warning, Info  
✅ **Suite Management**: Organize assertions into suites  
✅ **Detailed Results**: Complete assertion results with context

---

## 🔍 Assertion Types

### Basic Assertions

```python
from pad_framework.testing.assertions import Assertions, AssertionSeverity

# Create assertions suite
assertions = Assertions(suite_name="My Tests")

# Boolean assertions
assertions.assert_true(True, "Condition should be true")
assertions.assert_false(False, "Condition should be false")

# Equality assertions
assertions.assert_equal(actual=10, expected=10, "Values should match")
assertions.assert_not_equal(actual=5, expected=10, "Values should differ")

# None assertions
assertions.assert_is_none(None, "Should be None")
assertions.assert_is_not_none("value", "Should not be None")
```

---

### Comparison Assertions

```python
# Numeric comparisons
assertions.assert_greater(actual=15, threshold=10, "Should be greater")
assertions.assert_less(actual=5, threshold=10, "Should be less")
assertions.assert_in_range(value=7, min_value=5, max_value=10, "Should be in range")
```

---

### Collection Assertions

```python
# Collection operations
my_list = [1, 2, 3, 4, 5]

assertions.assert_contains(my_list, 3, "Should contain 3")
assertions.assert_not_contains(my_list, 10, "Should not contain 10")
assertions.assert_length(my_list, 5, "Should have 5 elements")
assertions.assert_empty([], "Should be empty")
assertions.assert_not_empty(my_list, "Should not be empty")
```

---

### String Assertions

```python
# String operations
text = "Hello, World!"

assertions.assert_starts_with(text, "Hello", "Should start with Hello")
assertions.assert_ends_with(text, "World!", "Should end with World!")
assertions.assert_matches_pattern(text, r"Hello.*", "Should match pattern")
```

---

### Type Assertions

```python
# Type checking
assertions.assert_type(value="text", expected_type=str, "Should be string")
assertions.assert_type(value=123, expected_type=int, "Should be integer")
```

---

### Flow-Specific Assertions

```python
# Flow execution assertions
result = pad.execute_flow("MyFlow", {})

# Check flow succeeded
assertions.assert_flow_success(result, "Flow should succeed")

# Check no errors
assertions.assert_no_error(result, "Should have no errors")

# Check duration
assertions.assert_duration_within(result, max_duration=60, "Should complete in <60s")

# Check output
assertions.assert_output_contains(result, "result_key", "Output should have result_key")
```

---

## 🎯 Complete Example

### End-to-End Testing with Assertions and Reporting

```python
from pad_framework import PADFramework
from pad_framework.testing.assertions import Assertions, AssertionSeverity
from pad_framework.reporting import (
    ReportGenerator,
    ExecutionReport,
    ValidationReport,
    ReportFormat
)
from datetime import datetime

# Initialize
pad = PADFramework()
assertions = Assertions(suite_name="MyFlow Test Suite")
reporter = ReportGenerator(output_dir="reports")

# Test 1: Validate flow
print("1. Validating flow...")
validation = pad.validate_flow("MyFlow")

assertions.assert_true(
    validation["valid"],
    "Flow should be valid",
    severity=AssertionSeverity.CRITICAL
)

# Generate validation report
validation_report = ValidationReport(
    flow_name="MyFlow",
    timestamp=datetime.now(),
    valid=validation["valid"],
    errors=validation.get("errors", []),
    warnings=validation.get("warnings", []),
    info=validation.get("info", []),
    checks_performed=5,
    checks_passed=5 if validation["valid"] else 0,
    checks_failed=0 if validation["valid"] else 5
)

validation_report_path = reporter.generate_validation_report(
    validation_report,
    format=ReportFormat.HTML
)
print(f"✓ Validation report: {validation_report_path}")

# Test 2: Execute flow
print("2. Executing flow...")
start_time = datetime.now()
result = pad.execute_flow("MyFlow", {"param": "value"})
end_time = datetime.now()

# Assertions
assertions.assert_flow_success(result, "Flow should execute successfully")
assertions.assert_no_error(result, "Should have no errors")
assertions.assert_duration_within(result, 60, "Should complete within 60s")
assertions.assert_output_contains(result, "stdout", "Should have stdout in output")

# Generate execution report
exec_report = ExecutionReport(
    flow_name=result.flow_name,
    execution_id=result.execution_id,
    status=result.status,
    start_time=start_time,
    end_time=end_time,
    duration=result.duration,
    input_variables={"param": "value"},
    output=result.output,
    error=result.error
)

exec_report_path = reporter.generate_execution_report(
    exec_report,
    format=ReportFormat.HTML
)
print(f"✓ Execution report: {exec_report_path}")

# Test 3: Complete assertions suite
assertions.complete()
suite = assertions.get_suite()

print("\n" + "="*60)
print(suite.summary())
print("="*60)

# Check if all tests passed
if suite.passed:
    print("\n✓ All tests passed!")
else:
    print("\n✗ Some tests failed:")
    for failure in suite.get_failures():
        print(f"  - {failure}")

# Exit with appropriate code
exit(0 if suite.passed else 1)
```

**Output**:
```
1. Validating flow...
✓ Validation report: reports/validation_MyFlow_20260211_103000.html

2. Executing flow...
✓ Execution report: reports/execution_MyFlow_20260211_103005.html

============================================================
Assertion Suite: MyFlow Test Suite
Total Assertions: 4
Passed: 4
Failed: 0
Success Rate: 100.0%
Status: ✓ PASSED
============================================================

✓ All tests passed!
```

---

## 📊 Report Formats Comparison

| Format | Use Case | Features |
|--------|----------|----------|
| **HTML** | Viewing in browser | Beautiful, interactive, charts |
| **JSON** | API/automation | Machine-readable, structured |
| **Markdown** | Documentation | Readable, version-controllable |
| **CSV** | Excel/analysis | Tabular data, spreadsheets |
| **Text** | Console/logs | Simple, console-friendly |

---

## 🎨 Assertion Severity Levels

```python
from pad_framework.testing.assertions import AssertionSeverity

# Critical - Must pass
assertions.assert_true(
    condition,
    "Critical check",
    severity=AssertionSeverity.CRITICAL
)

# Error - Test failure
assertions.assert_equal(
    actual, expected,
    "Important check",
    severity=AssertionSeverity.ERROR
)

# Warning - Non-critical issue
assertions.assert_not_empty(
    collection,
    "Should have data",
    severity=AssertionSeverity.WARNING
)

# Info - Informational
assertions.assert_type(
    value, str,
    "Type information",
    severity=AssertionSeverity.INFO
)
```

---

## 🔧 Advanced Features

### Custom Assertions

```python
# Define custom validation logic
def custom_check():
    # Your logic here
    return True

assertions.assert_custom(
    condition=custom_check,
    name="custom_validation",
    message="Custom check should pass",
    severity=AssertionSeverity.ERROR
)
```

### Assertion Filtering

```python
# Get only failures
failures = suite.get_failures()

# Get by severity
criticals = suite.get_by_severity(AssertionSeverity.CRITICAL)
errors = suite.get_by_severity(AssertionSeverity.ERROR)
warnings = suite.get_by_severity(AssertionSeverity.WARNING)
```

### Report Customization

```python
# Generate multiple formats
for format in [ReportFormat.HTML, ReportFormat.JSON, ReportFormat.MARKDOWN]:
    report_path = generator.generate_execution_report(
        exec_report,
        format=format
    )
    print(f"{format.value} report: {report_path}")
```

---

## 📋 Best Practices

### 1. **Use Meaningful Names**

```python
# ✅ Good
assertions = Assertions(suite_name="User Authentication Tests")

# ❌ Bad
assertions = Assertions(suite_name="Test1")
```

### 2. **Use Appropriate Severity**

```python
# Critical for must-pass checks
assertions.assert_true(
    user_authenticated,
    "User must be authenticated",
    severity=AssertionSeverity.CRITICAL
)

# Warning for nice-to-have
assertions.assert_not_empty(
    user_preferences,
    "User should have preferences",
    severity=AssertionSeverity.WARNING
)
```

### 3. **Generate Reports After Tests**

```python
# Always generate reports
suite = assertions.complete()

if not suite.passed:
    # Generate detailed report on failure
    report_path = generator.generate_validation_report(...)
    print(f"See report: {report_path}")
```

### 4. **Check Assertions Suite**

```python
# Always check suite results
suite = assertions.get_suite()

if suite.passed:
    print("✓ All tests passed")
else:
    print(f"✗ {suite.failed_assertions} tests failed")
    sys.exit(1)
```

---

## 🎯 Integration with CI/CD

```python
#!/usr/bin/env python
"""
CI/CD Test Script with Reporting
"""

from pad_framework import PADFramework
from pad_framework.testing.assertions import Assertions
from pad_framework.reporting import ReportGenerator, ReportFormat
import sys

def run_tests():
    pad = PADFramework()
    assertions = Assertions(suite_name="CI Tests")
    reporter = ReportGenerator(output_dir="test-reports")
    
    # Run tests
    result = pad.execute_flow("ProductionFlow", {})
    
    # Assertions
    assertions.assert_flow_success(result)
    assertions.assert_duration_within(result, 120)
    assertions.assert_no_error(result)
    
    # Complete suite
    suite = assertions.complete()
    
    # Generate reports
    # (Report generation code here)
    
    # Return exit code
    return 0 if suite.passed else 1

if __name__ == "__main__":
    sys.exit(run_tests())
```

---

## 📚 API Reference

### ReportGenerator

```python
generator = ReportGenerator(output_dir="reports")

# Execution report
generator.generate_execution_report(data, format=ReportFormat.HTML)

# Validation report
generator.generate_validation_report(data, format=ReportFormat.JSON)

# Performance report
generator.generate_performance_report(data, format=ReportFormat.MARKDOWN)

# Summary report
generator.generate_summary_report(data, format=ReportFormat.TEXT)
```

### Assertions

```python
assertions = Assertions(suite_name="My Tests")

# Basic
assertions.assert_true(condition, message)
assertions.assert_equal(actual, expected, message)

# Comparison
assertions.assert_greater(actual, threshold, message)
assertions.assert_in_range(value, min, max, message)

# Collections
assertions.assert_contains(collection, item, message)
assertions.assert_length(collection, expected_length, message)

# Flow-specific
assertions.assert_flow_success(result, message)
assertions.assert_duration_within(result, max_duration, message)

# Suite management
suite = assertions.get_suite()
assertions.complete()
```

---

## ✅ Summary

### Reporting Capabilities ✅
- ✅ Multiple report formats (HTML, JSON, MD, CSV, Text)
- ✅ 4 report types (Execution, Validation, Performance, Summary)
- ✅ Professional templates
- ✅ Automated generation
- ✅ Customizable output

### Assertion Capabilities ✅
- ✅ 20+ assertion types
- ✅ Flow-specific assertions
- ✅ Severity levels
- ✅ Suite management
- ✅ Detailed results

**Status**: ✅ Fully Implemented and Production-Ready!

---

**Version**: 1.1.0  
**Last Updated**: February 11, 2026  
**Documentation**: Complete ✅
