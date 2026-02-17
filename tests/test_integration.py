"""
Integration Tests for Reporting and Assertions
Tests the complete workflow together
"""

import pytest
import os
from datetime import datetime
from pathlib import Path

from pad_framework.testing.assertions import Assertions, AssertionSeverity
from pad_framework.reporting import (
    ReportGenerator,
    ExecutionReport,
    ValidationReport,
    ReportFormat
)


class TestIntegration:
    """Integration tests for reporting and assertions"""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create temporary directory for reports"""
        return tmp_path / "integration_reports"
    
    def test_complete_workflow(self, temp_dir):
        """Test complete workflow: assertions + reporting"""
        # 1. Initialize components
        assertions = Assertions(suite_name="Integration Test")
        reporter = ReportGenerator(output_dir=str(temp_dir))
        
        # 2. Perform assertions
        assertions.assert_true(True, "Basic check")
        assertions.assert_equal(10, 10, "Equality check")
        assertions.assert_greater(20, 10, "Comparison check")
        
        # 3. Complete assertions
        suite = assertions.complete()
        
        # 4. Create validation report from assertions
        validation_report = ValidationReport(
            flow_name="IntegrationTest",
            timestamp=datetime.now(),
            valid=suite.passed,
            errors=[str(f) for f in suite.get_failures()],
            warnings=[],
            info=["Integration test completed"],
            checks_performed=suite.total_assertions,
            checks_passed=suite.passed_assertions,
            checks_failed=suite.failed_assertions
        )
        
        # 5. Generate report
        report_path = reporter.generate_validation_report(
            validation_report,
            format=ReportFormat.HTML
        )
        
        # 6. Verify everything worked
        assert suite.passed is True
        assert suite.total_assertions == 3
        assert os.path.exists(report_path)
        
        # Verify report content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "IntegrationTest" in content
            assert "100.0" in content  # Success rate
    
    def test_failed_assertions_reporting(self, temp_dir):
        """Test reporting failed assertions"""
        # Create failing assertions
        assertions = Assertions(suite_name="Failure Test")
        
        assertions.assert_true(False, "This will fail")
        assertions.assert_equal(10, 20, "This will also fail")
        assertions.assert_true(True, "This will pass")
        
        suite = assertions.complete()
        
        # Create report
        reporter = ReportGenerator(output_dir=str(temp_dir))
        validation_report = ValidationReport(
            flow_name="FailureTest",
            timestamp=datetime.now(),
            valid=suite.passed,
            errors=[str(f) for f in suite.get_failures()],
            warnings=[],
            info=[],
            checks_performed=suite.total_assertions,
            checks_passed=suite.passed_assertions,
            checks_failed=suite.failed_assertions
        )
        
        report_path = reporter.generate_validation_report(
            validation_report,
            format=ReportFormat.HTML
        )
        
        # Verify
        assert suite.passed is False
        assert suite.failed_assertions == 2
        assert os.path.exists(report_path)
        
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "FAILED" in content
            assert "This will fail" in content
    
    def test_multiple_report_formats(self, temp_dir):
        """Test generating multiple report formats"""
        # Create assertions
        assertions = Assertions(suite_name="Multi-Format Test")
        assertions.assert_true(True, "Test")
        assertions.assert_equal(5, 5, "Test")
        
        suite = assertions.complete()
        
        # Create report
        reporter = ReportGenerator(output_dir=str(temp_dir))
        exec_report = ExecutionReport(
            flow_name="MultiFormatTest",
            execution_id="test-123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={},
            output={}
        )
        
        # Generate in all formats
        formats = [
            ReportFormat.HTML,
            ReportFormat.JSON,
            ReportFormat.MARKDOWN,
            ReportFormat.TEXT
        ]
        
        paths = []
        for format in formats:
            path = reporter.generate_execution_report(exec_report, format=format)
            paths.append(path)
            assert os.path.exists(path)
        
        # Verify all paths are different
        assert len(set(paths)) == len(paths)
    
    def test_severity_levels_reporting(self, temp_dir):
        """Test different severity levels in reporting"""
        assertions = Assertions(suite_name="Severity Test")
        
        # Different severities
        assertions.assert_true(
            True,
            "Critical check",
            severity=AssertionSeverity.CRITICAL
        )
        assertions.assert_true(
            True,
            "Error check",
            severity=AssertionSeverity.ERROR
        )
        assertions.assert_true(
            True,
            "Warning check",
            severity=AssertionSeverity.WARNING
        )
        assertions.assert_true(
            True,
            "Info check",
            severity=AssertionSeverity.INFO
        )
        
        suite = assertions.complete()
        
        # Verify severity distribution
        criticals = suite.get_by_severity(AssertionSeverity.CRITICAL)
        errors = suite.get_by_severity(AssertionSeverity.ERROR)
        warnings = suite.get_by_severity(AssertionSeverity.WARNING)
        infos = suite.get_by_severity(AssertionSeverity.INFO)
        
        assert len(criticals) == 1
        assert len(errors) == 1
        assert len(warnings) == 1
        assert len(infos) == 1
    
    def test_large_scale_assertions(self, temp_dir):
        """Test handling large number of assertions"""
        assertions = Assertions(suite_name="Large Scale Test")
        
        # Create many assertions
        for i in range(100):
            assertions.assert_true(True, f"Test {i}")
        
        suite = assertions.complete()
        
        # Verify
        assert suite.total_assertions == 100
        assert suite.passed_assertions == 100
        assert suite.success_rate == 100.0
        
        # Generate report
        reporter = ReportGenerator(output_dir=str(temp_dir))
        validation_report = ValidationReport(
            flow_name="LargeScaleTest",
            timestamp=datetime.now(),
            valid=suite.passed,
            errors=[],
            warnings=[],
            info=[f"Performed {suite.total_assertions} checks"],
            checks_performed=suite.total_assertions,
            checks_passed=suite.passed_assertions,
            checks_failed=suite.failed_assertions
        )
        
        report_path = reporter.generate_validation_report(
            validation_report,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(report_path)
    
    def test_nested_data_in_reports(self, temp_dir):
        """Test complex nested data in reports"""
        reporter = ReportGenerator(output_dir=str(temp_dir))
        
        # Complex nested data
        exec_report = ExecutionReport(
            flow_name="NestedDataTest",
            execution_id="test-456",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=15.5,
            input_variables={
                "config": {
                    "settings": {
                        "level1": {
                            "level2": {
                                "value": 123
                            }
                        }
                    }
                },
                "list_data": [1, 2, 3, [4, 5, 6]]
            },
            output={
                "results": [
                    {"id": 1, "status": "ok"},
                    {"id": 2, "status": "ok"}
                ]
            }
        )
        
        # Generate JSON (best for nested data)
        json_path = reporter.generate_execution_report(
            exec_report,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(json_path)
        
        # Verify JSON is valid and contains data
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['input_variables']['config']['settings']['level1']['level2']['value'] == 123
            assert len(data['output']['results']) == 2


class TestErrorHandling:
    """Test error handling in integration scenarios"""
    
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path / "error_tests"
    
    def test_invalid_directory_handling(self):
        """Test handling of invalid directory"""
        # Should create directory if it doesn't exist
        reporter = ReportGenerator(output_dir="/tmp/new_test_dir_12345")
        assert os.path.exists("/tmp/new_test_dir_12345")
        
        # Cleanup
        os.rmdir("/tmp/new_test_dir_12345")
    
    def test_assertions_with_none_values(self):
        """Test assertions handle None values correctly"""
        assertions = Assertions(suite_name="None Test")
        
        assertions.assert_is_none(None, "Should handle None")
        assertions.assert_is_not_none("value", "Should handle value")
        
        suite = assertions.complete()
        assert suite.passed is True
    
    def test_empty_collections(self):
        """Test assertions with empty collections"""
        assertions = Assertions(suite_name="Empty Test")
        
        assertions.assert_empty([], "Empty list")
        assertions.assert_empty({}, "Empty dict")
        assertions.assert_empty("", "Empty string")
        
        suite = assertions.complete()
        assert suite.passed is True


class TestPerformance:
    """Test performance of reporting and assertions"""
    
    def test_assertion_performance(self):
        """Test assertion performance with many checks"""
        import time
        
        assertions = Assertions(suite_name="Performance Test")
        
        start_time = time.time()
        
        # Perform 1000 assertions
        for i in range(1000):
            assertions.assert_equal(i, i, f"Check {i}")
        
        elapsed = time.time() - start_time
        
        suite = assertions.complete()
        
        # Should complete quickly
        assert elapsed < 5.0  # 5 seconds max
        assert suite.total_assertions == 1000
        assert suite.passed is True
    
    def test_report_generation_performance(self, tmp_path):
        """Test report generation performance"""
        import time
        
        reporter = ReportGenerator(output_dir=str(tmp_path))
        
        # Create large execution report
        exec_report = ExecutionReport(
            flow_name="PerformanceTest",
            execution_id="perf-123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=100.0,
            input_variables={f"param{i}": f"value{i}" for i in range(100)},
            output={f"result{i}": i for i in range(100)}
        )
        
        start_time = time.time()
        
        # Generate report
        path = reporter.generate_execution_report(
            exec_report,
            format=ReportFormat.HTML
        )
        
        elapsed = time.time() - start_time
        
        # Should generate quickly
        assert elapsed < 2.0  # 2 seconds max
        assert os.path.exists(path)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
