# Practice Exercises

Complete these exercises to reinforce your learning!

---

## 🟢 Level 1: Beginner Exercises

### Exercise 1.1: Hello Framework
**Goal**: Create a simple script that prints framework information

**Tasks**:
1. Import PADFramework
2. Create instance
3. Print version and status
4. Count available flows

**Expected Output**:
```
Framework Version: 1.0.0
Status: healthy
Available Flows: 1
```

<details>
<summary>💡 Solution</summary>

```python
from pad_framework import PADFramework

pad = PADFramework()
health = pad.get_health_status()

print(f"Framework Version: {health['version']}")
print(f"Status: {health['status']}")
print(f"Available Flows: {health['flows_available']}")
```
</details>

---

### Exercise 1.2: Flow Lister
**Goal**: Create a formatted list of all flows

**Tasks**:
1. Get all flows
2. Print in numbered format
3. Add search functionality

**Expected Output**:
```
All Flows:
  1. ExampleFlow
  2. DataProcessor
  3. EmailSender
```

<details>
<summary>💡 Solution</summary>

```python
from pad_framework import PADFramework

pad = PADFramework()
flows = pad.list_flows()

print("All Flows:")
for i, flow in enumerate(flows, 1):
    print(f"  {i}. {flow}")
```
</details>

---

### Exercise 1.3: Simple Executor
**Goal**: Execute a flow and display results nicely

**Tasks**:
1. Execute ExampleFlow
2. Format output with colors (✓ or ✗)
3. Show duration rounded to 2 decimals

<details>
<summary>💡 Solution</summary>

```python
from pad_framework import PADFramework

pad = PADFramework()

result = pad.execute_flow("ExampleFlow", {})

symbol = "✓" if result.status == "success" else "✗"
print(f"{symbol} Flow: {result.flow_name}")
print(f"  Status: {result.status}")
print(f"  Duration: {result.duration:.2f}s")
```
</details>

---

## 🟡 Level 2: Intermediate Exercises

### Exercise 2.1: Batch Executor
**Goal**: Execute multiple flows and report results

**Tasks**:
1. Execute 3 different flows
2. Track success/failure count
3. Calculate total duration
4. Generate summary report

**Template**:
```python
from pad_framework import PADFramework

pad = PADFramework()
flows_to_run = ["Flow1", "Flow2", "Flow3"]
results = []

# TODO: Execute each flow
# TODO: Collect results
# TODO: Generate report
```

---

### Exercise 2.2: Smart Retry
**Goal**: Create a function with custom retry logic

**Tasks**:
1. Create `execute_with_smart_retry()` function
2. Implement exponential backoff
3. Log each attempt
4. Return success/failure

**Template**:
```python
import time

def execute_with_smart_retry(pad, flow_name, max_retries=3):
    """Execute with exponential backoff"""
    
    for attempt in range(max_retries):
        # TODO: Execute flow
        # TODO: If success, return
        # TODO: If failed, wait and retry
        # TODO: Increase wait time each attempt
        pass
```

---

### Exercise 2.3: Performance Analyzer
**Goal**: Analyze flow performance and identify issues

**Tasks**:
1. Execute flow 10 times
2. Calculate average, min, max duration
3. Identify outliers (>2x average)
4. Generate performance report

**Template**:
```python
def analyze_performance(pad, flow_name, runs=10):
    """Analyze flow performance"""
    
    durations = []
    
    for i in range(runs):
        # TODO: Execute and collect duration
        pass
    
    # TODO: Calculate statistics
    # TODO: Identify outliers
    # TODO: Print report
```

---

## 🔴 Level 3: Advanced Exercises

### Exercise 3.1: Pipeline Builder
**Goal**: Create a flexible pipeline system

**Tasks**:
1. Create `Pipeline` class
2. Support adding steps
3. Execute steps in order
4. Handle step failures
5. Generate execution report

**Template**:
```python
class Pipeline:
    def __init__(self, name):
        self.name = name
        self.steps = []
        self.pad = PADFramework()
    
    def add_step(self, flow_name, inputs):
        """Add step to pipeline"""
        # TODO: Add step to list
        pass
    
    def execute(self):
        """Execute all steps"""
        # TODO: Run each step
        # TODO: Handle errors
        # TODO: Generate report
        pass
```

---

### Exercise 3.2: Health Monitor
**Goal**: Create a monitoring dashboard

**Tasks**:
1. Check health of all flows
2. Track performance metrics
3. Identify slow flows (>10s average)
4. Identify failed executions
5. Generate dashboard output

**Expected Output**:
```
=== SYSTEM HEALTH DASHBOARD ===

Overall Status: Healthy
Total Flows: 5
Active Schedules: 2

FLOW STATUS:
  ✓ Flow1 - Healthy (0.5s avg)
  ⚠ Flow2 - Slow (12.3s avg)
  ✗ Flow3 - Failed (last run)

RECOMMENDATIONS:
  • Optimize Flow2 (slow performance)
  • Investigate Flow3 failure
```

---

### Exercise 3.3: Data Sync Tool
**Goal**: Sync data between two systems

**Tasks**:
1. Read from source
2. Transform data format
3. Validate data quality
4. Write to destination
5. Handle conflicts
6. Log all operations

**Template**:
```python
class DataSync:
    def __init__(self):
        self.pad = PADFramework()
    
    def sync(self, source, destination):
        """Sync data between systems"""
        
        # TODO: Read from source
        # TODO: Transform data
        # TODO: Validate
        # TODO: Write to destination
        # TODO: Handle errors
        pass
```

---

## 🎯 Challenge Projects

### Challenge 1: Smart Scheduler
Create an intelligent scheduling system that:
- Analyzes flow performance history
- Schedules slower flows during off-peak hours
- Optimizes resource usage
- Sends alerts for failures
- Generates daily summary reports

### Challenge 2: Flow Optimizer
Build a system that:
- Identifies performance bottlenecks
- Suggests optimizations
- Benchmarks flows
- Compares versions
- Tracks improvements over time

### Challenge 3: Automation Hub
Create a central management system that:
- Manages multiple flow categories
- Provides web interface (Flask)
- Real-time monitoring dashboard
- User access control
- Audit logging
- Report generation

---

## ✅ Exercise Checklist

### Beginner
- [ ] Exercise 1.1 - Hello Framework
- [ ] Exercise 1.2 - Flow Lister
- [ ] Exercise 1.3 - Simple Executor

### Intermediate
- [ ] Exercise 2.1 - Batch Executor
- [ ] Exercise 2.2 - Smart Retry
- [ ] Exercise 2.3 - Performance Analyzer

### Advanced
- [ ] Exercise 3.1 - Pipeline Builder
- [ ] Exercise 3.2 - Health Monitor
- [ ] Exercise 3.3 - Data Sync Tool

### Challenges
- [ ] Challenge 1 - Smart Scheduler
- [ ] Challenge 2 - Flow Optimizer
- [ ] Challenge 3 - Automation Hub

---

## 📝 Submission Guidelines

1. Test your solution thoroughly
2. Add error handling
3. Include comments
4. Follow best practices
5. Document your code

---

## 🆘 Need Help?

- Review the corresponding lesson in LEARNING_MODULE.md
- Check USER_MANUAL.md for reference
- Look at examples/ folder
- Review docs/api_reference.md

---

## 🎓 Grading Rubric

- **Functionality** (40%): Does it work correctly?
- **Code Quality** (30%): Is it clean and maintainable?
- **Error Handling** (15%): Does it handle errors well?
- **Documentation** (15%): Is it well documented?

---

**Happy Coding!** 🚀
