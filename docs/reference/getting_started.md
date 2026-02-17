# Getting Started with PAD Framework

Welcome to the Power Automate Desktop Framework! This guide will help you get started quickly.

## Installation

1. **Install Python** (3.8 or higher)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Initialize Framework**
   ```bash
   python -c "from pad_framework import PADFramework; PADFramework()"
   ```

## Quick Start

### 1. Initialize the Framework

```python
from pad_framework import PADFramework

# Create framework instance
pad = PADFramework()
```

### 2. List Available Flows

```python
flows = pad.list_flows()
print(f"Available flows: {flows}")
```

### 3. Execute a Flow

```python
result = pad.execute_flow(
    flow_name="MyFlow",
    input_variables={"param1": "value1"}
)

print(f"Status: {result.status}")
print(f"Duration: {result.duration}s")
```

### 4. Create a New Flow

```python
pad.create_flow(
    flow_name="MyNewFlow",
    template="basic"
)
```

## Basic Concepts

### Flows
Flows are Power Automate Desktop automation sequences stored as JSON files in the `flows/` directory.

### Execution
The framework executes flows using the PAD Console Host, tracks performance, and provides detailed results.

### Configuration
All framework settings are in `configs/config.yaml`. Override with environment variables in `.env`.

### Logging
Logs are stored in `logs/` directory with automatic rotation. Configure logging level in config.

## Next Steps

- Read [Flow Development Guide](flow_development.md)
- Explore [Examples](../examples/)
- Check [API Reference](api_reference.md)
- Learn [Best Practices](best_practices.md)

## Common Operations

### Execute with Retry
```python
result = pad.execute_flow(
    flow_name="MyFlow",
    retry_count=3
)
```

### Schedule a Flow
```python
schedule_id = pad.schedule_flow(
    flow_name="DailyReport",
    schedule="0 9 * * *"
)
```

### Monitor Performance
```python
stats = pad.get_performance_stats("MyFlow")
print(f"Average duration: {stats['avg_duration']}s")
```

### Check Health
```python
health = pad.get_health_status()
print(health)
```

## Troubleshooting

### Flow Not Found
- Check flow exists in `flows/` directory
- Verify flow name matches file name (without .json)

### Execution Timeout
- Increase timeout parameter
- Check PAD Console Host is installed
- Review flow complexity

### Permission Errors
- Run as administrator if needed
- Check file system permissions
- Verify PAD installation

## Support

- Documentation: `docs/` folder
- Examples: `examples/` folder
- Issues: Create an issue in the repository
