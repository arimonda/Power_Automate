# Quick Reference Guide

## 🚀 One-Page Cheat Sheet

---

## Installation

```powershell
cd "c:\Users\arimo\.projects\Power_Automate"
pip install -r requirements.txt
python main.py
```

---

## Basic Usage

```python
from pad_framework import PADFramework

# Initialize
pad = PADFramework()

# Execute flow
result = pad.execute_flow("FlowName", {"param": "value"})

# Check result
if result.status == "success":
    print(f"✓ Done in {result.duration}s")
```

---

## Common Operations

| Operation | Code |
|-----------|------|
| **List flows** | `pad.list_flows()` |
| **Search flows** | `pad.list_flows(search_pattern="test")` |
| **Create flow** | `pad.create_flow("NewFlow", template="basic")` |
| **Validate flow** | `pad.validate_flow("FlowName")` |
| **Execute flow** | `pad.execute_flow("FlowName", {...})` |
| **Health check** | `pad.get_health_status()` |
| **Performance** | `pad.get_performance_stats("FlowName")` |
| **Schedule** | `pad.schedule_flow("FlowName", "0 9 * * *")` |

---

## Execution Options

```python
result = pad.execute_flow(
    flow_name="MyFlow",
    input_variables={"key": "value"},
    timeout=300,        # 5 minutes
    retry_count=3       # Retry 3 times
)
```

---

## Result Object

```python
result.status          # success, failed, timeout, cancelled
result.duration        # Execution time in seconds
result.output          # Output variables
result.error           # Error message (if failed)
result.execution_id    # Unique ID
result.start_time      # When started
result.end_time        # When ended
```

---

## Configuration

**File**: `configs/config.yaml`

```yaml
execution:
  default_timeout: 300
  retry_enabled: true
  default_retry_count: 3

logging:
  level: "INFO"
  console_output: true
  file_output: true

performance:
  monitoring_enabled: true
```

**Environment**: `.env`

```env
PAD_LOG_LEVEL=INFO
PAD_SMTP_SERVER=smtp.gmail.com
PAD_EMAIL_USER=user@example.com
```

---

## Scheduling (Cron Format)

```
* * * * *
│ │ │ │ └─ Day of week (0-6)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

**Examples**:
- `0 9 * * *` → Every day at 9 AM
- `0 */2 * * *` → Every 2 hours
- `30 8 * * 1-5` → Weekdays at 8:30 AM
- `0 0 1 * *` → First day of month

---

## Integrations

```python
# Database
db = pad.integrate("database")

# Email
email = pad.integrate("email")

# API
api = pad.integrate("api", endpoint="https://...")

# Web
web = pad.integrate("web")

# Files
files = pad.integrate("file")
```

---

## Error Handling

```python
try:
    result = pad.execute_flow("MyFlow", {})
    
    if result.status == "success":
        print("✓ Success!")
    else:
        print(f"✗ Failed: {result.error}")
        
except Exception as e:
    print(f"✗ Exception: {e}")
```

---

## Performance Monitoring

```python
# Get stats for a flow
stats = pad.get_performance_stats("MyFlow")

print(f"Executions: {stats['execution_count']}")
print(f"Avg Time: {stats['avg_duration']:.2f}s")
print(f"Memory: {stats['avg_memory_delta_mb']:.2f}MB")
```

---

## Logging

```python
# Access logger
pad.logger.info("Information message")
pad.logger.warning("Warning message")
pad.logger.error("Error message")

# Get logs
logs = pad.get_logs(
    flow_name="MyFlow",
    level="ERROR"
)
```

---

## File Locations

| Type | Location |
|------|----------|
| Flows | `flows/*.json` |
| Config | `configs/config.yaml` |
| Env vars | `.env` |
| Logs | `logs/*.log` |
| Data | `data/` |
| Examples | `examples/*.py` |
| Learning | `learning/*.py` |
| Docs | `docs/*.md` |

---

## Flow JSON Structure

```json
{
  "name": "MyFlow",
  "description": "What it does",
  "version": "1.0",
  "enabled": true,
  "variables": {
    "input": {
      "param1": {"type": "string", "default": ""}
    },
    "output": {
      "result": {"type": "string"}
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

---

## Command Line

```powershell
# Run main script
python main.py

# Run examples
python examples/basic_usage.py
python examples/advanced_usage.py

# Run learning lessons
python learning/lesson_1_3.py

# Run tests
pytest
pytest --cov=pad_framework

# Install as package
pip install -e .
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Flow not found | Check `flows/` folder, verify name |
| Timeout | Increase timeout parameter |
| Permission denied | Run as Administrator |
| Import error | Check Python version (3.8+) |

---

## Best Practices

✅ **DO**
- Validate flows before execution
- Use try-except for error handling
- Enable retry for critical flows
- Monitor performance regularly
- Keep secrets in .env
- Log important events

❌ **DON'T**
- Hardcode credentials
- Ignore error handling
- Skip validation
- Run untested flows in production
- Log sensitive data

---

## Quick Examples

### Execute with Timeout
```python
result = pad.execute_flow("SlowFlow", timeout=600)
```

### Execute with Retry
```python
result = pad.execute_flow("UnreliableFlow", retry_count=3)
```

### Create and Execute
```python
pad.create_flow("NewFlow")
pad.validate_flow("NewFlow")
result = pad.execute_flow("NewFlow", {})
```

### Schedule Daily
```python
schedule_id = pad.schedule_flow(
    "DailyReport",
    "0 9 * * *"
)
```

### Monitor Performance
```python
pad.execute_flow("MyFlow", {})
stats = pad.get_performance_stats("MyFlow")
if stats['avg_duration'] > 10:
    print("⚠ Flow is slow!")
```

---

## Learning Resources

| Resource | File |
|----------|------|
| Quick Start | `QUICKSTART.md` |
| User Manual | `USER_MANUAL.md` |
| Learning Path | `LEARNING_MODULE.md` |
| Exercises | `learning/EXERCISES.md` |
| API Docs | `docs/api_reference.md` |
| Best Practices | `docs/best_practices.md` |
| Features | `FEATURES.md` |

---

## Support

**Documentation**: Check `docs/` folder  
**Examples**: Look in `examples/` folder  
**Learning**: Start with `LEARNING_MODULE.md`  
**Issues**: Review `USER_MANUAL.md` troubleshooting

---

## Version Info

**Framework**: 1.0.0  
**Python Required**: 3.8+  
**Platform**: Windows  
**License**: MIT

---

**Print this page for quick reference!** 📄
