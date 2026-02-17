# Power Automate Desktop Framework - Learning Module

## 🎓 Learn Step-by-Step

**Welcome to the PAD Framework Learning Module!**

This guide will take you from beginner to expert through hands-on tutorials and exercises.

---

## 📚 Learning Path

```
Level 1: Beginner (30 minutes)
  ↓
Level 2: Intermediate (1 hour)
  ↓
Level 3: Advanced (2 hours)
  ↓
Level 4: Expert (Practice)
```

---

## Level 1: Beginner (30 Minutes)

### Lesson 1.1: Understanding the Framework (5 min)

**What You'll Learn**:
- What the framework does
- Basic concepts
- Project structure

**Theory**:

The PAD Framework is like a **control panel** for your automation flows:
- 🎮 **Framework** = Control panel
- 📋 **Flows** = Automation recipes
- ⚙️ **Execution** = Running the recipes
- 📊 **Monitoring** = Checking how well they run

**Your First Look**:

```python
# This is ALL you need to start!
from pad_framework import PADFramework

pad = PADFramework()
```

✅ **Checkpoint**: You understand what the framework is for.

---

### Lesson 1.2: Installation & Setup (10 min)

**What You'll Learn**:
- Install Python packages
- Verify installation
- Run your first command

**Hands-On Exercise**:

1. **Open PowerShell**

2. **Navigate to project folder**:
   ```powershell
   cd "c:\Users\arimo\.projects\Power_Automate"
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   Wait for completion ☕

4. **Test installation**:
   ```powershell
   python main.py
   ```

5. **Expected Output**:
   ```
   ✓ Framework initialized successfully
   Framework Health Status:
     status: healthy
   ```

✅ **Checkpoint**: You can run the framework.

**Practice Quiz**:
- Q: What command installs dependencies?
- A: `pip install -r requirements.txt`

---

### Lesson 1.3: Your First Script (15 min)

**What You'll Learn**:
- Create a Python script
- Use the framework
- Execute a flow

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_1_3.py`

2. **Type this code**:

```python
# Lesson 1.3: My First Script
from pad_framework import PADFramework

# Step 1: Create framework instance
print("Step 1: Initializing framework...")
pad = PADFramework()
print("✓ Framework ready!\n")

# Step 2: Check health
print("Step 2: Checking health...")
health = pad.get_health_status()
print(f"Status: {health['status']}")
print(f"Version: {health['version']}\n")

# Step 3: List available flows
print("Step 3: Listing flows...")
flows = pad.list_flows()
print(f"Found {len(flows)} flows:")
for i, flow in enumerate(flows, 1):
    print(f"  {i}. {flow}")

print("\n✓ Script completed successfully!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_1_3.py
   ```

4. **Expected Output**:
   ```
   Step 1: Initializing framework...
   ✓ Framework ready!
   
   Step 2: Checking health...
   Status: healthy
   Version: 1.0.0
   
   Step 3: Listing flows...
   Found 1 flows:
     1. ExampleFlow
   
   ✓ Script completed successfully!
   ```

✅ **Checkpoint**: You can write and run a basic script.

**Exercise**: Modify the script to also print the number of flows found.

---

## Level 2: Intermediate (1 Hour)

### Lesson 2.1: Flow Execution (20 min)

**What You'll Learn**:
- Execute flows
- Pass input variables
- Handle results

**Theory**:

Flow execution follows this pattern:
```
Input → Execute Flow → Output
```

Like calling a function:
```python
result = function(input_data)
```

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_2_1.py`

2. **Type this code**:

```python
# Lesson 2.1: Flow Execution
from pad_framework import PADFramework

pad = PADFramework()

# Execute the example flow
print("Executing ExampleFlow...")
result = pad.execute_flow(
    flow_name="ExampleFlow",
    input_variables={
        "inputParam1": "Hello from Learning Module",
        "inputParam2": 100
    }
)

# Check the result
print(f"\nExecution Result:")
print(f"  Status: {result.status}")
print(f"  Duration: {result.duration:.2f} seconds")
print(f"  Execution ID: {result.execution_id}")

if result.status == "success":
    print(f"  Output: {result.output}")
    print("\n✓ Flow executed successfully!")
else:
    print(f"  Error: {result.error}")
    print("\n✗ Flow execution failed!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_2_1.py
   ```

✅ **Checkpoint**: You can execute flows and check results.

**Practice Exercise**:

Modify the script to:
1. Execute the flow with different input values
2. Print only if duration is less than 5 seconds
3. Count successful vs failed executions

<details>
<summary>💡 Solution (Click to reveal)</summary>

```python
from pad_framework import PADFramework

pad = PADFramework()

test_inputs = [
    {"inputParam1": "Test 1", "inputParam2": 10},
    {"inputParam1": "Test 2", "inputParam2": 20},
    {"inputParam1": "Test 3", "inputParam2": 30},
]

successful = 0
failed = 0

for i, inputs in enumerate(test_inputs, 1):
    print(f"\nTest {i}:")
    result = pad.execute_flow("ExampleFlow", inputs)
    
    if result.status == "success":
        successful += 1
        if result.duration < 5:
            print(f"  ✓ Fast execution: {result.duration:.2f}s")
    else:
        failed += 1

print(f"\nSummary: {successful} successful, {failed} failed")
```
</details>

---

### Lesson 2.2: Creating Flows (20 min)

**What You'll Learn**:
- Create new flows
- Understand flow structure
- Validate flows

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_2_2.py`

2. **Type this code**:

```python
# Lesson 2.2: Creating Flows
from pad_framework import PADFramework

pad = PADFramework()

# Create a new flow
flow_name = "MyLearningFlow"
print(f"Creating flow: {flow_name}")

success = pad.create_flow(flow_name, template="basic")

if success:
    print(f"✓ Flow created!\n")
    
    # Validate the flow
    print("Validating flow...")
    validation = pad.validate_flow(flow_name)
    
    if validation["valid"]:
        print("✓ Flow is valid!")
    else:
        print("✗ Flow has errors:")
        for error in validation["errors"]:
            print(f"  - {error}")
    
    # List all flows to confirm
    print(f"\nAll flows:")
    flows = pad.list_flows()
    for flow in flows:
        print(f"  - {flow}")
else:
    print("✗ Failed to create flow")
```

3. **Run it**:
   ```powershell
   python learning/lesson_2_2.py
   ```

4. **Check the flow file**:
   ```powershell
   cat flows/MyLearningFlow.json
   ```

✅ **Checkpoint**: You can create and validate flows.

**Practice Exercise**:

Create three flows with different names and verify they all appear in the list.

---

### Lesson 2.3: Error Handling & Retry (20 min)

**What You'll Learn**:
- Handle execution errors
- Use retry mechanism
- Set timeouts

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_2_3.py`

2. **Type this code**:

```python
# Lesson 2.3: Error Handling & Retry
from pad_framework import PADFramework

pad = PADFramework()

def execute_with_retry(flow_name, inputs, retries=3):
    """Execute flow with retry logic"""
    
    print(f"Executing {flow_name} with {retries} retries...")
    
    try:
        result = pad.execute_flow(
            flow_name=flow_name,
            input_variables=inputs,
            retry_count=retries,
            timeout=60  # 1 minute timeout
        )
        
        if result.status == "success":
            print(f"✓ Success! Duration: {result.duration:.2f}s")
            return True
        else:
            print(f"✗ Failed: {result.error}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return False

# Test with existing flow
success = execute_with_retry(
    "ExampleFlow",
    {"inputParam1": "Test", "inputParam2": 1},
    retries=2
)

if success:
    print("\n✓ Execution completed successfully!")
else:
    print("\n✗ Execution failed after retries!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_2_3.py
   ```

✅ **Checkpoint**: You understand error handling and retry.

---

## Level 3: Advanced (2 Hours)

### Lesson 3.1: Performance Monitoring (30 min)

**What You'll Learn**:
- Track performance metrics
- Analyze execution times
- Set up monitoring

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_3_1.py`

2. **Type this code**:

```python
# Lesson 3.1: Performance Monitoring
from pad_framework import PADFramework
import time

pad = PADFramework()

# Execute flow multiple times
flow_name = "ExampleFlow"
executions = 5

print(f"Running {flow_name} {executions} times...\n")

for i in range(executions):
    print(f"Execution {i+1}/{executions}...")
    result = pad.execute_flow(
        flow_name,
        {"inputParam1": f"Test {i+1}", "inputParam2": i+1}
    )
    print(f"  Duration: {result.duration:.2f}s")
    time.sleep(1)  # Wait between executions

# Get performance statistics
print(f"\n{'='*50}")
print("PERFORMANCE STATISTICS")
print(f"{'='*50}")

stats = pad.get_performance_stats(flow_name)

if stats:
    print(f"Flow: {flow_name}")
    print(f"  Total Executions: {stats['execution_count']}")
    print(f"  Average Duration: {stats['avg_duration']:.2f}s")
    print(f"  Fastest: {stats['min_duration']:.2f}s")
    print(f"  Slowest: {stats['max_duration']:.2f}s")
    print(f"  Avg Memory Usage: {stats['avg_memory_delta_mb']:.2f}MB")
    
    # Analyze performance
    if stats['avg_duration'] < 1:
        print("\n✓ Excellent performance!")
    elif stats['avg_duration'] < 5:
        print("\n✓ Good performance")
    else:
        print("\n⚠ Consider optimization")
else:
    print("No statistics available")
```

3. **Run it**:
   ```powershell
   python learning/lesson_3_1.py
   ```

✅ **Checkpoint**: You can monitor and analyze performance.

**Challenge**: Create a function that alerts you if average duration exceeds a threshold.

---

### Lesson 3.2: Flow Scheduling (30 min)

**What You'll Learn**:
- Schedule flow execution
- Use cron expressions
- Manage schedules

**Theory - Cron Expressions**:

```
┌─ Minute (0-59)
│ ┌─ Hour (0-23)
│ │ ┌─ Day of Month (1-31)
│ │ │ ┌─ Month (1-12)
│ │ │ │ ┌─ Day of Week (0-6, 0=Sunday)
│ │ │ │ │
* * * * *
```

Examples:
- `0 9 * * *` = Every day at 9 AM
- `0 */2 * * *` = Every 2 hours
- `30 8 * * 1-5` = Weekdays at 8:30 AM

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_3_2.py`

2. **Type this code**:

```python
# Lesson 3.2: Flow Scheduling
from pad_framework import PADFramework

pad = PADFramework()

# Schedule examples
schedules = {
    "DailyReport": "0 9 * * *",      # 9 AM daily
    "HourlyCheck": "0 * * * *",      # Every hour
    "WeeklyBackup": "0 2 * * 0",     # Sunday 2 AM
}

print("Scheduling flows...\n")

schedule_ids = {}

for flow_name, schedule in schedules.items():
    schedule_id = pad.schedule_flow(
        flow_name=flow_name,
        schedule=schedule,
        input_variables={"scheduled": True}
    )
    schedule_ids[flow_name] = schedule_id
    print(f"✓ Scheduled {flow_name}")
    print(f"  Schedule: {schedule}")
    print(f"  ID: {schedule_id}\n")

# View active schedules
print(f"Active schedules: {pad.flow_executor.get_active_schedules_count()}")

# Cancel schedules (for learning purposes)
print("\nCanceling schedules...")
for flow_name, schedule_id in schedule_ids.items():
    pad.cancel_schedule(schedule_id)
    print(f"✓ Canceled {flow_name}")

print("\n✓ Lesson completed!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_3_2.py
   ```

✅ **Checkpoint**: You can schedule and manage flow executions.

---

### Lesson 3.3: Integrations (30 min)

**What You'll Learn**:
- Use database integration
- Send emails
- Work with APIs
- File operations

**Hands-On Exercise**:

1. **Create file**: `learning/lesson_3_3.py`

2. **Type this code**:

```python
# Lesson 3.3: Integrations
from pad_framework import PADFramework

pad = PADFramework()

print("Testing Integrations\n")
print("="*50)

# 1. Database Integration
print("\n1. Database Integration:")
db = pad.integrate("database")
print(f"  Status: {db['status']}")
print(f"  Type: {db['type']}")
print(f"  Capabilities: {', '.join(db['capabilities'])}")

# 2. Email Integration
print("\n2. Email Integration:")
email = pad.integrate("email")
print(f"  Status: {email['status']}")
print(f"  Server: {email['smtp_server']}")
print(f"  Capabilities: {', '.join(email['capabilities'])}")

# 3. API Integration
print("\n3. API Integration:")
api = pad.integrate("api", endpoint="https://api.example.com")
print(f"  Status: {api['status']}")
print(f"  Endpoint: {api['endpoint']}")
print(f"  Capabilities: {', '.join(api['capabilities'])}")

# 4. Web Automation
print("\n4. Web Automation:")
web = pad.integrate("web")
print(f"  Status: {web['status']}")
print(f"  Browser: {web['browser']}")
print(f"  Capabilities: {', '.join(web['capabilities'])}")

# 5. File Operations
print("\n5. File Operations:")
files = pad.integrate("file")
print(f"  Status: {files['status']}")
print(f"  Capabilities: {', '.join(files['capabilities'])}")

print("\n" + "="*50)
print("✓ All integrations initialized successfully!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_3_3.py
   ```

✅ **Checkpoint**: You understand available integrations.

---

### Lesson 3.4: Building a Complete Solution (30 min)

**What You'll Learn**:
- Combine multiple concepts
- Build a real-world solution
- Apply best practices

**Project**: Build a Data Processing Pipeline

1. **Create file**: `learning/lesson_3_4_project.py`

2. **Type this code**:

```python
# Lesson 3.4: Complete Solution - Data Processing Pipeline
from pad_framework import PADFramework
import time

class DataPipeline:
    def __init__(self):
        self.pad = PADFramework()
        self.results = []
    
    def run_pipeline(self, data_file):
        """Run complete data processing pipeline"""
        
        print(f"{'='*60}")
        print(f"DATA PROCESSING PIPELINE")
        print(f"{'='*60}\n")
        
        # Step 1: Validate
        print("Step 1: Validating flows...")
        if not self.validate_flows():
            return False
        print("✓ All flows valid\n")
        
        # Step 2: Extract
        print("Step 2: Extracting data...")
        extract_result = self.extract_data(data_file)
        if not extract_result:
            return False
        print(f"✓ Data extracted\n")
        
        # Step 3: Transform
        print("Step 3: Transforming data...")
        transform_result = self.transform_data(extract_result)
        if not transform_result:
            return False
        print(f"✓ Data transformed\n")
        
        # Step 4: Load
        print("Step 4: Loading data...")
        load_result = self.load_data(transform_result)
        if not load_result:
            return False
        print(f"✓ Data loaded\n")
        
        # Step 5: Report
        print("Step 5: Generating report...")
        self.generate_report()
        print("✓ Report generated\n")
        
        print(f"{'='*60}")
        print("✓ PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        
        return True
    
    def validate_flows(self):
        """Validate all required flows"""
        flows = ["ExampleFlow"]  # Add your flows here
        
        for flow in flows:
            validation = self.pad.validate_flow(flow)
            if not validation["valid"]:
                print(f"✗ {flow} validation failed")
                return False
        return True
    
    def extract_data(self, data_file):
        """Extract data from source"""
        # Simulate data extraction
        print(f"  Source: {data_file}")
        time.sleep(0.5)
        return {"records": 100, "status": "extracted"}
    
    def transform_data(self, data):
        """Transform extracted data"""
        # Simulate data transformation
        print(f"  Processing {data['records']} records...")
        time.sleep(0.5)
        return {"records": data["records"], "status": "transformed"}
    
    def load_data(self, data):
        """Load data to destination"""
        # Simulate data loading
        print(f"  Loading {data['records']} records...")
        time.sleep(0.5)
        return {"records": data["records"], "status": "loaded"}
    
    def generate_report(self):
        """Generate execution report"""
        stats = self.pad.get_performance_stats()
        print(f"  Pipeline Statistics:")
        print(f"    Total Executions: {len(self.results)}")
        print(f"    Success Rate: 100%")

# Run the pipeline
if __name__ == "__main__":
    pipeline = DataPipeline()
    success = pipeline.run_pipeline("data/input.xlsx")
    
    if success:
        print("\n✓ Project completed successfully!")
    else:
        print("\n✗ Project failed!")
```

3. **Run it**:
   ```powershell
   python learning/lesson_3_4_project.py
   ```

✅ **Checkpoint**: You can build complete solutions!

---

## Level 4: Expert (Practice Projects)

### Project 1: Automated Report Generator

**Goal**: Create a system that generates reports daily

**Requirements**:
- Schedule daily execution
- Extract data from database
- Generate Excel report
- Send email with report attached
- Log all operations

**Starter Code**:

```python
from pad_framework import PADFramework

class ReportGenerator:
    def __init__(self):
        self.pad = PADFramework()
    
    def generate_daily_report(self):
        # TODO: Implement report generation
        pass
    
    def schedule_reports(self):
        # TODO: Schedule daily execution
        pass

# Your implementation here
```

---

### Project 2: Data Sync Tool

**Goal**: Sync data between two systems

**Requirements**:
- Read data from source
- Transform data format
- Validate data quality
- Write to destination
- Handle errors gracefully
- Monitor performance

---

### Project 3: Health Monitoring Dashboard

**Goal**: Create a monitoring system for all flows

**Requirements**:
- Check health of all flows
- Track performance metrics
- Alert on failures
- Generate status dashboard
- Historical trend analysis

---

## 🎯 Practice Exercises

### Easy Exercises

1. **List Flows**: Write a script that lists all flows and counts them
2. **Execute Flow**: Execute ExampleFlow with custom inputs
3. **Validate**: Create and validate a new flow
4. **Health Check**: Display framework health in a formatted way

### Medium Exercises

5. **Batch Execution**: Execute multiple flows in sequence
6. **Error Handler**: Create a function that handles flow errors gracefully
7. **Performance Tracker**: Track execution times of 10 runs
8. **Schedule Manager**: Create, list, and cancel schedules

### Hard Exercises

9. **Flow Pipeline**: Chain 3 flows together, passing output to input
10. **Retry Logic**: Implement custom retry with exponential backoff
11. **Performance Optimizer**: Identify and optimize slow flows
12. **Integration Manager**: Test all integrations and report status

---

## 📝 Assessment Checklist

Mark completed items:

**Level 1 - Beginner**
- [ ] Installed framework successfully
- [ ] Ran first script
- [ ] Listed available flows
- [ ] Checked framework health

**Level 2 - Intermediate**
- [ ] Executed flows with custom inputs
- [ ] Created new flows
- [ ] Validated flows
- [ ] Handled execution errors
- [ ] Used retry mechanism

**Level 3 - Advanced**
- [ ] Monitored performance metrics
- [ ] Scheduled flow execution
- [ ] Used integrations
- [ ] Built complete pipeline
- [ ] Applied best practices

**Level 4 - Expert**
- [ ] Completed Project 1
- [ ] Completed Project 2
- [ ] Completed Project 3
- [ ] Can debug complex issues
- [ ] Can extend framework

---

## 🎓 Certificate of Completion

When you complete all levels:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              CERTIFICATE OF COMPLETION                    ║
║                                                          ║
║    Power Automate Desktop Framework Training             ║
║                                                          ║
║                  [Your Name]                             ║
║                                                          ║
║    Has successfully completed all levels of training     ║
║           in the PAD Framework Learning Module           ║
║                                                          ║
║              Date: _________________                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🆘 Need Help?

- **Stuck on a lesson?** Check the solution hints
- **Error in code?** Read the error message carefully
- **Don't understand?** Review the theory section
- **Need examples?** Check `examples/` folder
- **Want details?** Read `USER_MANUAL.md`

---

## 📚 Additional Resources

- **User Manual**: `USER_MANUAL.md` - Comprehensive reference
- **API Docs**: `docs/api_reference.md` - All functions
- **Examples**: `examples/` - Working code samples
- **Best Practices**: `docs/best_practices.md` - Guidelines

---

## 🎉 Congratulations!

You've completed the PAD Framework Learning Module!

**What's Next?**
1. Build your own projects
2. Explore advanced features
3. Optimize your workflows
4. Share your knowledge

**Happy Automating!** 🚀

---

**Learning Module Version**: 1.0.0  
**Last Updated**: February 11, 2026  
**Estimated Total Time**: 3.5 hours
