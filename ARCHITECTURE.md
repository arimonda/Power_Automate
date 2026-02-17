# PAD Framework — Architectural Document

**Project**: Power Automate Desktop (PAD) Automation Framework  
**Version**: 1.0.0  
**Date**: February 17, 2026  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Module Decomposition](#4-module-decomposition)
5. [Core Module](#5-core-module)
6. [Flows Module](#6-flows-module)
7. [Monitoring Module](#7-monitoring-module)
8. [Testing Module](#8-testing-module)
9. [Reporting Module](#9-reporting-module)
10. [Integrations Module](#10-integrations-module)
11. [CLI Layer](#11-cli-layer)
12. [Utilities Module](#12-utilities-module)
13. [Configuration Architecture](#13-configuration-architecture)
14. [Error Handling Architecture](#14-error-handling-architecture)
15. [Data Flow Diagrams](#15-data-flow-diagrams)
16. [Design Patterns](#16-design-patterns)
17. [Security Architecture](#17-security-architecture)
18. [Dependency Map](#18-dependency-map)
19. [Directory Structure](#19-directory-structure)
20. [Technology Stack](#20-technology-stack)
21. [Deployment & Packaging](#21-deployment--packaging)
22. [Testing Strategy](#22-testing-strategy)
23. [Extension Points](#23-extension-points)
24. [Glossary](#24-glossary)

---

## 1. Executive Summary

The **PAD Framework** is a Python-based automation framework built to orchestrate, manage, monitor, and test **Microsoft Power Automate Desktop** flows. It provides a unified programmatic and CLI interface to perform CRUD operations on flows, execute them synchronously or asynchronously (including batch, pipeline, and DAG-based dependency execution), collect performance metrics, run automated tests with an assertion framework, generate multi-format reports, and integrate with external services.

The framework follows a **modular, layered architecture** with clear separation of concerns, making it extensible, testable, and maintainable.

---

## 2. System Overview

### Purpose

The framework wraps the Power Automate Desktop CLI (`PAD.Console.Host.exe`) to provide:

- **Flow Lifecycle Management** — Create, validate, import, export, delete flows
- **Flow Execution** — Synchronous and async execution with retries, timeouts, and scheduling
- **Performance Monitoring** — Runtime metrics collection with Prometheus compatibility
- **Automated Testing** — Built-in test runner and assertion framework
- **Report Generation** — Multi-format (HTML, JSON, Markdown, Text) reports
- **Integration Management** — Email, database, API, and web automation integrations
- **CLI Interface** — Full-featured command-line interface via `click`

### Target Platform

- **OS**: Windows (required for Power Automate Desktop)
- **Runtime**: Python 3.8+
- **PAD Dependency**: `C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe`

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER / OPERATOR                              │
│              (CLI Commands / Python API / Scripts)                   │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
         ┌────────────▼────────────┐
         │       CLI Layer         │  ← click-based CLI (pad_framework/cli.py)
         │   (10 Commands)         │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │    PADFramework         │  ← Facade (pad_framework/core/framework.py)
         │   (Central Orchestrator)│
         └────┬───┬───┬───┬───┬───┘
              │   │   │   │   │
    ┌─────────┘   │   │   │   └─────────────┐
    │         ┌───┘   │   └───┐             │
    ▼         ▼       ▼       ▼             ▼
┌────────┐┌────────┐┌──────┐┌───────────┐┌────────────┐
│  Flow  ││  Flow  ││Test  ││Performance││Integration │
│Manager ││Executor││Runner││  Monitor  ││  Manager   │
└────────┘└───┬────┘└──────┘└───────────┘└────────────┘
              │
         ┌────▼────┐
         │  Async  │
         │Executor │
         └─────────┘
              │
    ┌─────────▼──────────┐
    │  PAD.Console.Host  │  ← Windows PAD CLI (subprocess)
    │    (External)      │
    └────────────────────┘
```

### Architectural Style

The framework uses a **Layered Architecture** combined with a **Facade Pattern** at the core:

| Layer | Responsibility |
|-------|---------------|
| **Presentation** | CLI commands, console output, color formatting |
| **Application** | `PADFramework` facade, orchestration logic |
| **Domain** | Flow management, execution, monitoring, testing, reporting |
| **Infrastructure** | File I/O, subprocess calls, logging, configuration |

---

## 4. Module Decomposition

```
pad_framework/
├── __init__.py              ← Public API exports
├── cli.py                   ← CLI interface (Presentation Layer)
├── core/                    ← Core framework components
│   ├── __init__.py
│   ├── framework.py         ← PADFramework facade class
│   ├── config.py            ← Configuration management
│   ├── exceptions.py        ← Base exception hierarchy
│   ├── error_codes.py       ← Structured error codes & severity
│   └── validation.py        ← Pydantic validation & sanitization
├── flows/                   ← Flow management & execution
│   ├── __init__.py
│   ├── flow_manager.py      ← Flow CRUD operations
│   ├── flow_executor.py     ← Synchronous flow execution
│   └── async_executor.py    ← Async/concurrent execution
├── monitoring/              ← Performance monitoring
│   ├── __init__.py
│   ├── performance_monitor.py ← Runtime metrics tracking
│   └── metrics.py           ← Prometheus-compatible metrics
├── testing/                 ← Testing framework
│   ├── __init__.py
│   ├── test_runner.py       ← Pytest-based test runner
│   └── assertions.py        ← Assertion framework with severity
├── reporting/               ← Report generation
│   ├── __init__.py
│   └── report_generator.py  ← Multi-format report generator
├── integrations/            ← External service integrations
│   ├── __init__.py
│   └── integration_manager.py ← Integration registry & execution
└── utils/                   ← Shared utilities
    ├── __init__.py
    ├── logger.py            ← Loguru-based logging
    └── helpers.py           ← File I/O, formatting, validation helpers
```

---

## 5. Core Module

### 5.1 PADFramework (`core/framework.py`)

The central **Facade** class that provides a unified interface to all subsystems.

#### Initialization Sequence

```
PADFramework.__init__(config_path)
    │
    ├── 1. Config(config_path)         → Load configuration
    ├── 2. Logger(config)              → Initialize logging
    ├── 3. FlowManager(config, logger) → Flow CRUD
    ├── 4. FlowExecutor(config, logger)→ Flow execution
    ├── 5. TestRunner(config, logger)  → Testing
    ├── 6. PerformanceMonitor(config, logger) → Monitoring
    └── 7. IntegrationManager(config, logger) → Integrations
```

#### Public API

| Method | Returns | Description |
|--------|---------|-------------|
| `execute_flow(flow_name, input_variables, timeout, retry_count)` | `FlowExecutionResult` | Execute a flow with options |
| `list_flows(search_pattern)` | `List[str]` | List available flows |
| `validate_flow(flow_name)` | `Dict[str, Any]` | Validate flow definition |
| `create_flow(flow_name, template)` | `bool` | Create a new flow |
| `export_flow(flow_name, output_path)` | `bool` | Export flow to file |
| `import_flow(flow_path, flow_name)` | `bool` | Import flow from file |
| `run_tests(test_pattern, verbose)` | `Dict[str, Any]` | Run automated tests |
| `get_performance_stats(flow_name)` | `Dict[str, Any]` | Get performance stats |
| `schedule_flow(flow_name, schedule, input_variables)` | `str` | Schedule flow (returns schedule_id) |
| `cancel_schedule(schedule_id)` | `bool` | Cancel a scheduled flow |
| `get_logs(flow_name, start_time, end_time, level)` | `List[Dict]` | Retrieve filtered logs |
| `integrate(service, **kwargs)` | `Any` | Execute integration |
| `get_health_status()` | `Dict[str, Any]` | System health check |
| `cleanup()` | `None` | Release resources |

### 5.2 Config (`core/config.py`)

Centralized configuration management with a three-tier precedence model.

#### Configuration Precedence (highest → lowest)

```
┌──────────────────────────┐
│  Environment Variables   │  ← PAD_* prefix (highest priority)
│  (PAD_DEBUG, PAD_LOG_*)  │
├──────────────────────────┤
│  YAML Configuration      │  ← configs/config.yaml
│  (File-based settings)   │
├──────────────────────────┤
│  Default Configuration   │  ← Config.DEFAULT_CONFIG (lowest priority)
│  (Hardcoded defaults)    │
└──────────────────────────┘
```

#### Configuration Domains

| Domain | Keys | Description |
|--------|------|-------------|
| `framework` | `name`, `version`, `debug` | Framework metadata |
| `paths` | `flows`, `logs`, `data`, `configs`, `tests` | Directory paths |
| `logging` | `level`, `format`, `file_size`, `backup_count` | Log configuration |
| `execution` | `timeout`, `max_concurrent`, `retry_count`, `retry_delay` | Execution defaults |
| `performance` | `monitoring_enabled`, `slow_threshold`, `memory_threshold` | Monitoring thresholds |
| `database` | Connection strings for SQL Server, MongoDB, Redis | DB configuration |
| `email` | SMTP settings | Email integration |
| `security` | `encryption_key`, `api_key_rotation` | Security settings |
| `integrations` | `web_automation`, `api`, `file_operations` | Integration toggles |
| `testing` | `coverage_threshold`, `parallel` | Test settings |
| `scheduling` | `enabled`, `max_concurrent` | Schedule settings |

#### Key Methods

| Method | Description |
|--------|-------------|
| `get(key, default)` | Dot-notation access (e.g., `config.get('logging.level')`) |
| `set(key, value)` | Dynamic configuration update |
| `get_path(path_type)` | Resolved `Path` object for a path type |
| `load_from_file(path)` | Load YAML configuration |
| `load_from_env()` | Load environment variable overrides |
| `save(file_path)` | Persist configuration to YAML |
| `create_directories()` | Ensure all configured directories exist |

### 5.3 Exceptions (`core/exceptions.py`)

Base exception hierarchy for the framework.

```
PADException (base)
├── FlowExecutionError
├── FlowNotFoundError
├── ConfigurationError
├── ValidationError
├── TimeoutError
├── RetryExhaustedError
├── IntegrationError
├── DatabaseError
├── AuthenticationError
└── PermissionError
```

### 5.4 Error Codes (`core/error_codes.py`)

Structured error system with codes, severity, and context.

#### Error Code Categories

| Range | Category | Examples |
|-------|----------|---------|
| E0xx | General | `E001` Unknown, `E002` Internal |
| E1xx | Configuration | `E101` Missing config, `E102` Invalid value |
| E2xx | Validation | `E201` Invalid input, `E202` Missing field |
| E3xx | Flow | `E301` Not found, `E302` Invalid definition |
| E4xx | Execution | `E401` Failed, `E402` Timeout |
| E5xx | Permission | `E501` Access denied |
| E6xx | Resource | `E601` Not available, `E602` Limit exceeded |
| E7xx | Integration | `E701` Connection failed |
| E8xx | Security | `E801` Auth failed |
| E9xx | Schedule | `E901` Invalid schedule |

#### PADError Class

```python
class PADError(Exception):
    code: ErrorCode           # Categorized error code
    message: str              # Human-readable message
    context: Dict[str, Any]   # Additional context data
    severity: ErrorSeverity   # LOW, MEDIUM, HIGH, CRITICAL
    original_exception: Exception  # Wrapped original exception
    timestamp: datetime       # When the error occurred
    traceback_str: str        # Stack trace
```

### 5.5 Validation (`core/validation.py`)

Pydantic-based validation models and security sanitizers.

#### Pydantic Models

| Model | Purpose | Key Validators |
|-------|---------|---------------|
| `FlowExecutionRequest` | Validate execution inputs | Flow name format, input variable types |
| `FlowCreationRequest` | Validate flow creation | Reserved names check, name format |
| `ScheduleRequest` | Validate scheduling | Cron expression validation |
| `ConfigUpdateRequest` | Validate config updates | Key format validation |

#### Security Validators

| Class | Purpose |
|-------|---------|
| `PathValidator` | Prevent path traversal attacks |
| `CommandValidator` | Prevent command injection |
| `InputSanitizer` | Sanitize strings and nested dicts |

---

## 6. Flows Module

### 6.1 FlowManager (`flows/flow_manager.py`)

Manages the lifecycle of flow definitions stored as JSON files.

#### Responsibilities

- **CRUD**: Create, read, list, delete flow files
- **Validation**: Structural validation of flow JSON (required fields, schema)
- **Import/Export**: Move flows between environments
- **Templating**: Create flows from predefined templates

#### Flow Storage

Flows are stored as individual JSON files in the configured `flows/` directory:

```
flows/
├── example_flow.json
├── data_extraction.json
└── report_generation.json
```

#### Flow JSON Schema

```json
{
  "name": "string",                    // Required
  "description": "string",
  "version": "string",                 // Required
  "enabled": true,
  "variables": {
    "input": {
      "variableName": {
        "type": "string|number|boolean",
        "default": "value",
        "description": "string"
      }
    },
    "output": {
      "variableName": {
        "type": "string",
        "description": "string"
      }
    }
  },
  "actions": [                         // Required
    {
      "id": "action_1",
      "type": "DisplayMessage|SetVariable|...",
      "parameters": { }
    }
  ],
  "error_handling": {
    "on_error": "stop|continue|retry",
    "retry_count": 3,
    "retry_delay": 5
  },
  "settings": {
    "timeout": 300,
    "priority": 1,
    "run_mode": "attended|unattended"
  },
  "metadata": {
    "created_by": "string",
    "created_at": "ISO8601",
    "tags": ["string"]
  }
}
```

### 6.2 FlowExecutor (`flows/flow_executor.py`)

Synchronous flow execution engine that interfaces with the PAD CLI.

#### Execution Flow

```
execute(flow_name, input_variables, timeout, retry_count)
    │
    ├── 1. Generate execution_id
    ├── 2. Record start_time
    ├── 3. Build CLI command
    │       └── PAD.Console.Host.exe /flow:{name} /input:{vars}
    ├── 4. Execute subprocess with timeout
    │       ├── Success → parse stdout
    │       ├── Timeout → TimeoutError
    │       └── Failure → check retry
    │               ├── Retries remaining → retry with delay
    │               └── No retries → FlowExecutionError
    ├── 5. Record end_time, duration
    └── 6. Return FlowExecutionResult
```

#### FlowExecutionResult

```python
@dataclass
class FlowExecutionResult:
    flow_name: str          # Name of executed flow
    status: str             # success | failed | timeout | cancelled
    start_time: datetime    # Execution start
    end_time: datetime      # Execution end
    duration: float         # Duration in seconds
    output: Dict[str, Any]  # Flow output variables
    error: Optional[str]    # Error message if failed
    execution_id: str       # Unique execution identifier
```

### 6.3 AsyncFlowExecutor (`flows/async_executor.py`)

Async wrapper providing concurrent execution capabilities.

#### Concurrency Model

```
AsyncFlowExecutor
    │
    ├── ThreadPoolExecutor(max_workers=5)   ← Thread pool for blocking calls
    ├── asyncio.Semaphore(max_concurrent=10) ← Concurrency limiter
    │
    └── execute_async()
         ├── Acquire semaphore
         ├── Run FlowExecutor.execute() in thread pool
         ├── Release semaphore
         └── Call optional callback (sync or async)
```

#### Execution Patterns

| Pattern | Method | Description |
|---------|--------|-------------|
| **Single Async** | `execute_async()` | Single flow, async with callback |
| **Batch Parallel** | `execute_batch()` | Multiple flows in parallel, optional fail-fast |
| **Pipeline** | `execute_pipeline()` | Sequential with output chaining |
| **DAG Dependencies** | `execute_with_dependencies()` | Dependency-graph execution |
| **Parallel Helper** | `execute_flows_parallel()` | Convenience for parallel execution |
| **Sequential Helper** | `execute_flows_sequential()` | Convenience for sequential execution |

#### DAG Execution

The `execute_with_dependencies()` method accepts a flow graph where each node declares its dependencies:

```python
flow_graph = {
    "extract": {"flow_name": "extract_data", "depends_on": []},
    "transform": {"flow_name": "transform_data", "depends_on": ["extract"]},
    "validate": {"flow_name": "validate_data", "depends_on": ["transform"]},
    "load": {"flow_name": "load_data", "depends_on": ["validate"]},
}
```

The executor resolves the dependency order and runs flows with satisfied dependencies in parallel.

---

## 7. Monitoring Module

### 7.1 PerformanceMonitor (`monitoring/performance_monitor.py`)

Runtime performance tracking using system metrics.

#### Tracking Mechanism

Uses a **context manager** pattern:

```python
with performance_monitor.track("my_flow"):
    # Flow execution happens here
    # Captures: duration, memory delta, CPU usage
```

#### Metrics Captured Per Execution

| Metric | Source | Unit |
|--------|--------|------|
| Duration | `time.time()` delta | Seconds |
| Memory Usage | `psutil.Process().memory_info()` | Megabytes |
| Memory Delta | Start vs. end memory | Megabytes |
| CPU Percent | `psutil.cpu_percent()` | Percentage |
| Timestamp | `datetime.now()` | ISO 8601 |

#### Alert Thresholds

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Slow execution | > 60 seconds | Log warning |
| High memory | > 100 MB delta | Log warning |

#### Statistics API

```python
get_stats(flow_name) → {
    "execution_count": int,
    "avg_duration": float,
    "min_duration": float,
    "max_duration": float,
    "avg_memory_delta": float,
    "max_memory_delta": float,
    "last_execution": str  # ISO timestamp
}

get_summary() → {
    "total_flows_tracked": int,
    "total_executions": int,
    "system_cpu_percent": float,
    "system_memory_percent": float,
    "disk_usage_percent": float
}
```

### 7.2 MetricsCollector (`monitoring/metrics.py`)

Prometheus-compatible metrics for external monitoring systems.

#### Metric Categories

| Category | Metric Name | Type | Labels |
|----------|------------|------|--------|
| **Execution** | `pad_flow_executions_total` | Counter | `flow_name`, `status` |
| | `pad_flow_execution_duration_seconds` | Histogram | `flow_name` |
| | `pad_flow_execution_errors_total` | Counter | `flow_name`, `error_type` |
| | `pad_active_flow_executions` | Gauge | — |
| **Management** | `pad_flows_registered_total` | Gauge | — |
| | `pad_flow_validation_failures_total` | Counter | `flow_name` |
| **Scheduling** | `pad_schedules_active` | Gauge | — |
| | `pad_schedule_executions_total` | Counter | `flow_name`, `status` |
| **Resources** | `pad_memory_usage_bytes` | Gauge | `type` |
| | `pad_cpu_usage_percent` | Gauge | — |
| **Integrations** | `pad_integration_calls_total` | Counter | `integration`, `operation`, `status` |
| | `pad_integration_duration_seconds` | Histogram | `integration` |
| **Reliability** | `pad_retry_attempts_total` | Counter | `flow_name` |
| | `pad_timeout_occurrences_total` | Counter | `flow_name` |
| **Framework** | `pad_framework_uptime_seconds` | Gauge | — |
| | `pad_framework_info` | Gauge | `version`, `python_version` |

#### MetricsMiddleware

Automatic metrics collection middleware:

```python
context = middleware.before_execution("my_flow")
# ... execution ...
middleware.after_execution(context, status="success")
```

#### Singleton Access

```python
collector = get_metrics_collector()  # Returns singleton instance
metrics_bytes = collector.export_metrics()  # Prometheus format
```

---

## 8. Testing Module

### 8.1 TestRunner (`testing/test_runner.py`)

Pytest-based test execution with coverage reporting.

#### Capabilities

- Run all tests or filter by pattern
- Generate coverage reports (terminal + HTML)
- Run flow-specific tests (`test_{flow_name}`)
- Returns structured results with exit codes

#### API

```python
runner.run(test_pattern=None, verbose=False) → {
    "success": bool,
    "exit_code": int,
    "message": str
}

runner.run_flow_test(flow_name) → Dict[str, Any]
```

### 8.2 Assertions (`testing/assertions.py`)

Comprehensive assertion framework with severity levels and suite management.

#### Severity Levels

| Level | Use Case |
|-------|----------|
| `CRITICAL` | Must-pass assertions; failure indicates a severe issue |
| `ERROR` | Important assertions; failure is a significant problem |
| `WARNING` | Advisory assertions; failure is a concern |
| `INFO` | Informational assertions; failure is notable but not urgent |

#### Assertion Categories

**Basic Assertions**:
- `assert_true(condition)`, `assert_false(condition)`
- `assert_equal(actual, expected)`, `assert_not_equal(actual, expected)`
- `assert_is_none(value)`, `assert_is_not_none(value)`

**Comparison Assertions**:
- `assert_greater(actual, threshold)`
- `assert_less(actual, threshold)`
- `assert_in_range(value, min, max)`

**Collection Assertions**:
- `assert_contains(collection, item)`, `assert_not_contains(collection, item)`
- `assert_length(collection, expected_length)`
- `assert_empty(collection)`, `assert_not_empty(collection)`

**String Assertions**:
- `assert_starts_with(string, prefix)`
- `assert_ends_with(string, suffix)`
- `assert_matches_pattern(string, regex)`

**Type Assertions**:
- `assert_type(value, expected_type)`

**Flow-Specific Assertions**:
- `assert_flow_success(result)`, `assert_flow_failed(result)`
- `assert_duration_within(result, max_duration)`
- `assert_output_contains(result, key)`
- `assert_no_error(result)`

**Custom Assertions**:
- `assert_custom(condition_func, name, message)`

#### Suite Management

```python
assertions = Assertions("My Test Suite")

# Run assertions...
assertions.assert_true(condition, "Check something")

# Complete and inspect
suite = assertions.complete()
print(suite.success_rate)       # e.g., 95.0
print(suite.failed_assertions)  # count of failures
failures = suite.get_failures() # list of failed AssertionResult
```

#### AssertionResult

```python
@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str
    severity: AssertionSeverity
    expected: Any
    actual: Any
    timestamp: datetime
```

#### AssertionSuite

```python
@dataclass
class AssertionSuite:
    name: str
    results: List[AssertionResult]
    start_time: datetime
    end_time: Optional[datetime]

    # Properties
    passed: bool              # All assertions passed
    total_assertions: int
    passed_assertions: int
    failed_assertions: int
    success_rate: float       # Percentage

    # Methods
    add_result(result)
    complete()
    get_failures() → List[AssertionResult]
    get_by_severity(severity) → List[AssertionResult]
    summary() → Dict[str, Any]
```

---

## 9. Reporting Module

### 9.1 ReportGenerator (`reporting/report_generator.py`)

Multi-format report generation engine.

#### Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| `HTML` | `.html` | Rich visual reports with CSS styling |
| `JSON` | `.json` | Machine-readable, API consumption |
| `MARKDOWN` | `.md` | Documentation, Git-friendly |
| `TEXT` | `.txt` | Plain text, terminal-friendly |
| `CSV` | `.csv` | Spreadsheet import (defined, not fully implemented) |
| `PDF` | `.pdf` | Print-ready (defined, not fully implemented) |

#### Report Types

| Type | Data Class | Content |
|------|-----------|---------|
| **Execution** | `ExecutionReport` | Flow name, status, duration, I/O, errors, retries |
| **Validation** | `ValidationReport` | Checks performed/passed/failed, errors, warnings, info, success rate |
| **Performance** | `PerformanceReport` | Execution counts, duration percentiles (p50/p95/p99), memory, CPU, error rate |
| **Summary** | `List[Dict]` | Multi-flow overview table |

#### Data Classes

```python
@dataclass
class ExecutionReport:
    flow_name: str
    execution_id: str
    status: str
    start_time: datetime
    end_time: datetime
    duration: float
    input_variables: Dict
    output: Dict
    error: Optional[str]
    retry_attempts: int
    warnings: List[str]

@dataclass
class ValidationReport:
    flow_name: str
    timestamp: datetime
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    checks_performed: int
    checks_passed: int
    checks_failed: int
    # Property: success_rate

@dataclass
class PerformanceReport:
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
    # Property: success_rate
```

#### Generation Pipeline

```
Report Data (dataclass) → Format Selection → Template Rendering → File Output
                                                                       │
                                              ┌────────────────────────┤
                                              ▼                        ▼
                                    reports/ directory          Return file path
```

---

## 10. Integrations Module

### 10.1 IntegrationManager (`integrations/integration_manager.py`)

Registry-based integration management for external services.

#### Architecture

```
IntegrationManager
    │
    ├── register_integration(name, class)  → Register integration
    ├── get_integration(name)              → Retrieve instance
    ├── integrate(service, **kwargs)       → Execute integration
    ├── list_integrations()                → List registered
    └── test_integration(name)             → Test connectivity
```

#### Supported Integration Categories

| Category | Services | Configuration |
|----------|----------|--------------|
| **Email** | SMTP | `email.*` config keys |
| **Database** | SQL Server, MongoDB, Redis | `database.*` config keys |
| **API** | REST APIs | `integrations.api.*` config keys |
| **Web Automation** | Selenium-based | `integrations.web_automation.*` config keys |
| **File Operations** | File system | `integrations.file_operations.*` config keys |

---

## 11. CLI Layer

### 11.1 CLI Interface (`cli.py`)

Built with `click`, the CLI provides 10 commands for framework operations.

#### Command Reference

| Command | Arguments | Options | Description |
|---------|-----------|---------|-------------|
| `pad health` | — | — | Show framework health status |
| `pad list` | — | `--search`, `--json` | List available flows |
| `pad execute` | `FLOW_NAME` | `--input`, `--timeout`, `--retry`, `--json` | Execute a flow |
| `pad create` | `FLOW_NAME` | `--template` | Create a new flow |
| `pad validate` | `FLOW_NAME` | `--json` | Validate flow definition |
| `pad schedule` | `FLOW_NAME`, `SCHEDULE` | `--input` | Schedule flow execution |
| `pad stats` | `[FLOW_NAME]` | `--json` | Performance statistics |
| `pad logs` | — | `--level`, `--flow`, `--lines` | View framework logs |
| `pad config` | — | — | Show current configuration |
| `pad test` | — | `--pattern`, `--verbose` | Run automated tests |

#### Global Options

| Option | Description |
|--------|-------------|
| `--config PATH` | Custom configuration file path |
| `--verbose` | Enable verbose output |

#### Entry Points (from `setup.py`)

```
pad = pad_framework.cli:main
pad-framework = pad_framework.cli:main
```

#### Output Formatting

- Color-coded output using `click.style()` (green=success, red=error, yellow=warning, blue=info)
- Tabular data via `tabulate` library
- Optional JSON output for programmatic consumption

---

## 12. Utilities Module

### 12.1 Logger (`utils/logger.py`)

Centralized logging built on `loguru`.

#### Features

| Feature | Detail |
|---------|--------|
| Console Output | Colorized, configurable format |
| File Output | Rotated (size-based), compressed, configurable retention |
| In-Memory Buffer | Last 1,000 entries for `get_logs()` queries |
| Filtering | By flow name, time range, log level |
| Log Levels | DEBUG, INFO, WARNING, ERROR, CRITICAL |

#### API

```python
logger.debug(message, **kwargs)
logger.info(message, **kwargs)
logger.warning(message, **kwargs)
logger.error(message, **kwargs)
logger.critical(message, **kwargs)
logger.exception(message, **kwargs)  # Includes traceback
logger.get_logs(flow_name, start_time, end_time, level) → List[Dict]
```

### 12.2 Helpers (`utils/helpers.py`)

Shared utility functions used across all modules.

| Category | Functions |
|----------|----------|
| **File I/O** | `load_json()`, `save_json()`, `load_yaml()`, `save_yaml()` |
| **ID Generation** | `generate_id(prefix)` → timestamp-based unique ID |
| **Hashing** | `hash_string(text)` → SHA256 hash |
| **Directory** | `ensure_directory(path)` → create if missing |
| **Formatting** | `format_duration(seconds)`, `format_bytes(bytes)` |
| **Dict Operations** | `safe_get(dict, key_path)`, `merge_dicts(d1, d2)` |
| **Time** | `timestamp()` → ISO format |
| **Validation** | `parse_cron(expression)`, `validate_email(email)`, `sanitize_filename(name)` |

---

## 13. Configuration Architecture

### 13.1 Configuration Sources

```
┌─────────────────────────────────────────────────────────┐
│                 .env File (dotenv)                       │
│  PAD_DEBUG=true                                         │
│  PAD_LOG_LEVEL=DEBUG                                    │
│  PAD_DB_CONNECTION_STRING=...                           │
└───────────────────────┬─────────────────────────────────┘
                        │ load_from_env()
                        ▼
┌─────────────────────────────────────────────────────────┐
│              configs/config.yaml                         │
│  framework:                                              │
│    name: "PAD Framework"                                 │
│    version: "1.0.0"                                      │
│  logging:                                                │
│    level: "INFO"                                         │
└───────────────────────┬─────────────────────────────────┘
                        │ load_from_file()
                        ▼
┌─────────────────────────────────────────────────────────┐
│            Config.DEFAULT_CONFIG                         │
│  (Hardcoded Python dictionary with all defaults)         │
└─────────────────────────────────────────────────────────┘
```

### 13.2 Configuration Flow

```
1. Copy DEFAULT_CONFIG
2. Deep-merge YAML file (if exists)
3. Override with environment variables (PAD_* prefix)
4. Create required directories
5. Configuration ready for consumption
```

### 13.3 Access Pattern

All components receive the `Config` object during initialization and use dot-notation for nested access:

```python
config.get('logging.level')         # → "INFO"
config.get('execution.timeout')     # → 300
config.get_path('flows')            # → Path("./flows")
```

---

## 14. Error Handling Architecture

### 14.1 Multi-Layer Strategy

```
Layer 1: Input Validation (Pydantic)
    │  Catches invalid inputs before processing
    ▼
Layer 2: Security Sanitization
    │  PathValidator, CommandValidator, InputSanitizer
    ▼
Layer 3: Domain Exceptions (exceptions.py)
    │  PADException hierarchy for categorical handling
    ▼
Layer 4: Structured Errors (error_codes.py)
    │  PADError with codes, severity, context, traceback
    ▼
Layer 5: Error Handler Function
    │  handle_exception() → converts to PADError, logs
    ▼
Layer 6: Logging
       Logger captures all errors with context
```

### 14.2 Error Propagation

```
Subsystem Error
    → Caught by subsystem
    → Wrapped in PADError with code + context
    → Logged via Logger
    → Propagated to PADFramework facade
    → Returned to caller (CLI or API)
    → CLI formats and displays to user
```

---

## 15. Data Flow Diagrams

### 15.1 Flow Execution Data Flow

```
User Input (CLI/API)
    │
    ▼
┌─────────────┐    ┌──────────────┐
│  Validation  │───▶│  Sanitization │
│  (Pydantic)  │    │  (Security)   │
└──────┬──────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 ▼
       ┌─────────────────┐
       │  PADFramework    │
       │  .execute_flow() │
       └────────┬────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌─────────┐
│PerMon  │ │FlowExe │ │Metrics  │
│.track()│ │.execute│ │Collector│
└────────┘ └───┬────┘ └─────────┘
               │
               ▼
    ┌──────────────────┐
    │ PAD.Console.Host │
    │   (subprocess)   │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │FlowExecutionResult│
    └────────┬─────────┘
             │
    ┌────────┼─────────┐
    ▼        ▼         ▼
┌──────┐ ┌──────┐ ┌────────┐
│Logging│ │Report│ │Metrics │
│       │ │Gen   │ │Update  │
└──────┘ └──────┘ └────────┘
```

### 15.2 Configuration Data Flow

```
.env ──────┐
           ▼
config.yaml ──▶ Config ──▶ PADFramework
           ▲       │
Defaults ──┘       │
                   ├──▶ FlowManager
                   ├──▶ FlowExecutor
                   ├──▶ TestRunner
                   ├──▶ PerformanceMonitor
                   ├──▶ IntegrationManager
                   └──▶ Logger
```

### 15.3 Reporting Data Flow

```
Execution Results ──┐
                    ▼
Assertion Suite ──▶ ReportGenerator ──┬──▶ HTML Report
                    ▲                 ├──▶ JSON Report
Performance Stats ──┘                 ├──▶ Markdown Report
                                      └──▶ Text Report
                                            │
                                            ▼
                                       reports/ directory
```

---

## 16. Design Patterns

| Pattern | Where Used | Description |
|---------|-----------|-------------|
| **Facade** | `PADFramework` | Single entry point to all subsystems |
| **Singleton** | `MetricsCollector` | `get_metrics_collector()` returns single instance |
| **Context Manager** | `PerformanceMonitor.track()` | Resource-safe metrics collection |
| **Factory** | `ReportGenerator` | Creates reports in different formats |
| **Strategy** | `IntegrationManager` | Pluggable integration implementations |
| **Template Method** | Flow execution lifecycle | Fixed steps with variable implementation |
| **Builder** | `Config` | Progressive configuration construction |
| **Decorator** | Retry logic (tenacity) | Wraps execution with retry behavior |
| **Middleware** | `MetricsMiddleware` | Before/after hooks for metrics |
| **Data Transfer Object** | `FlowExecutionResult`, Report dataclasses | Structured data passing between layers |
| **Repository** | `FlowManager` | Abstracts flow file storage |
| **Chain of Responsibility** | Exception hierarchy | Layered error handling |

---

## 17. Security Architecture

### 17.1 Input Security

| Threat | Mitigation | Component |
|--------|-----------|-----------|
| Path Traversal | `PathValidator.validate_path()` — checks for `..` sequences | `validation.py` |
| Command Injection | `CommandValidator.validate_args()` — blocks shell metacharacters | `validation.py` |
| XSS / Injection | `InputSanitizer.sanitize_string()` — strips dangerous characters | `validation.py` |
| Invalid Input | Pydantic models validate types and constraints | `validation.py` |

### 17.2 Configuration Security

- Environment variables for secrets (DB passwords, API keys)
- `.env.example` template (no actual secrets)
- `.gitignore` excludes `.env` files
- `security.encryption_key` for data encryption
- API key rotation support

### 17.3 Execution Security

- Subprocess execution with controlled arguments
- Timeout enforcement prevents runaway processes
- Reserved flow name checking prevents system conflicts

---

## 18. Dependency Map

### 18.1 Internal Module Dependencies

```
pad_framework/
│
├── core/framework.py ─────────────────┐
│   ├── imports: core/config.py        │
│   ├── imports: core/exceptions.py    │
│   ├── imports: flows/flow_manager    │
│   ├── imports: flows/flow_executor   │ All paths lead
│   ├── imports: testing/test_runner   │ through the
│   ├── imports: utils/logger          │ facade
│   ├── imports: monitoring/perf_mon   │
│   └── imports: integrations/mgr     │
│                                      │
├── flows/async_executor.py ───────────┤
│   └── imports: flows/flow_executor   │
│                                      │
├── cli.py ────────────────────────────┘
│   └── imports: core/framework.py
│
├── monitoring/metrics.py  (standalone — Prometheus client)
├── testing/assertions.py  (standalone — no framework imports)
├── reporting/report_gen.py (standalone — no framework imports)
├── utils/helpers.py        (standalone — pure utilities)
└── utils/logger.py         (standalone — loguru wrapper)
```

### 18.2 External Dependencies

| Category | Package | Purpose |
|----------|---------|---------|
| **Core** | `pyyaml` | YAML config parsing |
| | `python-dotenv` | Environment variable loading |
| | `pydantic` | Input validation models |
| | `requests` | HTTP client |
| **CLI** | `click` | CLI framework |
| | `tabulate` | Table formatting |
| | `rich` | Rich terminal output |
| **Logging** | `loguru` | Structured logging |
| | `colorama` | Terminal colors |
| **Database** | `pyodbc` | SQL Server |
| | `pymongo` | MongoDB |
| | `redis` | Redis |
| **Excel** | `openpyxl`, `pandas`, `xlrd` | Spreadsheet operations |
| **Web** | `selenium` | Browser automation |
| | `beautifulsoup4` | HTML parsing |
| **Testing** | `pytest`, `pytest-cov`, `pytest-mock` | Test framework |
| **Async** | `aiofiles` | Async file I/O |
| **Scheduling** | `schedule` | Task scheduling |
| **Monitoring** | `psutil` | System metrics |
| | `memory-profiler` | Memory profiling |
| | `prometheus-client` | Prometheus metrics |
| **Retry** | `tenacity` | Retry logic |
| **Validation** | `jsonschema` | JSON schema validation |
| | `xmltodict` | XML processing |
| **Security** | `cryptography` | Encryption |
| **API** | `fastapi`, `uvicorn` | REST API server |
| **Docs** | `mkdocs`, `mkdocs-material` | Documentation |

---

## 19. Directory Structure

```
Power_Automate/
│
├── main.py                          # Application entry point
├── setup.py                         # Package installation & metadata
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore                       # Git ignore rules
├── LICENSE                          # Project license
│
├── configs/
│   └── config.yaml                  # Framework configuration
│
├── flows/
│   └── example_flow.json            # Example flow definition
│
├── pad_framework/                   # Main package
│   ├── __init__.py                  # Public API exports
│   ├── cli.py                       # CLI interface
│   ├── core/                        # Core components
│   ├── flows/                       # Flow management & execution
│   ├── monitoring/                  # Performance monitoring
│   ├── testing/                     # Test framework
│   ├── reporting/                   # Report generation
│   ├── integrations/                # External integrations
│   └── utils/                       # Shared utilities
│
├── tests/                           # Test suite
│   ├── test_framework.py            # Core framework tests
│   ├── test_integration.py          # Integration tests
│   ├── test_reporting.py            # Reporting tests
│   └── test_assertions.py           # Assertions tests
│
├── examples/                        # Usage examples
│   ├── basic_usage.py               # Getting started examples
│   ├── advanced_usage.py            # Advanced patterns
│   ├── reporting_example.py         # Report generation examples
│   └── assertions_example.py        # Assertions examples
│
├── docs/                            # Documentation
│   ├── getting_started.md           # Getting started guide
│   ├── api_reference.md             # API documentation
│   └── best_practices.md            # Best practices guide
│
├── learning/                        # Learning materials
│   ├── README.md                    # Learning module overview
│   ├── EXERCISES.md                 # Practice exercises
│   ├── lesson_1_3.py                # Lesson 1.3
│   ├── lesson_2_1.py                # Lesson 2.1
│   ├── lesson_2_2.py                # Lesson 2.2
│   ├── lesson_3_1.py                # Lesson 3.1
│   ├── lesson_3_4_project.py        # Lesson 3.4 project
│   └── project_1_report_generator.py # Project 1
│
├── test_quick.py                    # Quick verification script
├── run_tests.py                     # Comprehensive test runner
│
├── README.md                        # Project overview
├── ARCHITECTURE.md                  # This document
├── CHANGELOG.md                     # Version history
├── SECURITY.md                      # Security documentation
├── USER_MANUAL.md                   # User manual
├── CLI_GUIDE.md                     # CLI usage guide
├── QUICKSTART.md                    # Quick start guide
├── QUICK_REFERENCE.md               # Quick reference card
├── FEATURES.md                      # Feature list
├── COMPLETE_FEATURES.md             # Comprehensive features
├── IMPROVEMENT_PLAN.md              # Future improvements
├── IMPROVEMENTS_CHANGELOG.md        # Improvements history
├── IMPLEMENTATION_SUMMARY.md        # Implementation summary
├── REPORTING_AND_ASSERTIONS.md      # Reporting & assertions docs
├── LEARNING_MODULE.md               # Learning module docs
├── PROJECT_OVERVIEW.md              # Project overview
├── WHATS_NEW.md                     # What's new
├── START_HERE.md                    # Getting started pointer
├── ANSWER.md                        # Q&A document
└── FINAL_SUMMARY.md                 # Final summary
```

---

## 20. Technology Stack

```
┌─────────────────────────────────────────┐
│           Language: Python 3.8+          │
├─────────────────────────────────────────┤
│              CLI: click                  │
├─────────────────────────────────────────┤
│          Validation: pydantic            │
├─────────────────────────────────────────┤
│          Logging: loguru                 │
├─────────────────────────────────────────┤
│         Testing: pytest + coverage       │
├─────────────────────────────────────────┤
│    Monitoring: psutil + prometheus       │
├─────────────────────────────────────────┤
│        Retry: tenacity                   │
├─────────────────────────────────────────┤
│      Config: PyYAML + python-dotenv      │
├─────────────────────────────────────────┤
│    Async: asyncio + ThreadPoolExecutor   │
├─────────────────────────────────────────┤
│   Database: pyodbc, pymongo, redis       │
├─────────────────────────────────────────┤
│   Web: selenium, beautifulsoup4          │
├─────────────────────────────────────────┤
│    API: fastapi + uvicorn                │
├─────────────────────────────────────────┤
│    Security: cryptography                │
├─────────────────────────────────────────┤
│  Docs: mkdocs + mkdocs-material         │
├─────────────────────────────────────────┤
│    Target: Windows + PAD Console Host    │
└─────────────────────────────────────────┘
```

---

## 21. Deployment & Packaging

### 21.1 Installation

```bash
# From source
pip install -e .

# From requirements
pip install -r requirements.txt
```

### 21.2 Package Configuration (`setup.py`)

| Field | Value |
|-------|-------|
| Name | `pad-framework` |
| Version | `1.0.0` |
| Python | `>=3.8` |
| Console Scripts | `pad`, `pad-framework` |
| Package Data | `configs/*.yaml`, `configs/templates/*.json` |

### 21.3 Runtime Requirements

- Windows OS (Power Automate Desktop dependency)
- Power Automate Desktop installed at default path
- Python 3.8+ with dependencies from `requirements.txt`

---

## 22. Testing Strategy

### 22.1 Test Pyramid

```
         ┌───────────────┐
         │  Integration   │  ← tests/test_integration.py
         │   Tests (6+)   │     Cross-module workflows
         ├───────────────┤
         │  Unit Tests    │  ← tests/test_framework.py
         │   (15+ tests)  │     tests/test_assertions.py
         │                │     tests/test_reporting.py
         │                │     Individual component tests
         ├───────────────┤
         │  Quick Smoke   │  ← test_quick.py
         │   Tests        │     Fast verification
         └───────────────┘
```

### 22.2 Test Coverage Areas

| Area | Test File | Scope |
|------|----------|-------|
| Core Framework | `test_framework.py` | Init, config, flow manager |
| Assertions | `test_assertions.py` | All assertion types, suites, severity |
| Reporting | `test_reporting.py` | All formats, all report types, edge cases |
| Integration | `test_integration.py` | Cross-module workflows, error handling, performance |
| Quick Smoke | `test_quick.py` | Fast end-to-end verification |

### 22.3 Test Execution

| Command | Purpose |
|---------|---------|
| `python test_quick.py` | Fast smoke test |
| `python run_tests.py` | Full test suite with timing |
| `pytest tests/ -v` | Pytest with verbose output |
| `pytest tests/ --cov=pad_framework` | With coverage |
| `pad test --pattern "test_*"` | Via CLI |

### 22.4 Performance Benchmarks

- 1,000 assertions in < 5 seconds
- Report generation in < 2 seconds

---

## 23. Extension Points

The framework is designed for extensibility at several points:

| Extension Point | Mechanism | Example |
|----------------|-----------|---------|
| **New Integrations** | `IntegrationManager.register_integration()` | Add Slack, Jira, etc. |
| **Flow Templates** | JSON templates in `configs/templates/` | Custom flow starters |
| **Report Formats** | Add methods to `ReportGenerator` | CSV, PDF implementation |
| **Custom Assertions** | `Assertions.assert_custom()` | Domain-specific checks |
| **Metrics** | `MetricsCollector` counters/gauges | Custom Prometheus metrics |
| **Configuration** | Add keys to `DEFAULT_CONFIG` | New configuration domains |
| **CLI Commands** | Add `@cli.command()` in `cli.py` | Custom CLI operations |
| **Error Codes** | Extend `ErrorCode` enum | New error categories |

---

## 24. Glossary

| Term | Definition |
|------|-----------|
| **PAD** | Power Automate Desktop — Microsoft's desktop automation tool |
| **Flow** | An automation workflow defined as a JSON file with actions, variables, and settings |
| **Action** | A single step within a flow (e.g., DisplayMessage, SetVariable) |
| **Execution** | A single run of a flow with input variables and recorded results |
| **Assertion** | A testable condition that verifies expected behavior |
| **Suite** | A collection of related assertions grouped for reporting |
| **Facade** | A design pattern providing a unified interface to subsystems |
| **DAG** | Directed Acyclic Graph — used for dependency-based flow execution |
| **Cron** | A time-based scheduling format (e.g., `*/5 * * * *` = every 5 minutes) |
| **Prometheus** | An open-source monitoring system; metrics are exported in its format |

---

*This document was generated from a comprehensive analysis of the PAD Framework codebase.*
