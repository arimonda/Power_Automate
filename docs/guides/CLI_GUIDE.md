# CLI Usage Guide

## 🖥️ Professional Command-Line Interface

The PAD Framework includes a powerful command-line interface for managing and executing flows.

---

## Installation

### Ensure CLI is Available

```bash
# Install in development mode
pip install -e .

# Or install the package
pip install .

# Verify installation
pad --version
```

---

## Quick Start

```bash
# Check framework health
pad health

# List all flows
pad list

# Execute a flow
pad execute MyFlow

# View help
pad --help
```

---

## Commands Reference

### Global Options

```bash
pad [OPTIONS] COMMAND [ARGS]...

Options:
  --config, -c PATH    Path to configuration file
  --verbose, -v        Enable verbose output
  --version           Show version and exit
  --help              Show help message
```

---

## Command Details

### 1. health - Check Framework Health

**Usage**:
```bash
pad health
```

**Output**:
```
============================================================
FRAMEWORK HEALTH STATUS
============================================================

Status: HEALTHY
Version: 1.0.0
Timestamp: 2026-02-11T10:30:00

Flows Available: 5
Active Schedules: 2

Performance:
  Total Flows Tracked: 5
  Total Executions: 127
  System CPU: 15.3%
  System Memory: 45.2%

============================================================
```

**Use Cases**:
- Quick health check
- Pre-deployment validation
- Monitoring scripts
- Troubleshooting

---

### 2. list - List Flows

**Usage**:
```bash
pad list [OPTIONS]

Options:
  --search, -s TEXT  Search pattern for filtering flows
  --json            Output as JSON
```

**Examples**:
```bash
# List all flows
pad list

# Search for specific flows
pad list --search "report"
pad list -s "data"

# JSON output for scripting
pad list --json
```

**Output**:
```
Available Flows (5 found):

  1. DataProcessor
  2. EmailReport
  3. MonthlyReport
  4. SystemBackup
  5. UserSync
```

**JSON Output**:
```json
{
  "flows": [
    "DataProcessor",
    "EmailReport",
    "MonthlyReport",
    "SystemBackup",
    "UserSync"
  ]
}
```

---

### 3. execute - Execute Flow

**Usage**:
```bash
pad execute FLOW_NAME [OPTIONS]

Options:
  --input, -i TEXT    Input variables as JSON string or @file.json
  --timeout, -t INT   Execution timeout in seconds
  --retry, -r INT     Number of retry attempts (default: 0)
  --json             Output as JSON
```

**Examples**:
```bash
# Simple execution
pad execute MyFlow

# With input variables (inline JSON)
pad execute DataProcessor --input '{"file": "data.csv", "output": "results/"}'

# From file
pad execute DataProcessor --input @input.json

# With timeout and retry
pad execute LongFlow --timeout 600 --retry 3

# JSON output
pad execute MyFlow --json
```

**Output**:
```
Executing flow: DataProcessor

✓ Flow executed successfully

Execution Details:
  Status: success
  Duration: 45.32s
  Execution ID: a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6
```

**JSON Output**:
```json
{
  "flow_name": "DataProcessor",
  "status": "success",
  "duration": 45.32,
  "execution_id": "a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6",
  "start_time": "2026-02-11T10:30:00",
  "end_time": "2026-02-11T10:30:45",
  "output": {
    "records_processed": 1250,
    "output_file": "results/output.csv"
  },
  "error": null
}
```

---

### 4. create - Create Flow

**Usage**:
```bash
pad create FLOW_NAME [OPTIONS]

Options:
  --template, -t TEXT  Template to use
```

**Examples**:
```bash
# Create with default template
pad create NewFlow

# Create from template
pad create ReportFlow --template report

# Create custom flow
pad create CustomFlow -t custom
```

**Output**:
```
✓ Flow 'NewFlow' created successfully
```

---

### 5. validate - Validate Flow

**Usage**:
```bash
pad validate FLOW_NAME [OPTIONS]

Options:
  --json  Output as JSON
```

**Examples**:
```bash
# Validate a flow
pad validate MyFlow

# JSON output
pad validate MyFlow --json
```

**Output**:
```
Validation Results for 'MyFlow':

✓ Flow is valid

Info:
  • Flow validation completed for: MyFlow
```

**With Errors**:
```
Validation Results for 'BrokenFlow':

✗ Flow has errors

Errors:
  • Missing required field: version
  • Actions must be a list

Warnings:
  • Flow has no actions
```

---

### 6. schedule - Schedule Flow

**Usage**:
```bash
pad schedule FLOW_NAME SCHEDULE [OPTIONS]

Options:
  --input, -i TEXT  Input variables as JSON string
```

**Examples**:
```bash
# Schedule daily at 9 AM
pad schedule DailyReport "0 9 * * *"

# Schedule with input variables
pad schedule EmailReport "0 8 * * 1-5" --input '{"recipients": ["team@company.com"]}'

# Schedule every 2 hours
pad schedule DataSync "0 */2 * * *"
```

**Cron Format**:
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-6, Sunday=0)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

**Output**:
```
✓ Flow scheduled successfully
Schedule ID: s1234567-89ab-cdef-0123-456789abcdef
Schedule: 0 9 * * *
```

---

### 7. stats - View Statistics

**Usage**:
```bash
pad stats [FLOW_NAME] [OPTIONS]

Options:
  --json  Output as JSON
```

**Examples**:
```bash
# All flows statistics
pad stats

# Specific flow
pad stats MyFlow

# JSON output
pad stats --json
```

**Output (All Flows)**:
```
Performance Statistics

╒══════════════════╤═══════════════╤═══════════════╤═══════════════╕
│ Flow             │   Executions  │  Avg Duration │  Max Duration │
╞══════════════════╪═══════════════╪═══════════════╪═══════════════╡
│ DataProcessor    │           45  │       12.34s  │       45.67s  │
│ EmailReport      │           23  │        3.21s  │        8.90s  │
│ UserSync         │           12  │       89.01s  │      123.45s  │
╘══════════════════╧═══════════════╧═══════════════╧═══════════════╛
```

**Output (Single Flow)**:
```
Performance Statistics

Flow: DataProcessor
  Executions: 45
  Avg Duration: 12.34s
  Min Duration: 8.90s
  Max Duration: 45.67s
  Avg Memory: 123.45MB
```

---

### 8. logs - View Logs

**Usage**:
```bash
pad logs [OPTIONS]

Options:
  --level, -l TEXT      Filter by log level (DEBUG, INFO, WARNING, ERROR)
  --flow, -f TEXT       Filter by flow name
  --lines, -n INTEGER   Number of lines to show (default: 50)
```

**Examples**:
```bash
# View last 50 log entries
pad logs

# View errors only
pad logs --level ERROR

# Filter by flow
pad logs --flow DataProcessor

# Show more lines
pad logs --lines 100

# Combine filters
pad logs --level WARNING --flow MyFlow --lines 20
```

**Output**:
```
Log Entries (showing last 50):

[2026-02-11 10:30:00] INFO      Flow execution started: DataProcessor
[2026-02-11 10:30:05] DEBUG     Processing record 1/1000
[2026-02-11 10:30:45] INFO      Flow execution completed: DataProcessor
[2026-02-11 10:31:00] ERROR     Flow execution failed: BrokenFlow
```

---

### 9. config - Show Configuration

**Usage**:
```bash
pad config
```

**Examples**:
```bash
# View current configuration
pad config

# Use with jq for filtering
pad config | jq '.execution'
```

**Output**: JSON configuration

---

### 10. test - Run Tests

**Usage**:
```bash
pad test [OPTIONS]

Options:
  --pattern, -p TEXT  Test pattern to filter
  --verbose, -v      Verbose output
```

**Examples**:
```bash
# Run all tests
pad test

# Run specific tests
pad test --pattern test_flow

# Verbose output
pad test --verbose
```

---

## Scripting Examples

### Shell Script Integration

```bash
#!/bin/bash

# Execute flow and capture result
result=$(pad execute DataProcessor --json)

# Parse JSON and check status
status=$(echo $result | jq -r '.status')

if [ "$status" == "success" ]; then
    echo "✓ Flow completed successfully"
    
    # Get duration
    duration=$(echo $result | jq -r '.duration')
    echo "Duration: ${duration}s"
    
    exit 0
else
    echo "✗ Flow failed"
    error=$(echo $result | jq -r '.error')
    echo "Error: $error"
    
    exit 1
fi
```

### Python Script Integration

```python
import subprocess
import json

# Execute via CLI
result = subprocess.run(
    ["pad", "execute", "DataProcessor", "--json"],
    capture_output=True,
    text=True
)

# Parse result
data = json.loads(result.stdout)

if data["status"] == "success":
    print(f"✓ Success in {data['duration']}s")
else:
    print(f"✗ Failed: {data['error']}")
```

### PowerShell Script

```powershell
# Execute flow
$result = pad execute DataProcessor --json | ConvertFrom-Json

# Check status
if ($result.status -eq "success") {
    Write-Host "✓ Flow completed" -ForegroundColor Green
    Write-Host "Duration: $($result.duration)s"
} else {
    Write-Host "✗ Flow failed" -ForegroundColor Red
    Write-Host "Error: $($result.error)"
}
```

---

## Automation Examples

### Cron Job

```bash
# /etc/cron.d/pad-jobs

# Daily report at 9 AM
0 9 * * * user cd /app && pad execute DailyReport

# Hourly data sync
0 * * * * user cd /app && pad execute DataSync

# Weekly backup on Sunday at 2 AM
0 2 * * 0 user cd /app && pad execute WeeklyBackup
```

### Windows Task Scheduler

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "pad" -Argument "execute DailyReport"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "PAD-DailyReport" -Action $action -Trigger $trigger
```

### CI/CD Integration

```yaml
# .github/workflows/pad-flows.yml
name: Execute PAD Flows

on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: pip install -e .
      
      - name: Execute flow
        run: |
          result=$(pad execute DailyReport --json)
          echo $result | jq '.'
```

---

## Tips & Tricks

### 1. Use JSON Output for Scripting

```bash
# Easier to parse
pad list --json | jq '.flows[] | select(contains("Report"))'
```

### 2. Set Configuration Path

```bash
# Use custom config
pad --config /path/to/config.yaml execute MyFlow
```

### 3. Combine with Other Tools

```bash
# Send to Slack on failure
pad execute MyFlow --json | jq -r '.status' | grep -q failed && \
  curl -X POST $SLACK_WEBHOOK -d '{"text": "Flow failed"}'
```

### 4. Monitor Execution

```bash
# Watch stats in real-time
watch -n 5 'pad stats'
```

### 5. Create Aliases

```bash
# Add to .bashrc or .zshrc
alias pex='pad execute'
alias pls='pad list'
alias pst='pad stats'

# Usage
pex MyFlow --retry 3
pls --search report
pst MyFlow
```

---

## Troubleshooting

### Command Not Found

```bash
# Ensure package is installed
pip install -e .

# Or add to PATH
export PATH="$PATH:/path/to/pad_framework"
```

### Permission Errors

```bash
# Run with appropriate permissions
sudo pad execute MyFlow

# Or fix permissions
chmod +x $(which pad)
```

### JSON Parsing Errors

```bash
# Validate JSON output
pad execute MyFlow --json | jq '.'

# Pretty print
pad execute MyFlow --json | jq '.output'
```

---

## Best Practices

1. **Always use --json for scripts** - Easier to parse
2. **Set appropriate timeouts** - Prevent hanging
3. **Use verbose mode for debugging** - More information
4. **Check exit codes** - Proper error handling
5. **Log CLI operations** - Audit trail
6. **Use configuration files** - Consistency
7. **Test commands first** - Validate syntax

---

**CLI Version**: 1.0.0  
**Last Updated**: February 11, 2026  
**Status**: Production Ready ✅
