# Power Automate Desktop Framework

## 🚀 Enterprise-Grade | Production-Ready | Fully Featured

A comprehensive, professional Python framework for managing, testing, and automating Microsoft Power Automate Desktop flows.

**Version 1.1.0** - Now with enhanced security, validation, CLI, metrics, and async support!

## ⭐ What's New in v1.1.0

- ✅ **Input Validation Framework** - Pydantic-based validation for all inputs
- ✅ **Enhanced Error Handling** - Structured error codes (80+) and detailed context
- ✅ **Professional CLI** - Full-featured command-line interface (10 commands)
- ✅ **Metrics System** - Prometheus-compatible metrics export (15+ metrics)
- ✅ **Async Support** - Real async/await for concurrent execution
- ✅ **Security Enhancements** - Input sanitization, injection prevention
- ✅ **Reporting System** - Multi-format reports (HTML, JSON, MD, CSV, Text)
- ✅ **Assertion Framework** - 20+ assertion types for testing and validation
- ✅ **Complete Documentation** - Comprehensive guides for all features

See [IMPROVEMENTS_CHANGELOG.md](IMPROVEMENTS_CHANGELOG.md) and [REPORTING_AND_ASSERTIONS.md](REPORTING_AND_ASSERTIONS.md) for details.

## 🎓 New User? Start Here!

**Complete Learning Resources Available:**

1. **QUICKSTART.md** - Get started in 5 minutes
2. **USER_MANUAL.md** - Complete user guide with examples
3. **LEARNING_MODULE.md** - Step-by-step tutorials (3.5 hours)
4. **learning/** folder - Hands-on practice files with exercises
5. **QUICK_REFERENCE.md** - One-page cheat sheet

### Quick Learning Path

```
QUICKSTART.md (5 min)
    ↓
USER_MANUAL.md (30 min)
    ↓
LEARNING_MODULE.md + learning/*.py (3.5 hours)
    ↓
Build Your Own Projects! 🚀
```

## Features

✨ **Professional & Enterprise-Ready**

### Core Features
- 🔄 **Flow Management** - Create, import, export, validate flows
- ⚡ **Async Execution** - Real async/await with concurrency control
- 🧪 **Testing Framework** - Comprehensive testing with pytest
- 📊 **Monitoring** - Prometheus metrics, performance tracking
- 🔐 **Security** - Input validation, injection prevention, encryption
- 🖥️ **CLI Interface** - Professional command-line tools
- 📝 **Structured Logging** - Advanced logging with rotation
- ⚙️ **Configuration** - Flexible YAML + environment variables

### Advanced Features
- 🔁 **Retry Logic** - Exponential backoff, automatic retry
- ⏱️ **Scheduling** - Cron-style flow scheduling
- 🔌 **Integrations** - Database, Email, API, Web automation
- 📈 **Performance** - Real-time metrics, resource monitoring
- 🛡️ **Validation** - Pydantic-based input validation (20+ validators)
- 🚨 **Error Handling** - Structured error codes (80+), detailed context
- 📋 **Audit Trail** - Comprehensive execution logging
- 🔄 **Pipeline Execution** - Sequential and parallel flow chains
- 📊 **Reporting** - Multi-format reports (HTML, JSON, MD, CSV, Text)
- 🧪 **Assertions** - 20+ assertion types for testing and validation

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from pad_framework import PADFramework

# Initialize framework
pad = PADFramework()

# Execute a flow
result = pad.execute_flow(
    flow_name="MyFlow",
    input_variables={"param1": "value1"},
    timeout=300,
    retry_count=3
)

# Check execution status
print(f"Status: {result.status}")
print(f"Duration: {result.duration}s")
print(f"Output: {result.output}")
```

### Command Line Interface

```bash
# Install CLI
pip install -e .

# Execute a flow
pad execute MyFlow --retry 3 --timeout 600

# View statistics
pad stats

# Check health
pad health

# View logs
pad logs --level ERROR --flow MyFlow
```

### Async Execution

```python
from pad_framework.flows.async_executor import AsyncFlowExecutor
import asyncio

async def main():
    pad = PADFramework()
    executor = AsyncFlowExecutor(pad.flow_executor, max_concurrent=10)
    
    # Execute multiple flows in parallel
    results = await executor.execute_batch([
        {"flow_name": "Flow1"},
        {"flow_name": "Flow2"},
        {"flow_name": "Flow3"}
    ])

asyncio.run(main())
```

## Project Structure

```
Power_Automate/
├── pad_framework/           # Core framework
│   ├── core/               # Core functionality
│   ├── flows/              # Flow management
│   ├── testing/            # Testing utilities
│   ├── utils/              # Helper utilities
│   ├── integrations/       # External integrations
│   └── monitoring/         # Monitoring & logging
├── flows/                  # Your PAD flows
├── tests/                  # Test cases
├── configs/                # Configuration files
├── logs/                   # Log files
├── data/                   # Data files
└── examples/               # Usage examples
```

## Configuration

Edit `configs/config.yaml` to customize:

- Flow paths
- Logging levels
- Database connections
- Email settings
- API endpoints
- Retry policies
- Performance thresholds

## 📚 Documentation

### 🚀 Getting Started
- **START_HERE.md** - Welcome guide (start here!)
- **QUICKSTART.md** - 5-minute setup
- **USER_MANUAL.md** - Complete user manual
- **QUICK_REFERENCE.md** - One-page cheat sheet
- **CLI_GUIDE.md** - Command-line interface guide

### 🎓 Learning Resources
- **LEARNING_MODULE.md** - Step-by-step tutorials (3.5 hours)
- **learning/** - Hands-on practice files with exercises
  - `lesson_1_3.py` - Your first script
  - `lesson_2_1.py` - Flow execution
  - `lesson_3_1.py` - Performance monitoring
  - `lesson_3_4_project.py` - Complete project
  - `EXERCISES.md` - Practice exercises with solutions
- **examples/** - Working code examples
  - `basic_usage.py` - Common operations
  - `advanced_usage.py` - Advanced patterns

### 📖 Reference & Technical
- **docs/api_reference.md** - Complete API documentation
- **docs/best_practices.md** - Best practices guide
- **docs/getting_started.md** - Detailed setup guide
- **FEATURES.md** - All 150+ features listed
- **PROJECT_OVERVIEW.md** - Project architecture

### 🔒 Security & Operations
- **SECURITY.md** - Security features and best practices
- **IMPROVEMENT_PLAN.md** - Improvement strategy
- **IMPROVEMENTS_CHANGELOG.md** - v1.1.0 changes
- **CHANGELOG.md** - Version history

## 🎯 Learning Path for Beginners

**Total Time: ~4 hours to become proficient**

1. **Read QUICKSTART.md** (5 min) - Get framework running
2. **Read USER_MANUAL.md** (30 min) - Understand all features
3. **Complete LEARNING_MODULE.md** (3.5 hours)
   - Level 1: Beginner (30 min)
   - Level 2: Intermediate (1 hour)
   - Level 3: Advanced (2 hours)
   - Level 4: Expert Projects (practice)
4. **Try Examples** (30 min) - Run example scripts
5. **Build Your Project!** 🚀

## License

MIT License
