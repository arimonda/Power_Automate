# Power Automate Desktop Framework - User Manual

## 📖 Complete User Guide

**Version**: 1.0.0  
**Last Updated**: February 11, 2026  
**Difficulty**: Beginner to Advanced

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First Steps](#first-steps)
4. [Understanding Flows](#understanding-flows)
5. [Working with the Framework](#working-with-the-framework)
6. [Configuration Guide](#configuration-guide)
7. [Flow Management](#flow-management)
8. [Execution & Monitoring](#execution--monitoring)
9. [Integrations](#integrations)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [FAQ](#faq)

---

## Introduction

### What is This Framework?

The Power Automate Desktop (PAD) Framework is a Python-based tool that helps you:
- **Manage** your Power Automate Desktop flows
- **Execute** flows programmatically
- **Monitor** flow performance
- **Integrate** with databases, emails, APIs, and more
- **Schedule** automatic flow execution
- **Test** and validate your flows

### Who Should Use This?

- Automation developers
- Business process analysts
- IT administrators
- Anyone working with Power Automate Desktop

### What You Need

- **Python 3.8 or higher**
- **Power Automate Desktop** installed on Windows
- **Basic Python knowledge** (helpful but not required)

---

## Installation

### Step 1: Check Python Installation

Open PowerShell and check if Python is installed:

```powershell
python --version
```

If you see `Python 3.8.x` or higher, you're good! If not, download from [python.org](https://python.org).

### Step 2: Navigate to Project Folder

```powershell
cd "c:\Users\arimo\.projects\Power_Automate"
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install all required packages. Wait for it to complete (2-5 minutes).

### Step 4: Verify Installation

```powershell
python main.py
```

You should see:
```
============================================================
Power Automate Desktop Framework
Version 1.0.0 - All Features Enabled
============================================================
✓ Framework initialized successfully
```

✅ **Installation Complete!**

---

## First Steps

### Your First Program

Create a file called `my_first_flow.py`:

```python
# Import the framework
from pad_framework import PADFramework

# Create framework instance
pad = PADFramework()

# Check if framework is healthy
health = pad.get_health_status()
print(f"Framework Status: {health['status']}")

# List available flows
flows = pad.list_flows()
print(f"Available flows: {flows}")
```

Run it:
```powershell
python my_first_flow.py
```

### Understanding the Output

```
Framework Status: healthy
Available flows: ['ExampleFlow']
```

- `healthy` means everything is working
- `ExampleFlow` is a sample flow included with the framework

---

## Understanding Flows

### What is a Flow?

A **flow** is an automation sequence created in Power Automate Desktop. Think of it as a recipe:
- **Ingredients** = Input variables
- **Steps** = Actions (click, type, read data, etc.)
- **Final Dish** = Output results

### Flow Structure

Every flow has:

```json
{
  "name": "MyFlow",
  "description": "What this flow does",
  "variables": {
    "input": { "param1": "value" },
    "output": { "result": "value" }
  },
  "actions": [
    { "type": "Action1", "parameters": {} },
    { "type": "Action2", "parameters": {} }
  ]
}
```

### Where Are Flows Stored?

Flows are stored in the `flows/` folder as `.json` files:

```
flows/
  ├── ExampleFlow.json
  ├── MyFlow.json
  └── DataProcessor.json
```

---

## Working with the Framework

### The PADFramework Class

This is your main tool. Everything starts here:

```python
from pad_framework import PADFramework

pad = PADFramework()
```

### Common Operations

#### 1. List Flows

```python
# List all flows
all_flows = pad.list_flows()
print(f"Found {len(all_flows)} flows")

# Search for specific flows
test_flows = pad.list_flows(search_pattern="test")
print(f"Test flows: {test_flows}")
```

#### 2. Execute a Flow

```python
result = pad.execute_flow(
    flow_name="ExampleFlow",
    input_variables={
        "inputParam1": "Hello World",
        "inputParam2": 42
    }
)

# Check if successful
if result.status == "success":
    print("✓ Flow completed!")
    print(f"Duration: {result.duration} seconds")
    print(f"Output: {result.output}")
else:
    print("✗ Flow failed!")
    print(f"Error: {result.error}")
```

#### 3. Create a New Flow

```python
# Create from template
success = pad.create_flow(
    flow_name="MyNewFlow",
    template="basic"
)

if success:
    print("✓ Flow created successfully!")
```

#### 4. Validate a Flow

```python
validation = pad.validate_flow("MyNewFlow")

if validation["valid"]:
    print("✓ Flow is valid")
else:
    print("✗ Flow has errors:")
    for error in validation["errors"]:
        print(f"  - {error}")
```

#### 5. Check Framework Health

```python
health = pad.get_health_status()

print(f"Status: {health['status']}")
print(f"Version: {health['version']}")
print(f"Available flows: {health['flows_available']}")
```

---

## Configuration Guide

### Configuration File Location

Main configuration: `configs/config.yaml`

### Understanding config.yaml

```yaml
# Execution settings
execution:
  default_timeout: 300        # 5 minutes
  max_concurrent_flows: 5     # Run up to 5 flows at once
  retry_enabled: true         # Auto-retry on failure
  default_retry_count: 3      # Try 3 times before giving up

# Logging settings
logging:
  level: "INFO"               # DEBUG, INFO, WARNING, ERROR
  console_output: true        # Show logs in console
  file_output: true           # Save logs to file

# Performance monitoring
performance:
  monitoring_enabled: true    # Track performance
  collect_metrics: true       # Collect detailed metrics
```

### Environment Variables

Create a `.env` file for sensitive data:

```env
# Copy from .env.example
PAD_LOG_LEVEL=INFO
PAD_SMTP_SERVER=smtp.gmail.com
PAD_SMTP_PORT=587
PAD_EMAIL_USER=your-email@gmail.com
PAD_EMAIL_PASSWORD=your-app-password
```

**Important**: Never commit `.env` to version control!

### Changing Settings

#### Method 1: Edit config.yaml

```yaml
execution:
  default_timeout: 600  # Change to 10 minutes
```

#### Method 2: Environment Variables

```powershell
$env:PAD_LOG_LEVEL="DEBUG"
python my_script.py
```

#### Method 3: In Code

```python
config = Config()
config.set("execution.default_timeout", 600)
```

---

## Flow Management

### Creating Flows

#### Option 1: Use the Framework

```python
pad = PADFramework()

# Create basic flow
pad.create_flow("DataProcessor", template="basic")

# Create from scratch
pad.create_flow("CustomFlow")
```

#### Option 2: Manual Creation

Create `flows/MyFlow.json`:

```json
{
  "name": "MyFlow",
  "description": "My custom flow",
  "version": "1.0",
  "enabled": true,
  "variables": {
    "input": {
      "fileName": {
        "type": "string",
        "default": "",
        "description": "File to process"
      }
    },
    "output": {
      "result": {
        "type": "string",
        "description": "Processing result"
      }
    }
  },
  "actions": [],
  "error_handling": {
    "on_error": "stop",
    "retry_count": 2
  },
  "settings": {
    "timeout": 300,
    "priority": 5
  }
}
```

### Editing Flows

1. **Find the flow file** in `flows/` folder
2. **Edit with text editor** (VS Code, Notepad++)
3. **Validate changes**:

```python
validation = pad.validate_flow("MyFlow")
if validation["valid"]:
    print("✓ Flow is valid")
```

### Importing Flows

```python
# Import from another location
pad.import_flow(
    flow_path="C:/backup/MyFlow.json",
    flow_name="ImportedFlow"
)
```

### Exporting Flows

```python
# Export for backup or sharing
pad.export_flow(
    flow_name="MyFlow",
    output_path="C:/backup/MyFlow.json"
)
```

### Deleting Flows

```python
# Delete a flow (be careful!)
pad.flow_manager.delete_flow("OldFlow")
```

---

## Execution & Monitoring

### Basic Execution

```python
result = pad.execute_flow("MyFlow", {})
print(result.status)  # success, failed, timeout, cancelled
```

### With Timeout

```python
# Stop after 2 minutes
result = pad.execute_flow(
    flow_name="LongRunningFlow",
    timeout=120  # seconds
)
```

### With Retry

```python
# Retry up to 3 times on failure
result = pad.execute_flow(
    flow_name="UnreliableFlow",
    retry_count=3
)
```

### With Input Variables

```python
result = pad.execute_flow(
    flow_name="DataProcessor",
    input_variables={
        "fileName": "data.xlsx",
        "sheetName": "Sheet1",
        "outputFolder": "results/"
    }
)

# Access output
if result.status == "success":
    output_file = result.output.get("outputFile")
    print(f"Output saved to: {output_file}")
```

### Monitoring Performance

```python
# Execute flow
pad.execute_flow("MyFlow", {})

# Get performance statistics
stats = pad.get_performance_stats("MyFlow")

print(f"Executions: {stats['execution_count']}")
print(f"Average time: {stats['avg_duration']:.2f}s")
print(f"Fastest: {stats['min_duration']:.2f}s")
print(f"Slowest: {stats['max_duration']:.2f}s")
print(f"Memory used: {stats['avg_memory_delta_mb']:.2f}MB")
```

### Scheduling Flows

```python
# Schedule daily at 9 AM
schedule_id = pad.schedule_flow(
    flow_name="DailyReport",
    schedule="0 9 * * *",  # Cron format
    input_variables={"date": "today"}
)

print(f"Scheduled with ID: {schedule_id}")

# Cancel schedule later
pad.cancel_schedule(schedule_id)
```

### Cron Schedule Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-6, Sunday=0)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

Examples:
- `0 9 * * *` - Every day at 9:00 AM
- `0 */2 * * *` - Every 2 hours
- `30 8 * * 1-5` - Weekdays at 8:30 AM
- `0 0 1 * *` - First day of every month

---

## Integrations

### Email Integration

#### Setup

Edit `.env`:
```env
PAD_SMTP_SERVER=smtp.gmail.com
PAD_SMTP_PORT=587
PAD_EMAIL_USER=your-email@gmail.com
PAD_EMAIL_PASSWORD=your-app-password
```

#### Send Email

```python
# Initialize email integration
email = pad.integrate("email")

# In your flow, use email capabilities
# (Framework handles the connection)
```

### Database Integration

#### SQLite (Default)

```python
# Database integration
db = pad.integrate("database", type="sqlite")

# Use in your flows to store/retrieve data
```

#### SQL Server

Edit `config.yaml`:
```yaml
database:
  enabled: true
  type: "sqlserver"
  connection_string: "DRIVER={SQL Server};SERVER=localhost;DATABASE=mydb;UID=user;PWD=pass"
```

### API Integration

```python
# API integration
api = pad.integrate(
    "api",
    endpoint="https://api.example.com"
)

# Make API calls in your flows
```

### Web Automation

```python
# Web automation with Chrome
web = pad.integrate(
    "web",
    browser="chrome",
    headless=False
)
```

### File Operations

```python
# File operations integration
files = pad.integrate("file")

# Use for Excel, CSV, JSON operations in flows
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Flow not found"

**Problem**: Flow file doesn't exist or wrong name

**Solution**:
```python
# List all flows to see actual names
flows = pad.list_flows()
print(flows)

# Check file exists
import os
flow_path = "flows/MyFlow.json"
if os.path.exists(flow_path):
    print("✓ Flow file exists")
else:
    print("✗ Flow file not found")
```

#### Issue 2: "Module not found"

**Problem**: Dependencies not installed

**Solution**:
```powershell
pip install -r requirements.txt
```

#### Issue 3: "Timeout error"

**Problem**: Flow takes too long

**Solution**:
```python
# Increase timeout
result = pad.execute_flow(
    flow_name="LongFlow",
    timeout=600  # 10 minutes
)
```

#### Issue 4: "Permission denied"

**Problem**: Need administrator rights

**Solution**:
- Right-click PowerShell
- Select "Run as Administrator"
- Try again

#### Issue 5: "Configuration error"

**Problem**: Invalid configuration

**Solution**:
```python
# Validate configuration
config = Config()
print(config.to_dict())

# Reset to defaults
# Delete configs/config.yaml and restart
```

### Getting Help

1. **Check logs**: `logs/pad_framework_YYYY-MM-DD.log`
2. **Read documentation**: `docs/` folder
3. **Check examples**: `examples/` folder
4. **Enable debug mode**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Best Practices

### 1. Always Validate Before Executing

```python
validation = pad.validate_flow("MyFlow")
if validation["valid"]:
    result = pad.execute_flow("MyFlow", {})
```

### 2. Use Try-Except for Error Handling

```python
try:
    result = pad.execute_flow("MyFlow", {})
    if result.status == "success":
        print("✓ Success!")
except Exception as e:
    print(f"✗ Error: {e}")
```

### 3. Enable Retry for Critical Flows

```python
result = pad.execute_flow(
    flow_name="CriticalFlow",
    retry_count=3
)
```

### 4. Monitor Performance Regularly

```python
# After executions, check stats
stats = pad.get_performance_stats()
for flow_name, flow_stats in stats.items():
    if flow_stats["avg_duration"] > 60:
        print(f"⚠ {flow_name} is slow!")
```

### 5. Keep Sensitive Data in .env

```python
# ❌ DON'T
password = "my_secret_password"

# ✅ DO
import os
password = os.getenv("MY_PASSWORD")
```

### 6. Use Meaningful Flow Names

```python
# ❌ DON'T
pad.create_flow("flow1")

# ✅ DO
pad.create_flow("ProcessMonthlyInvoices")
```

### 7. Log Important Events

```python
result = pad.execute_flow("MyFlow", {})
if result.status == "success":
    pad.logger.info(f"Flow completed: {result.duration}s")
```

### 8. Clean Up Resources

```python
# At end of script
pad.cleanup()
```

---

## FAQ

### Q: Do I need Power Automate Desktop installed?

**A**: Yes, this framework works with PAD. It executes flows created in PAD.

### Q: Can I run flows on a schedule?

**A**: Yes! Use `schedule_flow()` with cron expressions.

### Q: How do I see what went wrong?

**A**: Check logs in `logs/` folder or use:
```python
result = pad.execute_flow("MyFlow", {})
if result.status == "failed":
    print(result.error)
```

### Q: Can I run multiple flows at once?

**A**: Yes, configure in `config.yaml`:
```yaml
execution:
  max_concurrent_flows: 5
```

### Q: How do I update the framework?

**A**: Pull latest changes and reinstall:
```powershell
git pull
pip install -r requirements.txt
```

### Q: Is this production-ready?

**A**: Yes! It includes error handling, logging, monitoring, and testing.

### Q: Can I contribute?

**A**: Yes! Follow the code structure and add your features.

### Q: What Python version do I need?

**A**: Python 3.8 or higher.

### Q: Where are logs stored?

**A**: In the `logs/` folder with automatic rotation.

### Q: How do I back up my flows?

**A**: Copy the `flows/` folder or use:
```python
pad.export_flow("MyFlow", "backup/MyFlow.json")
```

---

## Quick Reference Card

### Essential Commands

```python
# Import
from pad_framework import PADFramework
pad = PADFramework()

# Execute
result = pad.execute_flow("FlowName", {"param": "value"})

# List flows
flows = pad.list_flows()

# Create flow
pad.create_flow("NewFlow", template="basic")

# Validate
validation = pad.validate_flow("FlowName")

# Schedule
schedule_id = pad.schedule_flow("FlowName", "0 9 * * *")

# Performance
stats = pad.get_performance_stats("FlowName")

# Health check
health = pad.get_health_status()

# Cleanup
pad.cleanup()
```

### File Locations

- **Flows**: `flows/*.json`
- **Config**: `configs/config.yaml`
- **Environment**: `.env`
- **Logs**: `logs/*.log`
- **Data**: `data/`
- **Examples**: `examples/*.py`
- **Documentation**: `docs/*.md`

---

## Getting More Help

- **Getting Started**: `docs/getting_started.md`
- **API Reference**: `docs/api_reference.md`
- **Best Practices**: `docs/best_practices.md`
- **Learning Module**: `LEARNING_MODULE.md`
- **Quick Start**: `QUICKSTART.md`
- **Features**: `FEATURES.md`

---

**Need more help?** Check the Learning Module for step-by-step tutorials!

**Framework Version**: 1.0.0  
**Last Updated**: February 11, 2026
