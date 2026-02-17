"""
Comprehensive Tests for Reporting System
Tests all report formats, types, and edge cases
"""

import pytest
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

from pad_framework.reporting import (
    ReportGenerator,
    ReportFormat,
    ReportType,
    ExecutionReport,
    ValidationReport,
    PerformanceReport
)


class TestReportGenerator:
    """Test ReportGenerator class"""
    
    @pytest.fixture
    def generator(self, tmp_path):
        """Create report generator with temp directory"""
        return ReportGenerator(output_dir=str(tmp_path))
    
    @pytest.fixture
    def execution_report(self):
        """Create sample execution report"""
        return ExecutionReport(
            flow_name="TestFlow",
            execution_id="test-123",
            status="success",
            start_time=datetime.now() - timedelta(seconds=45),
            end_time=datetime.now(),
            duration=45.5,
            input_variables={"param1": "value1", "param2": 123},
            output={"result": "success", "data": [1, 2, 3]},
            error=None,
            retry_attempts=0,
            warnings=[]
        )
    
    @pytest.fixture
    def validation_report(self):
        """Create sample validation report"""
        return ValidationReport(
            flow_name="TestFlow",
            timestamp=datetime.now(),
            valid=True,
            errors=[],
            warnings=["Minor warning"],
            info=["Validation completed"],
            checks_performed=10,
            checks_passed=9,
            checks_failed=1
        )
    
    @pytest.fixture
    def performance_report(self):
        """Create sample performance report"""
        return PerformanceReport(
            flow_name="TestFlow",
            period_start=datetime.now() - timedelta(days=7),
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
    
    # Test Execution Reports
    
    def test_execution_report_html(self, generator, execution_report):
        """Test HTML execution report generation"""
        path = generator.generate_execution_report(
            execution_report,
            format=ReportFormat.HTML
        )
        
        assert os.path.exists(path)
        assert path.endswith('.html')
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "TestFlow" in content
            assert "success" in content
            assert "45.5" in content
            assert "<!DOCTYPE html>" in content
    
    def test_execution_report_json(self, generator, execution_report):
        """Test JSON execution report generation"""
        path = generator.generate_execution_report(
            execution_report,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(path)
        assert path.endswith('.json')
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['flow_name'] == "TestFlow"
            assert data['status'] == "success"
            assert data['duration'] == 45.5
    
    def test_execution_report_markdown(self, generator, execution_report):
        """Test Markdown execution report generation"""
        path = generator.generate_execution_report(
            execution_report,
            format=ReportFormat.MARKDOWN
        )
        
        assert os.path.exists(path)
        assert path.endswith('.md')
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "# Flow Execution Report" in content
            assert "TestFlow" in content
            assert "success" in content
    
    def test_execution_report_text(self, generator, execution_report):
        """Test text execution report generation"""
        path = generator.generate_execution_report(
            execution_report,
            format=ReportFormat.TEXT
        )
        
        assert os.path.exists(path)
        assert path.endswith('.txt')
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "FLOW EXECUTION REPORT" in content
            assert "TestFlow" in content
    
    # Test Validation Reports
    
    def test_validation_report_html(self, generator, validation_report):
        """Test HTML validation report generation"""
        path = generator.generate_validation_report(
            validation_report,
            format=ReportFormat.HTML
        )
        
        assert os.path.exists(path)
        assert path.endswith('.html')
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "TestFlow" in content
            assert "90.0" in content  # Success rate
            assert "Minor warning" in content
    
    def test_validation_report_json(self, generator, validation_report):
        """Test JSON validation report generation"""
        path = generator.generate_validation_report(
            validation_report,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['flow_name'] == "TestFlow"
            assert data['valid'] is True
            assert data['checks_performed'] == 10
    
    def test_validation_report_markdown(self, generator, validation_report):
        """Test Markdown validation report generation"""
        path = generator.generate_validation_report(
            validation_report,
            format=ReportFormat.MARKDOWN
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "# Flow Validation Report" in content
            assert "✅ PASSED" in content
    
    # Test Performance Reports
    
    def test_performance_report_html(self, generator, performance_report):
        """Test HTML performance report generation"""
        path = generator.generate_performance_report(
            performance_report,
            format=ReportFormat.HTML
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "TestFlow" in content
            assert "95.0" in content  # Success rate
            assert "12.5" in content  # Avg duration
    
    def test_performance_report_json(self, generator, performance_report):
        """Test JSON performance report generation"""
        path = generator.generate_performance_report(
            performance_report,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data['flow_name'] == "TestFlow"
            assert data['total_executions'] == 100
            assert data['avg_duration'] == 12.5
    
    # Test Summary Reports
    
    def test_summary_report_html(self, generator):
        """Test HTML summary report generation"""
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
        
        path = generator.generate_summary_report(
            flows_data,
            format=ReportFormat.HTML
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Flow1" in content
            assert "Flow2" in content
            assert "Total Flows: 2" in content
    
    def test_summary_report_json(self, generator):
        """Test JSON summary report generation"""
        flows_data = [{"name": "Flow1", "executions": 100}]
        
        path = generator.generate_summary_report(
            flows_data,
            format=ReportFormat.JSON
        )
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]['name'] == "Flow1"
    
    # Test Edge Cases
    
    def test_execution_report_with_error(self, generator):
        """Test execution report with error"""
        report = ExecutionReport(
            flow_name="FailedFlow",
            execution_id="fail-123",
            status="failed",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={},
            output={},
            error="Something went wrong",
            retry_attempts=3,
            warnings=["Warning 1", "Warning 2"]
        )
        
        path = generator.generate_execution_report(report, ReportFormat.HTML)
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "failed" in content
            assert "Something went wrong" in content
            assert "Warning 1" in content
    
    def test_validation_report_failed(self, generator):
        """Test validation report with failures"""
        report = ValidationReport(
            flow_name="InvalidFlow",
            timestamp=datetime.now(),
            valid=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            info=[],
            checks_performed=10,
            checks_passed=7,
            checks_failed=3
        )
        
        path = generator.generate_validation_report(report, ReportFormat.HTML)
        
        assert os.path.exists(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "FAILED" in content
            assert "Error 1" in content
            assert "Error 2" in content
    
    def test_invalid_format(self, generator, execution_report):
        """Test invalid report format"""
        with pytest.raises(ValueError):
            generator.generate_execution_report(
                execution_report,
                format="invalid"
            )
    
    def test_output_directory_creation(self, tmp_path):
        """Test output directory is created if it doesn't exist"""
        report_dir = tmp_path / "new_reports"
        generator = ReportGenerator(output_dir=str(report_dir))
        
        assert report_dir.exists()
    
    def test_multiple_reports_same_flow(self, generator, execution_report):
        """Test generating multiple reports for same flow"""
        path1 = generator.generate_execution_report(execution_report, ReportFormat.HTML)
        path2 = generator.generate_execution_report(execution_report, ReportFormat.HTML)
        
        # Different filenames (timestamps differ)
        assert path1 != path2
        assert os.path.exists(path1)
        assert os.path.exists(path2)


class TestReportDataClasses:
    """Test report data classes"""
    
    def test_execution_report_creation(self):
        """Test ExecutionReport creation"""
        report = ExecutionReport(
            flow_name="Test",
            execution_id="123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={},
            output={}
        )
        
        assert report.flow_name == "Test"
        assert report.status == "success"
        assert report.warnings == []  # Default value
    
    def test_validation_report_success_rate(self):
        """Test ValidationReport success rate calculation"""
        report = ValidationReport(
            flow_name="Test",
            timestamp=datetime.now(),
            valid=True,
            errors=[],
            warnings=[],
            info=[],
            checks_performed=10,
            checks_passed=8,
            checks_failed=2
        )
        
        assert report.success_rate == 80.0
    
    def test_validation_report_success_rate_zero_checks(self):
        """Test ValidationReport success rate with zero checks"""
        report = ValidationReport(
            flow_name="Test",
            timestamp=datetime.now(),
            valid=True,
            errors=[],
            warnings=[],
            info=[],
            checks_performed=0,
            checks_passed=0,
            checks_failed=0
        )
        
        assert report.success_rate == 0.0
    
    def test_performance_report_success_rate(self):
        """Test PerformanceReport success rate calculation"""
        report = PerformanceReport(
            flow_name="Test",
            period_start=datetime.now(),
            period_end=datetime.now(),
            total_executions=100,
            successful_executions=95,
            failed_executions=5,
            avg_duration=10.0,
            min_duration=5.0,
            max_duration=20.0,
            p50_duration=10.0,
            p95_duration=18.0,
            p99_duration=19.5,
            avg_memory_mb=100.0,
            max_memory_mb=200.0,
            avg_cpu_percent=50.0,
            error_rate=5.0
        )
        
        assert report.success_rate == 95.0
    
    def test_performance_report_success_rate_zero_executions(self):
        """Test PerformanceReport success rate with zero executions"""
        report = PerformanceReport(
            flow_name="Test",
            period_start=datetime.now(),
            period_end=datetime.now(),
            total_executions=0,
            successful_executions=0,
            failed_executions=0,
            avg_duration=0.0,
            min_duration=0.0,
            max_duration=0.0,
            p50_duration=0.0,
            p95_duration=0.0,
            p99_duration=0.0,
            avg_memory_mb=0.0,
            max_memory_mb=0.0,
            avg_cpu_percent=0.0,
            error_rate=0.0
        )
        
        assert report.success_rate == 0.0


class TestReportContent:
    """Test report content quality"""
    
    @pytest.fixture
    def generator(self, tmp_path):
        return ReportGenerator(output_dir=str(tmp_path))
    
    def test_html_report_has_css(self, generator):
        """Test HTML reports contain CSS styling"""
        report = ExecutionReport(
            flow_name="Test",
            execution_id="123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={},
            output={}
        )
        
        path = generator.generate_execution_report(report, ReportFormat.HTML)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "<style>" in content
            assert "font-family" in content
            assert "table" in content
    
    def test_markdown_report_has_proper_formatting(self, generator):
        """Test Markdown reports have proper formatting"""
        report = ExecutionReport(
            flow_name="Test",
            execution_id="123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={},
            output={}
        )
        
        path = generator.generate_execution_report(report, ReportFormat.MARKDOWN)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content.startswith("#")  # Header
            assert "|" in content  # Table
            assert "```" in content  # Code block
    
    def test_json_report_is_valid_json(self, generator):
        """Test JSON reports are valid JSON"""
        report = ExecutionReport(
            flow_name="Test",
            execution_id="123",
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            input_variables={"key": "value"},
            output={"result": 123}
        )
        
        path = generator.generate_execution_report(report, ReportFormat.JSON)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Should not raise
            assert isinstance(data, dict)
            assert "flow_name" in data
            assert "input_variables" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
