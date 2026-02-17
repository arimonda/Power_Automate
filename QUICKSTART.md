# Power Automate Desktop Framework - Quick Start

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Configure Environment

```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env with your settings (optional)
notepad .env
```

### Step 3: Run the Framework

```powershell
python main.py
```

You should see:
```
============================================================
Power Automate Desktop Framework
Version 1.0.0 - All Features Enabled
============================================================

Initializing framework...
✓ Framework initialized successfully

Framework Health Status:
----------------------------------------
  status: healthy
  version: 1.0.0
  flows_available: 1
  ...
```

## 📚 Your First Flow

### Create a New Flow

```python
from pad_framework import PADFramework

# Initialize framework
pad = PADFramework()

# Create a new flow
pad.create_flow("MyFirstFlow", template="basic")
```

### Execute a Flow

```python
# Execute the example flow
result = pad.execute_flow(
    flow_name="ExampleFlow",
    input_variables={
        "inputParam1": "Hello",
        "inputParam2": 42
    }
)

# Check the result
print(f"Status: {result.status}")
print(f"Duration: {result.duration}s")
print(f"Output: {result.output}")
```

### Validate a Flow

```python
# Validate before execution
validation = pad.validate_flow("MyFirstFlow")

if validation["valid"]:
    print("✓ Flow is valid!")
else:
    print(f"✗ Errors: {validation['errors']}")
```

## 🎯 Common Tasks

### List All Flows
```python
flows = pad.list_flows()
for flow in flows:
    print(f"  • {flow}")
```

### Schedule a Flow
```python
schedule_id = pad.schedule_flow(
    flow_name="DailyReport",
    schedule="0 9 * * *",  # Daily at 9 AM
    input_variables={"email": "user@example.com"}
)
```

### Monitor Performance
```python
stats = pad.get_performance_stats("MyFlow")
print(f"Average duration: {stats['avg_duration']:.2f}s")
print(f"Executions: {stats['execution_count']}")
```

### Check Framework Health
```python
health = pad.get_health_status()
print(f"Status: {health['status']}")
print(f"Available flows: {health['flows_available']}")
```

## 🔧 Configuration

Edit `configs/config.yaml` to customize:

```yaml
execution:
  default_timeout: 300
  max_concurrent_flows: 5
  retry_enabled: true
  default_retry_count: 3

logging:
  level: "INFO"
  console_output: true
  file_output: true

performance:
  monitoring_enabled: true
  collect_metrics: true
```

## 📖 Examples

Check the `examples/` folder:
- `basic_usage.py` - Common operations
- `advanced_usage.py` - Advanced patterns

Run examples:
```powershell
python examples/basic_usage.py
python examples/advanced_usage.py
```

## ✨ All Features Available

✓ Flow Execution & Management
✓ Performance Monitoring
✓ Comprehensive Logging
✓ Testing Framework
✓ Retry & Error Handling
✓ Flow Scheduling
✓ Database Integration
✓ Email Integration
✓ API Integration
✓ Web Automation
✓ File Operations
✓ Credential Management
✓ Notification System
✓ Health Monitoring

## 📚 Documentation

- **Getting Started**: `docs/getting_started.md`
- **API Reference**: `docs/api_reference.md`
- **Best Practices**: `docs/best_practices.md`

## 🐛 Troubleshooting

### ImportError
```powershell
pip install -r requirements.txt
```

### Flow Not Found
- Check that flow exists in `flows/` directory
- Verify flow name matches filename (without .json)

### Permission Errors
- Run PowerShell as Administrator
- Check file system permissions

## 🎉 Next Steps

1. Create your first custom flow
2. Explore the examples
3. Read the documentation
4. Configure integrations
5. Set up monitoring

## 💡 Tips

- Start with the example flow as a template
- Use validation before executing flows
- Enable performance monitoring
- Check logs in `logs/` folder
- Monitor execution with `get_performance_stats()`

## 🆘 Need Help?

- Check documentation in `docs/`
- Review examples in `examples/`
- Check the API reference
- Review configuration in `configs/`

---

**Framework Version**: 1.0.0  
**Python Required**: 3.8+  
**Platform**: Windows (Power Automate Desktop required)
