# API Reference

Complete API documentation for the PAD Framework.

## PADFramework

Main framework class providing unified interface.

### Methods

#### `__init__(config_path: Optional[str] = None)`
Initialize the framework.

**Parameters:**
- `config_path`: Optional path to configuration file

**Example:**
```python
pad = PADFramework()
# or with custom config
pad = PADFramework("path/to/config.yaml")
```

#### `execute_flow(flow_name, input_variables, timeout, retry_count) -> FlowExecutionResult`
Execute a Power Automate Desktop flow.

**Parameters:**
- `flow_name` (str): Name of the flow to execute
- `input_variables` (dict, optional): Input variables for the flow
- `timeout` (int, optional): Execution timeout in seconds
- `retry_count` (int, optional): Number of retry attempts

**Returns:**
- `FlowExecutionResult`: Execution result object

**Example:**
```python
result = pad.execute_flow(
    flow_name="DataProcessor",
    input_variables={"file": "data.xlsx"},
    timeout=120,
    retry_count=2
)
```

#### `list_flows(search_pattern: Optional[str] = None) -> List[str]`
List available flows.

**Parameters:**
- `search_pattern` (str, optional): Pattern to filter flows

**Returns:**
- `List[str]`: List of flow names

**Example:**
```python
all_flows = pad.list_flows()
test_flows = pad.list_flows(search_pattern="test")
```

#### `validate_flow(flow_name: str) -> Dict[str, Any]`
Validate a flow configuration.

**Parameters:**
- `flow_name` (str): Name of the flow to validate

**Returns:**
- `Dict[str, Any]`: Validation results with keys: valid, errors, warnings, info

**Example:**
```python
validation = pad.validate_flow("MyFlow")
if validation["valid"]:
    print("Flow is valid!")
else:
    print(f"Errors: {validation['errors']}")
```

#### `create_flow(flow_name: str, template: Optional[str] = None) -> bool`
Create a new flow.

**Parameters:**
- `flow_name` (str): Name for the new flow
- `template` (str, optional): Template name to use

**Returns:**
- `bool`: Success status

**Example:**
```python
pad.create_flow("NewFlow", template="basic")
```

#### `schedule_flow(flow_name, schedule, input_variables) -> str`
Schedule a flow execution.

**Parameters:**
- `flow_name` (str): Name of the flow to schedule
- `schedule` (str): Schedule expression (cron-like)
- `input_variables` (dict, optional): Input variables

**Returns:**
- `str`: Schedule ID

**Example:**
```python
schedule_id = pad.schedule_flow(
    flow_name="DailyReport",
    schedule="0 9 * * *",  # Daily at 9 AM
    input_variables={"email": "user@example.com"}
)
```

#### `get_performance_stats(flow_name: Optional[str] = None) -> Dict[str, Any]`
Get performance statistics.

**Parameters:**
- `flow_name` (str, optional): Flow name to filter stats

**Returns:**
- `Dict[str, Any]`: Performance statistics

**Example:**
```python
stats = pad.get_performance_stats("MyFlow")
print(f"Average duration: {stats['avg_duration']}s")
print(f"Max memory: {stats['max_memory_delta_mb']}MB")
```

#### `get_health_status() -> Dict[str, Any]`
Get framework health status.

**Returns:**
- `Dict[str, Any]`: Health information

**Example:**
```python
health = pad.get_health_status()
print(f"Status: {health['status']}")
print(f"Active schedules: {health['active_schedules']}")
```

#### `integrate(service: str, **kwargs) -> Any`
Integrate with external services.

**Parameters:**
- `service` (str): Service name (email, database, api, web, file, notification)
- `**kwargs`: Service-specific parameters

**Returns:**
- `Any`: Integration result

**Example:**
```python
# Email integration
email = pad.integrate("email", smtp_server="smtp.gmail.com")

# API integration
api = pad.integrate("api", endpoint="https://api.example.com")
```

## FlowExecutionResult

Result object from flow execution.

### Properties

- `flow_name` (str): Name of the executed flow
- `status` (str): Execution status (success, failed, timeout, cancelled)
- `start_time` (datetime): Execution start time
- `end_time` (datetime): Execution end time
- `duration` (float): Execution duration in seconds
- `output` (dict): Flow output variables
- `error` (str, optional): Error message if failed
- `execution_id` (str): Unique execution identifier

## Config

Configuration management class.

### Methods

#### `get(key: str, default: Any = None) -> Any`
Get configuration value.

**Example:**
```python
config = Config()
log_level = config.get("logging.level", "INFO")
```

#### `set(key: str, value: Any) -> None`
Set configuration value.

**Example:**
```python
config.set("execution.default_timeout", 600)
```

#### `get_path(path_type: str) -> Path`
Get full path for a path type.

**Example:**
```python
flows_path = config.get_path("flows")
```

## FlowConfig

Data class for flow configuration.

### Properties

- `name` (str): Flow name
- `description` (str): Flow description
- `timeout` (int): Execution timeout in seconds
- `retry_count` (int): Number of retry attempts
- `retry_delay` (int): Delay between retries in seconds
- `input_variables` (dict): Input variables
- `output_variables` (dict): Output variables
- `enabled` (bool): Whether flow is enabled
- `priority` (int): Execution priority (1-10)
- `tags` (list): Flow tags

## Exceptions

### PADException
Base exception for all framework exceptions.

### FlowExecutionError
Raised when flow execution fails.

### FlowNotFoundError
Raised when flow is not found.

### ConfigurationError
Raised when configuration is invalid.

### ValidationError
Raised when validation fails.

### TimeoutError
Raised when operation times out.

### RetryExhaustedError
Raised when retry attempts are exhausted.

### IntegrationError
Raised when integration fails.

## Example: Complete Workflow

```python
from pad_framework import PADFramework

# Initialize
pad = PADFramework()

# Check health
health = pad.get_health_status()
assert health["status"] == "healthy"

# List flows
flows = pad.list_flows()
print(f"Available: {len(flows)} flows")

# Validate flow
validation = pad.validate_flow("DataProcessor")
if not validation["valid"]:
    print("Flow has errors!")
    exit(1)

# Execute flow
result = pad.execute_flow(
    flow_name="DataProcessor",
    input_variables={"source": "data.xlsx"},
    timeout=300,
    retry_count=2
)

# Check result
if result.status == "success":
    print(f"Success in {result.duration:.2f}s")
    print(f"Output: {result.output}")
else:
    print(f"Failed: {result.error}")

# Get stats
stats = pad.get_performance_stats("DataProcessor")
print(f"Average duration: {stats['avg_duration']:.2f}s")

# Cleanup
pad.cleanup()
```
