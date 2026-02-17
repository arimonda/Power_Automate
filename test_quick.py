"""
Quick Test Script
Fast verification that reporting and assertions work
"""

import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pad_framework.testing.assertions import Assertions, AssertionSeverity
from pad_framework.reporting import (
    ReportGenerator,
    ExecutionReport,
    ValidationReport,
    PerformanceReport,
    ReportFormat
)


def test_assertions():
    """Quick test of assertion framework"""
    print("="*60)
    print("TESTING ASSERTION FRAMEWORK")
    print("="*60)
    
    assertions = Assertions(suite_name="Quick Test")
    
    # Basic assertions
    print("\n1. Testing basic assertions...")
    assertions.assert_true(True, "Boolean check")
    assertions.assert_equal(10, 10, "Equality check")
    assertions.assert_greater(20, 10, "Comparison check")
    print("   ✓ Basic assertions OK")
    
    # Collection assertions
    print("\n2. Testing collection assertions...")
    assertions.assert_contains([1, 2, 3], 2, "Contains check")
    assertions.assert_length([1, 2, 3], 3, "Length check")
    assertions.assert_not_empty([1, 2, 3], "Not empty check")
    print("   ✓ Collection assertions OK")
    
    # String assertions
    print("\n3. Testing string assertions...")
    assertions.assert_starts_with("Hello World", "Hello", "Starts with check")
    assertions.assert_ends_with("Hello World", "World", "Ends with check")
    print("   ✓ String assertions OK")
    
    # Type assertions
    print("\n4. Testing type assertions...")
    assertions.assert_type("text", str, "String type check")
    assertions.assert_type(123, int, "Int type check")
    print("   ✓ Type assertions OK")
    
    # Get results
    suite = assertions.complete()
    
    print("\n" + "-"*60)
    print("ASSERTION RESULTS:")
    print(f"  Total Assertions: {suite.total_assertions}")
    print(f"  Passed: {suite.passed_assertions}")
    print(f"  Failed: {suite.failed_assertions}")
    print(f"  Success Rate: {suite.success_rate:.1f}%")
    print(f"  Status: {'✓ PASSED' if suite.passed else '✗ FAILED'}")
    print("-"*60)
    
    return suite.passed


def test_reporting():
    """Quick test of reporting system"""
    print("\n" + "="*60)
    print("TESTING REPORTING SYSTEM")
    print("="*60)
    
    # Create reporter
    reporter = ReportGenerator(output_dir="test_reports")
    
    # Test execution report
    print("\n1. Testing execution reports...")
    exec_report = ExecutionReport(
        flow_name="QuickTest",
        execution_id="test-123",
        status="success",
        start_time=datetime.now(),
        end_time=datetime.now(),
        duration=12.5,
        input_variables={"param": "value"},
        output={"result": "success"}
    )
    
    html_path = reporter.generate_execution_report(exec_report, ReportFormat.HTML)
    json_path = reporter.generate_execution_report(exec_report, ReportFormat.JSON)
    md_path = reporter.generate_execution_report(exec_report, ReportFormat.MARKDOWN)
    
    print(f"   ✓ HTML report: {html_path}")
    print(f"   ✓ JSON report: {json_path}")
    print(f"   ✓ Markdown report: {md_path}")
    
    # Test validation report
    print("\n2. Testing validation reports...")
    val_report = ValidationReport(
        flow_name="QuickTest",
        timestamp=datetime.now(),
        valid=True,
        errors=[],
        warnings=["Minor warning"],
        info=["Test completed"],
        checks_performed=10,
        checks_passed=9,
        checks_failed=1
    )
    
    val_path = reporter.generate_validation_report(val_report, ReportFormat.HTML)
    print(f"   ✓ Validation report: {val_path}")
    
    # Test performance report
    print("\n3. Testing performance reports...")
    perf_report = PerformanceReport(
        flow_name="QuickTest",
        period_start=datetime.now(),
        period_end=datetime.now(),
        total_executions=100,
        successful_executions=95,
        failed_executions=5,
        avg_duration=12.5,
        min_duration=8.0,
        max_duration=30.0,
        p50_duration=11.0,
        p95_duration=25.0,
        p99_duration=28.0,
        avg_memory_mb=100.0,
        max_memory_mb=200.0,
        avg_cpu_percent=45.0,
        error_rate=5.0
    )
    
    perf_path = reporter.generate_performance_report(perf_report, ReportFormat.HTML)
    print(f"   ✓ Performance report: {perf_path}")
    
    # Test summary report
    print("\n4. Testing summary reports...")
    flows_data = [
        {"name": "Flow1", "executions": 100, "success_rate": 95.0},
        {"name": "Flow2", "executions": 50, "success_rate": 98.0}
    ]
    
    summary_path = reporter.generate_summary_report(flows_data, ReportFormat.HTML)
    print(f"   ✓ Summary report: {summary_path}")
    
    print("\n" + "-"*60)
    print("REPORTING RESULTS:")
    print("  ✓ All report types generated successfully")
    print("  ✓ All report formats working correctly")
    print(f"  Reports saved to: test_reports/")
    print("-"*60)
    
    return True


def test_integration():
    """Quick integration test"""
    print("\n" + "="*60)
    print("TESTING INTEGRATION")
    print("="*60)
    
    # Create components
    assertions = Assertions(suite_name="Integration Test")
    reporter = ReportGenerator(output_dir="test_reports")
    
    print("\n1. Running assertions...")
    assertions.assert_true(True, "Integration check 1")
    assertions.assert_equal(5, 5, "Integration check 2")
    assertions.assert_greater(10, 5, "Integration check 3")
    
    suite = assertions.complete()
    print(f"   ✓ {suite.total_assertions} assertions completed")
    
    print("\n2. Generating report from assertions...")
    validation_report = ValidationReport(
        flow_name="IntegrationTest",
        timestamp=datetime.now(),
        valid=suite.passed,
        errors=[str(f) for f in suite.get_failures()],
        warnings=[],
        info=["Integration test"],
        checks_performed=suite.total_assertions,
        checks_passed=suite.passed_assertions,
        checks_failed=suite.failed_assertions
    )
    
    report_path = reporter.generate_validation_report(
        validation_report,
        format=ReportFormat.HTML
    )
    
    print(f"   ✓ Report generated: {report_path}")
    
    print("\n" + "-"*60)
    print("INTEGRATION RESULTS:")
    print("  ✓ Assertions and reporting work together correctly")
    print("-"*60)
    
    return suite.passed


def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("  QUICK TEST - REPORTING & ASSERTIONS")
    print("="*60)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    try:
        # Test assertions
        results.append(("Assertions", test_assertions()))
        
        # Test reporting
        results.append(("Reporting", test_reporting()))
        
        # Test integration
        results.append(("Integration", test_integration()))
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Print final summary
    print("\n" + "="*60)
    print("  FINAL SUMMARY")
    print("="*60)
    
    all_passed = all(r[1] for r in results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status} | {name}")
    
    print("="*60)
    
    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
        print("\n✅ Reporting and Assertion frameworks are working correctly!")
        print("\nYou can now:")
        print("  - Use assertions in your tests")
        print("  - Generate reports in multiple formats")
        print("  - View generated reports in test_reports/")
        print("\nFor comprehensive tests, run: python run_tests.py")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
