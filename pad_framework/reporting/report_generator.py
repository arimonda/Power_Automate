"""
Report Generator
Comprehensive reporting system for flow executions, performance, and validation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json
from dataclasses import dataclass, asdict
from enum import Enum


class ReportFormat(str, Enum):
    """Supported report formats"""
    HTML = "html"
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "md"
    PDF = "pdf"
    TEXT = "txt"


class ReportType(str, Enum):
    """Types of reports"""
    EXECUTION = "execution"
    PERFORMANCE = "performance"
    VALIDATION = "validation"
    SUMMARY = "summary"
    DETAILED = "detailed"
    AUDIT = "audit"


@dataclass
class ExecutionReport:
    """Execution report data"""
    flow_name: str
    execution_id: str
    status: str
    start_time: datetime
    end_time: datetime
    duration: float
    input_variables: Dict[str, Any]
    output: Dict[str, Any]
    error: Optional[str] = None
    retry_attempts: int = 0
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class ValidationReport:
    """Validation report data"""
    flow_name: str
    timestamp: datetime
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    checks_performed: int
    checks_passed: int
    checks_failed: int
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.checks_performed == 0:
            return 0.0
        return (self.checks_passed / self.checks_performed) * 100


@dataclass
class PerformanceReport:
    """Performance report data"""
    flow_name: str
    period_start: datetime
    period_end: datetime
    total_executions: int
    successful_executions: int
    failed_executions: int
    avg_duration: float
    min_duration: float
    max_duration: float
    p50_duration: float
    p95_duration: float
    p99_duration: float
    avg_memory_mb: float
    max_memory_mb: float
    avg_cpu_percent: float
    error_rate: float
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_executions == 0:
            return 0.0
        return (self.successful_executions / self.total_executions) * 100


class ReportGenerator:
    """
    Generates comprehensive reports in various formats
    """
    
    def __init__(self, output_dir: str = "reports"):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_execution_report(
        self,
        execution_data: ExecutionReport,
        format: ReportFormat = ReportFormat.HTML
    ) -> str:
        """
        Generate execution report
        
        Args:
            execution_data: Execution report data
            format: Report format
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"execution_{execution_data.flow_name}_{timestamp}.{format.value}"
        filepath = self.output_dir / filename
        
        if format == ReportFormat.HTML:
            content = self._generate_execution_html(execution_data)
        elif format == ReportFormat.JSON:
            content = self._generate_execution_json(execution_data)
        elif format == ReportFormat.MARKDOWN:
            content = self._generate_execution_markdown(execution_data)
        elif format == ReportFormat.TEXT:
            content = self._generate_execution_text(execution_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_validation_report(
        self,
        validation_data: ValidationReport,
        format: ReportFormat = ReportFormat.HTML
    ) -> str:
        """
        Generate validation report
        
        Args:
            validation_data: Validation report data
            format: Report format
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_{validation_data.flow_name}_{timestamp}.{format.value}"
        filepath = self.output_dir / filename
        
        if format == ReportFormat.HTML:
            content = self._generate_validation_html(validation_data)
        elif format == ReportFormat.JSON:
            content = self._generate_validation_json(validation_data)
        elif format == ReportFormat.MARKDOWN:
            content = self._generate_validation_markdown(validation_data)
        elif format == ReportFormat.TEXT:
            content = self._generate_validation_text(validation_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_performance_report(
        self,
        performance_data: PerformanceReport,
        format: ReportFormat = ReportFormat.HTML
    ) -> str:
        """
        Generate performance report
        
        Args:
            performance_data: Performance report data
            format: Report format
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_{performance_data.flow_name}_{timestamp}.{format.value}"
        filepath = self.output_dir / filename
        
        if format == ReportFormat.HTML:
            content = self._generate_performance_html(performance_data)
        elif format == ReportFormat.JSON:
            content = self._generate_performance_json(performance_data)
        elif format == ReportFormat.MARKDOWN:
            content = self._generate_performance_markdown(performance_data)
        elif format == ReportFormat.TEXT:
            content = self._generate_performance_text(performance_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def generate_summary_report(
        self,
        flows_data: List[Dict[str, Any]],
        format: ReportFormat = ReportFormat.HTML
    ) -> str:
        """
        Generate summary report for multiple flows
        
        Args:
            flows_data: List of flow data
            format: Report format
            
        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.{format.value}"
        filepath = self.output_dir / filename
        
        if format == ReportFormat.HTML:
            content = self._generate_summary_html(flows_data)
        elif format == ReportFormat.JSON:
            content = json.dumps(flows_data, indent=2, default=str)
        elif format == ReportFormat.MARKDOWN:
            content = self._generate_summary_markdown(flows_data)
        elif format == ReportFormat.TEXT:
            content = self._generate_summary_text(flows_data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    # HTML Generators
    
    def _generate_execution_html(self, data: ExecutionReport) -> str:
        """Generate HTML execution report"""
        status_color = "green" if data.status == "success" else "red"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Execution Report - {data.flow_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .status {{ color: {status_color}; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .error {{ color: red; background-color: #ffe6e6; padding: 10px; }}
        .warning {{ color: orange; background-color: #fff4e6; padding: 10px; }}
        .section {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Flow Execution Report</h1>
    
    <div class="section">
        <h2>Execution Details</h2>
        <table>
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Flow Name</td><td>{data.flow_name}</td></tr>
            <tr><td>Execution ID</td><td>{data.execution_id}</td></tr>
            <tr><td>Status</td><td class="status">{data.status.upper()}</td></tr>
            <tr><td>Start Time</td><td>{data.start_time}</td></tr>
            <tr><td>End Time</td><td>{data.end_time}</td></tr>
            <tr><td>Duration</td><td>{data.duration:.2f} seconds</td></tr>
            <tr><td>Retry Attempts</td><td>{data.retry_attempts}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Input Variables</h2>
        <pre>{json.dumps(data.input_variables, indent=2)}</pre>
    </div>
    
    <div class="section">
        <h2>Output</h2>
        <pre>{json.dumps(data.output, indent=2)}</pre>
    </div>
    
    {f'<div class="error"><h3>Error</h3><p>{data.error}</p></div>' if data.error else ''}
    
    {f'<div class="warning"><h3>Warnings</h3><ul>{"".join([f"<li>{w}</li>" for w in data.warnings])}</ul></div>' if data.warnings else ''}
    
    <p><em>Report generated: {datetime.now()}</em></p>
</body>
</html>
"""
        return html
    
    def _generate_validation_html(self, data: ValidationReport) -> str:
        """Generate HTML validation report"""
        status_color = "green" if data.valid else "red"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Validation Report - {data.flow_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .valid {{ color: green; font-weight: bold; }}
        .invalid {{ color: red; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .info {{ color: blue; }}
        ul {{ margin: 10px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px; padding: 10px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>Flow Validation Report</h1>
    
    <h2>Validation Status: <span class="{'valid' if data.valid else 'invalid'}">{('PASSED' if data.valid else 'FAILED').upper()}</span></h2>
    
    <div>
        <h3>Summary Metrics</h3>
        <div class="metric">
            <strong>Success Rate:</strong> {data.success_rate:.1f}%
        </div>
        <div class="metric">
            <strong>Checks Performed:</strong> {data.checks_performed}
        </div>
        <div class="metric">
            <strong>Checks Passed:</strong> {data.checks_passed}
        </div>
        <div class="metric">
            <strong>Checks Failed:</strong> {data.checks_failed}
        </div>
    </div>
    
    {f'<div><h3 class="error">Errors ({len(data.errors)})</h3><ul>{"".join([f"<li>{e}</li>" for e in data.errors])}</ul></div>' if data.errors else ''}
    
    {f'<div><h3 class="warning">Warnings ({len(data.warnings)})</h3><ul>{"".join([f"<li>{w}</li>" for w in data.warnings])}</ul></div>' if data.warnings else ''}
    
    {f'<div><h3 class="info">Information ({len(data.info)})</h3><ul>{"".join([f"<li>{i}</li>" for i in data.info])}</ul></div>' if data.info else ''}
    
    <p><em>Report generated: {datetime.now()}</em></p>
</body>
</html>
"""
        return html
    
    def _generate_performance_html(self, data: PerformanceReport) -> str:
        """Generate HTML performance report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Performance Report - {data.flow_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; border: 2px solid #ddd; border-radius: 5px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
        .section {{ margin: 30px 0; }}
    </style>
</head>
<body>
    <h1>Performance Report: {data.flow_name}</h1>
    
    <div class="section">
        <h2>Period: {data.period_start} to {data.period_end}</h2>
    </div>
    
    <div class="section">
        <h2>Key Metrics</h2>
        <div class="metric">
            <div>Total Executions</div>
            <div class="metric-value">{data.total_executions}</div>
        </div>
        <div class="metric">
            <div>Success Rate</div>
            <div class="metric-value">{data.success_rate:.1f}%</div>
        </div>
        <div class="metric">
            <div>Error Rate</div>
            <div class="metric-value">{data.error_rate:.1f}%</div>
        </div>
        <div class="metric">
            <div>Avg Duration</div>
            <div class="metric-value">{data.avg_duration:.2f}s</div>
        </div>
    </div>
    
    <div class="section">
        <h2>Execution Statistics</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Executions</td><td>{data.total_executions}</td></tr>
            <tr><td>Successful</td><td>{data.successful_executions}</td></tr>
            <tr><td>Failed</td><td>{data.failed_executions}</td></tr>
            <tr><td>Success Rate</td><td>{data.success_rate:.2f}%</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Duration Statistics</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Average</td><td>{data.avg_duration:.2f}s</td></tr>
            <tr><td>Minimum</td><td>{data.min_duration:.2f}s</td></tr>
            <tr><td>Maximum</td><td>{data.max_duration:.2f}s</td></tr>
            <tr><td>50th Percentile</td><td>{data.p50_duration:.2f}s</td></tr>
            <tr><td>95th Percentile</td><td>{data.p95_duration:.2f}s</td></tr>
            <tr><td>99th Percentile</td><td>{data.p99_duration:.2f}s</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Resource Usage</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Avg Memory</td><td>{data.avg_memory_mb:.2f} MB</td></tr>
            <tr><td>Max Memory</td><td>{data.max_memory_mb:.2f} MB</td></tr>
            <tr><td>Avg CPU</td><td>{data.avg_cpu_percent:.1f}%</td></tr>
        </table>
    </div>
    
    <p><em>Report generated: {datetime.now()}</em></p>
</body>
</html>
"""
        return html
    
    def _generate_summary_html(self, flows_data: List[Dict[str, Any]]) -> str:
        """Generate HTML summary report"""
        rows = ""
        for flow in flows_data:
            rows += f"""
            <tr>
                <td>{flow.get('name', 'N/A')}</td>
                <td>{flow.get('executions', 0)}</td>
                <td>{flow.get('success_rate', 0):.1f}%</td>
                <td>{flow.get('avg_duration', 0):.2f}s</td>
                <td>{flow.get('last_execution', 'N/A')}</td>
            </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Summary Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>Flows Summary Report</h1>
    <p>Total Flows: {len(flows_data)}</p>
    
    <table>
        <tr>
            <th>Flow Name</th>
            <th>Executions</th>
            <th>Success Rate</th>
            <th>Avg Duration</th>
            <th>Last Execution</th>
        </tr>
        {rows}
    </table>
    
    <p><em>Report generated: {datetime.now()}</em></p>
</body>
</html>
"""
        return html
    
    # JSON Generators
    
    def _generate_execution_json(self, data: ExecutionReport) -> str:
        """Generate JSON execution report"""
        return json.dumps(asdict(data), indent=2, default=str)
    
    def _generate_validation_json(self, data: ValidationReport) -> str:
        """Generate JSON validation report"""
        return json.dumps(asdict(data), indent=2, default=str)
    
    def _generate_performance_json(self, data: PerformanceReport) -> str:
        """Generate JSON performance report"""
        return json.dumps(asdict(data), indent=2, default=str)
    
    # Markdown Generators
    
    def _generate_execution_markdown(self, data: ExecutionReport) -> str:
        """Generate Markdown execution report"""
        md = f"""# Flow Execution Report

## Execution Details

| Property | Value |
|----------|-------|
| Flow Name | {data.flow_name} |
| Execution ID | {data.execution_id} |
| Status | **{data.status.upper()}** |
| Start Time | {data.start_time} |
| End Time | {data.end_time} |
| Duration | {data.duration:.2f}s |
| Retry Attempts | {data.retry_attempts} |

## Input Variables

```json
{json.dumps(data.input_variables, indent=2)}
```

## Output

```json
{json.dumps(data.output, indent=2)}
```

{f'## Error\\n\\n```\\n{data.error}\\n```' if data.error else ''}

{f'## Warnings\\n\\n' + '\\n'.join([f'- {w}' for w in data.warnings]) if data.warnings else ''}

---
*Report generated: {datetime.now()}*
"""
        return md
    
    def _generate_validation_markdown(self, data: ValidationReport) -> str:
        """Generate Markdown validation report"""
        status = "✅ PASSED" if data.valid else "❌ FAILED"
        
        md = f"""# Flow Validation Report

## Status: {status}

### Summary Metrics

- **Success Rate**: {data.success_rate:.1f}%
- **Checks Performed**: {data.checks_performed}
- **Checks Passed**: {data.checks_passed}
- **Checks Failed**: {data.checks_failed}

{f'### ❌ Errors ({len(data.errors)})\\n\\n' + '\\n'.join([f'- {e}' for e in data.errors]) if data.errors else ''}

{f'### ⚠️ Warnings ({len(data.warnings)})\\n\\n' + '\\n'.join([f'- {w}' for w in data.warnings]) if data.warnings else ''}

{f'### ℹ️ Information ({len(data.info)})\\n\\n' + '\\n'.join([f'- {i}' for i in data.info]) if data.info else ''}

---
*Report generated: {datetime.now()}*
"""
        return md
    
    def _generate_performance_markdown(self, data: PerformanceReport) -> str:
        """Generate Markdown performance report"""
        md = f"""# Performance Report: {data.flow_name}

## Period
{data.period_start} to {data.period_end}

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Executions | {data.total_executions} |
| Success Rate | {data.success_rate:.2f}% |
| Error Rate | {data.error_rate:.2f}% |
| Avg Duration | {data.avg_duration:.2f}s |

## Execution Statistics

| Metric | Value |
|--------|-------|
| Successful | {data.successful_executions} |
| Failed | {data.failed_executions} |

## Duration Statistics

| Metric | Value |
|--------|-------|
| Average | {data.avg_duration:.2f}s |
| Minimum | {data.min_duration:.2f}s |
| Maximum | {data.max_duration:.2f}s |
| 50th Percentile | {data.p50_duration:.2f}s |
| 95th Percentile | {data.p95_duration:.2f}s |
| 99th Percentile | {data.p99_duration:.2f}s |

## Resource Usage

| Metric | Value |
|--------|-------|
| Avg Memory | {data.avg_memory_mb:.2f} MB |
| Max Memory | {data.max_memory_mb:.2f} MB |
| Avg CPU | {data.avg_cpu_percent:.1f}% |

---
*Report generated: {datetime.now()}*
"""
        return md
    
    def _generate_summary_markdown(self, flows_data: List[Dict[str, Any]]) -> str:
        """Generate Markdown summary report"""
        rows = "\n".join([
            f"| {f.get('name', 'N/A')} | {f.get('executions', 0)} | {f.get('success_rate', 0):.1f}% | {f.get('avg_duration', 0):.2f}s | {f.get('last_execution', 'N/A')} |"
            for f in flows_data
        ])
        
        md = f"""# Flows Summary Report

**Total Flows**: {len(flows_data)}

| Flow Name | Executions | Success Rate | Avg Duration | Last Execution |
|-----------|------------|--------------|--------------|----------------|
{rows}

---
*Report generated: {datetime.now()}*
"""
        return md
    
    # Text Generators
    
    def _generate_execution_text(self, data: ExecutionReport) -> str:
        """Generate plain text execution report"""
        text = f"""
FLOW EXECUTION REPORT
{'='*60}

Execution Details:
  Flow Name:      {data.flow_name}
  Execution ID:   {data.execution_id}
  Status:         {data.status.upper()}
  Start Time:     {data.start_time}
  End Time:       {data.end_time}
  Duration:       {data.duration:.2f}s
  Retry Attempts: {data.retry_attempts}

Input Variables:
{json.dumps(data.input_variables, indent=2)}

Output:
{json.dumps(data.output, indent=2)}

{f'Error:\\n{data.error}' if data.error else ''}

{f'Warnings:\\n' + '\\n'.join([f'  - {w}' for w in data.warnings]) if data.warnings else ''}

{'='*60}
Report generated: {datetime.now()}
"""
        return text
    
    def _generate_validation_text(self, data: ValidationReport) -> str:
        """Generate plain text validation report"""
        status = "PASSED" if data.valid else "FAILED"
        
        text = f"""
FLOW VALIDATION REPORT
{'='*60}

Status: {status}

Summary Metrics:
  Success Rate:      {data.success_rate:.1f}%
  Checks Performed:  {data.checks_performed}
  Checks Passed:     {data.checks_passed}
  Checks Failed:     {data.checks_failed}

{f'Errors ({len(data.errors)}): \\n' + '\\n'.join([f'  - {e}' for e in data.errors]) if data.errors else ''}

{f'Warnings ({len(data.warnings)}): \\n' + '\\n'.join([f'  - {w}' for w in data.warnings]) if data.warnings else ''}

{f'Information ({len(data.info)}): \\n' + '\\n'.join([f'  - {i}' for i in data.info]) if data.info else ''}

{'='*60}
Report generated: {datetime.now()}
"""
        return text
    
    def _generate_performance_text(self, data: PerformanceReport) -> str:
        """Generate plain text performance report"""
        text = f"""
PERFORMANCE REPORT: {data.flow_name}
{'='*60}

Period: {data.period_start} to {data.period_end}

Key Metrics:
  Total Executions: {data.total_executions}
  Success Rate:     {data.success_rate:.2f}%
  Error Rate:       {data.error_rate:.2f}%
  Avg Duration:     {data.avg_duration:.2f}s

Execution Statistics:
  Successful: {data.successful_executions}
  Failed:     {data.failed_executions}

Duration Statistics:
  Average:          {data.avg_duration:.2f}s
  Minimum:          {data.min_duration:.2f}s
  Maximum:          {data.max_duration:.2f}s
  50th Percentile:  {data.p50_duration:.2f}s
  95th Percentile:  {data.p95_duration:.2f}s
  99th Percentile:  {data.p99_duration:.2f}s

Resource Usage:
  Avg Memory: {data.avg_memory_mb:.2f} MB
  Max Memory: {data.max_memory_mb:.2f} MB
  Avg CPU:    {data.avg_cpu_percent:.1f}%

{'='*60}
Report generated: {datetime.now()}
"""
        return text
    
    def _generate_summary_text(self, flows_data: List[Dict[str, Any]]) -> str:
        """Generate plain text summary report"""
        rows = "\n".join([
            f"  {f.get('name', 'N/A'):<30} {f.get('executions', 0):>10} {f.get('success_rate', 0):>10.1f}% {f.get('avg_duration', 0):>12.2f}s"
            for f in flows_data
        ])
        
        text = f"""
FLOWS SUMMARY REPORT
{'='*60}

Total Flows: {len(flows_data)}

{'Flow Name':<30} {'Executions':>10} {'Success Rate':>13} {'Avg Duration':>13}
{'-'*70}
{rows}

{'='*60}
Report generated: {datetime.now()}
"""
        return text
