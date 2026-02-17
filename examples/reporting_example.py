"""
Reporting Examples
Demonstrates report generation capabilities
"""

from pad_framework import PADFramework
from pad_framework.reporting import (
    ReportGenerator,
    ExecutionReport,
    ValidationReport,
    PerformanceReport,
    ReportFormat
)
from datetime import datetime, timedelta


def example_execution_report():
    """Generate execution report"""
    print("="*60)
    print("EXAMPLE: Execution Report")
    print("="*60)
    
    # Create report data
    report_data = ExecutionReport(
        flow_name="DataProcessor",
        execution_id="exec-123-456",
        status="success",
        start_time=datetime.now() - timedelta(seconds=45),
        end_time=datetime.now(),
        duration=45.5,
        input_variables={
            "file": "data/input.csv",
            "output_folder": "data/output/",
            "options": {"validate": True}
        },
        output={
            "records_processed": 1250,
            "output_file": "data/output/processed.csv",
            "validation_passed": True
        },
        retry_attempts=0,
        warnings=[]
    )
    
    # Generate reports in different formats
    generator = ReportGenerator(output_dir="reports")
    
    formats = [ReportFormat.HTML, ReportFormat.JSON, ReportFormat.MARKDOWN, ReportFormat.TEXT]
    
    for format in formats:
        report_path = generator.generate_execution_report(report_data, format=format)
        print(f"✓ {format.value.upper():10} report: {report_path}")
    
    print()


def example_validation_report():
    """Generate validation report"""
    print("="*60)
    print("EXAMPLE: Validation Report")
    print("="*60)
    
    # Create validation data
    validation_data = ValidationReport(
        flow_name="EmailSender",
        timestamp=datetime.now(),
        valid=True,
        errors=[],
        warnings=["Flow has no description", "Missing timeout configuration"],
        info=["Flow validation completed", "All required fields present"],
        checks_performed=15,
        checks_passed=13,
        checks_failed=0
    )
    
    # Generate report
    generator = ReportGenerator(output_dir="reports")
    report_path = generator.generate_validation_report(
        validation_data,
        format=ReportFormat.HTML
    )
    
    print(f"✓ Validation report: {report_path}")
    print(f"  Success Rate: {validation_data.success_rate:.1f}%")
    print(f"  Checks: {validation_data.checks_passed}/{validation_data.checks_performed} passed")
    print()


def example_performance_report():
    """Generate performance report"""
    print("="*60)
    print("EXAMPLE: Performance Report")
    print("="*60)
    
    # Create performance data
    perf_data = PerformanceReport(
        flow_name="DataProcessor",
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
    
    # Generate report
    generator = ReportGenerator(output_dir="reports")
    report_path = generator.generate_performance_report(
        perf_data,
        format=ReportFormat.HTML
    )
    
    print(f"✓ Performance report: {report_path}")
    print(f"  Success Rate: {perf_data.success_rate:.1f}%")
    print(f"  Avg Duration: {perf_data.avg_duration:.2f}s")
    print(f"  Total Executions: {perf_data.total_executions}")
    print()


def example_summary_report():
    """Generate summary report for multiple flows"""
    print("="*60)
    print("EXAMPLE: Summary Report")
    print("="*60)
    
    # Create summary data
    flows_data = [
        {
            "name": "DataProcessor",
            "executions": 100,
            "success_rate": 95.0,
            "avg_duration": 12.5,
            "last_execution": "2026-02-11 10:30:00"
        },
        {
            "name": "EmailSender",
            "executions": 50,
            "success_rate": 98.0,
            "avg_duration": 3.2,
            "last_execution": "2026-02-11 09:15:00"
        },
        {
            "name": "BackupFlow",
            "executions": 25,
            "success_rate": 100.0,
            "avg_duration": 120.5,
            "last_execution": "2026-02-11 02:00:00"
        }
    ]
    
    # Generate report
    generator = ReportGenerator(output_dir="reports")
    report_path = generator.generate_summary_report(
        flows_data,
        format=ReportFormat.HTML
    )
    
    print(f"✓ Summary report: {report_path}")
    print(f"  Total Flows: {len(flows_data)}")
    avg_success = sum(f["success_rate"] for f in flows_data) / len(flows_data)
    print(f"  Avg Success Rate: {avg_success:.1f}%")
    print()


def example_all_formats():
    """Generate report in all formats"""
    print("="*60)
    print("EXAMPLE: All Report Formats")
    print("="*60)
    
    exec_report = ExecutionReport(
        flow_name="TestFlow",
        execution_id="test-123",
        status="success",
        start_time=datetime.now(),
        end_time=datetime.now(),
        duration=10.5,
        input_variables={"test": True},
        output={"result": "ok"}
    )
    
    generator = ReportGenerator(output_dir="reports")
    
    formats = {
        ReportFormat.HTML: "Beautiful browser view",
        ReportFormat.JSON: "Machine-readable data",
        ReportFormat.MARKDOWN: "Documentation format",
        ReportFormat.TEXT: "Console-friendly"
    }
    
    for format, description in formats.items():
        report_path = generator.generate_execution_report(exec_report, format=format)
        print(f"✓ {format.value.upper():8} ({description:25}): {report_path}")
    
    print()


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("REPORTING EXAMPLES")
    print("="*60)
    print()
    
    try:
        example_execution_report()
        example_validation_report()
        example_performance_report()
        example_summary_report()
        example_all_formats()
        
        print("="*60)
        print("✓ All reports generated successfully!")
        print("="*60)
        print("\nCheck the 'reports/' folder to view generated reports.")
        print()
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
