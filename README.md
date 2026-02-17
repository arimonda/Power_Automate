# Power Automate Desktop Framework

## Enterprise-Grade | Production-Ready | Fully Featured

A comprehensive, professional Python framework for managing, testing, and automating Microsoft Power Automate Desktop flows.

**Version 1.1.0** - Now with enhanced security, validation, CLI, metrics, async support, and full Excel/VBA automation!

See [What's New](docs/changelog/WHATS_NEW.md) and [Improvements Changelog](docs/changelog/IMPROVEMENTS_CHANGELOG.md) for details.

## New User? Start Here!

**Complete Learning Resources Available:**

1. [QUICKSTART](docs/guides/QUICKSTART.md) - Get started in 5 minutes
2. [USER_MANUAL](docs/guides/USER_MANUAL.md) - Complete user guide with examples
3. [LEARNING_MODULE](docs/guides/LEARNING_MODULE.md) - Step-by-step tutorials (3.5 hours)
4. `learning/` folder - Hands-on practice files with exercises
5. [QUICK_REFERENCE](docs/guides/QUICK_REFERENCE.md) - One-page cheat sheet

### Quick Learning Path

```
docs/guides/QUICKSTART.md      (5 min)
    ↓
docs/guides/USER_MANUAL.md     (30 min)
    ↓
learning/*.py                   (3.5 hours)
    ↓
Build Your Own Projects!
```

## Features

### Core Features
- **Flow Management** - Create, import, export, validate flows
- **Async Execution** - Real async/await with concurrency control
- **Testing Framework** - Comprehensive testing with pytest
- **Monitoring** - Prometheus metrics, performance tracking
- **Security** - Input validation, injection prevention, encryption
- **CLI Interface** - Professional command-line tools (10 commands)
- **Structured Logging** - Advanced logging with rotation
- **Configuration** - Flexible YAML + environment variables

### Excel / VBA Automation
- **Workbook Operations** - Open, create, save, save-as, close, attach
- **Worksheet Operations** - Add, rename, copy, delete, protect
- **Cell/Range Operations** - Read, write, formulas, find, replace, clear
- **Formatting** - Font, borders, fill, merge, freeze panes, number format
- **Data Operations** - Sort, filter, remove duplicates, named ranges
- **Tables & Pivots** - Create, resize, refresh
- **Charts** - Create, export as image, delete
- **VBA Macros** - Run, pass arguments, capture return values
- **Popup Handling** - UserForms, InputBox, MsgBox, file dialogs, password prompts
- **Error Recovery** - Detect hung Excel, dismiss dialogs, force close

### Advanced Features
- **Retry Logic** - Exponential backoff, automatic retry
- **Scheduling** - Cron-style flow scheduling
- **Integrations** - Database, Email, API, Web, Excel
- **Performance** - Real-time metrics, resource monitoring
- **Validation** - Pydantic-based input validation (20+ validators)
- **Error Handling** - Structured error codes (80+), detailed context
- **Pipeline Execution** - Sequential and parallel flow chains
- **Reporting** - Multi-format reports (HTML, JSON, MD, CSV, Text)
- **Assertions** - 20+ assertion types for testing and validation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from pad_framework import PADFramework

pad = PADFramework()

result = pad.execute_flow(
    flow_name="MyFlow",
    input_variables={"param1": "value1"},
    timeout=300,
    retry_count=3
)

print(f"Status: {result.status}")
print(f"Duration: {result.duration}s")
print(f"Output: {result.output}")
```

### Command Line Interface

```bash
pip install -e .

pad execute MyFlow --retry 3 --timeout 600
pad stats
pad health
pad logs --level ERROR --flow MyFlow
```

### Excel Automation

```python
from pad_framework import ExcelFlowBuilder, ExcelWorkbookActions, ExcelCellActions

builder = ExcelFlowBuilder("ReadSalesData")
builder.add(ExcelWorkbookActions.launch())
builder.add(ExcelWorkbookActions.open_workbook(r"C:\Data\sales.xlsx"))
builder.add(ExcelCellActions.read("A1:D100"))
builder.add(ExcelWorkbookActions.close())

flow = builder.build()
```

## Project Structure

```
Power_Automate/
├── main.py                     # Application entry point
├── setup.py                    # Package installation
├── requirements.txt            # Dependencies
│
├── pad_framework/              # Core framework package
│   ├── core/                   #   Framework, config, validation, errors
│   ├── flows/                  #   Flow manager, executor, async executor
│   ├── integrations/           #   Email, DB, API, Excel automation
│   ├── monitoring/             #   Performance monitor, Prometheus metrics
│   ├── testing/                #   Test runner, assertions framework
│   ├── reporting/              #   Multi-format report generator
│   ├── utils/                  #   Logger, helpers
│   └── cli.py                  #   Command-line interface
│
├── configs/                    # Configuration files
│   ├── config.yaml             #   Main settings
│   └── templates/              #   Flow templates (Excel, etc.)
│
├── flows/                      # PAD flow definitions
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── learning/                   # Step-by-step tutorials
│
└── docs/                       # Documentation
    ├── guides/                 #   User guides & tutorials
    ├── architecture/           #   System architecture docs
    ├── reference/              #   API, features, security
    └── changelog/              #   Version history & plans
```

## Documentation

All documentation lives in the `docs/` folder, organized by category:

### Guides (`docs/guides/`)
- [START_HERE](docs/guides/START_HERE.md) - Welcome guide
- [QUICKSTART](docs/guides/QUICKSTART.md) - 5-minute setup
- [USER_MANUAL](docs/guides/USER_MANUAL.md) - Complete user manual
- [CLI_GUIDE](docs/guides/CLI_GUIDE.md) - Command-line interface guide
- [QUICK_REFERENCE](docs/guides/QUICK_REFERENCE.md) - One-page cheat sheet
- [LEARNING_MODULE](docs/guides/LEARNING_MODULE.md) - Step-by-step tutorials (3.5 hours)

### Architecture (`docs/architecture/`)
- [ARCHITECTURE](docs/architecture/ARCHITECTURE.md) - Detailed technical architecture
- [ARCHITECTURE_OVERVIEW](docs/architecture/ARCHITECTURE_OVERVIEW.md) - Plain-language overview
- [PROJECT_OVERVIEW](docs/architecture/PROJECT_OVERVIEW.md) - Project structure

### Reference (`docs/reference/`)
- [API Reference](docs/reference/api_reference.md) - Complete API documentation
- [Best Practices](docs/reference/best_practices.md) - Best practices guide
- [Getting Started](docs/reference/getting_started.md) - Detailed setup guide
- [FEATURES](docs/reference/FEATURES.md) - All 150+ features
- [COMPLETE_FEATURES](docs/reference/COMPLETE_FEATURES.md) - Comprehensive feature list
- [REPORTING_AND_ASSERTIONS](docs/reference/REPORTING_AND_ASSERTIONS.md) - Reporting & assertions
- [SECURITY](docs/reference/SECURITY.md) - Security features

### Changelog (`docs/changelog/`)
- [CHANGELOG](docs/changelog/CHANGELOG.md) - Version history
- [WHATS_NEW](docs/changelog/WHATS_NEW.md) - What's new
- [IMPROVEMENTS_CHANGELOG](docs/changelog/IMPROVEMENTS_CHANGELOG.md) - v1.1.0 changes
- [IMPROVEMENT_PLAN](docs/changelog/IMPROVEMENT_PLAN.md) - Future plans

### Learning Resources
- `learning/` - Hands-on practice files (15 lessons + exercises)
- `examples/` - Working code examples (basic, advanced, Excel, reporting, assertions)

## Learning Path for Beginners

**Total Time: ~4 hours to become proficient**

1. Read [QUICKSTART](docs/guides/QUICKSTART.md) (5 min)
2. Read [USER_MANUAL](docs/guides/USER_MANUAL.md) (30 min)
3. Complete [LEARNING_MODULE](docs/guides/LEARNING_MODULE.md) (3.5 hours)
4. Try examples in `examples/` (30 min)
5. Build your own project!

## Configuration

Edit `configs/config.yaml` to customize flows, logging, database, email, API, retry, and performance settings.

## License

MIT License
