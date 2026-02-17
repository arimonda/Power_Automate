"""
Lesson 2.1: Flow Execution
Learn how to execute flows and handle results
"""

from pad_framework import PADFramework

print("="*60)
print("LESSON 2.1: Flow Execution")
print("="*60)
print()

pad = PADFramework()

# Execute the example flow
print("Executing ExampleFlow...")
print("-"*40)

result = pad.execute_flow(
    flow_name="ExampleFlow",
    input_variables={
        "inputParam1": "Hello from Learning Module!",
        "inputParam2": 100
    }
)

# Check the result
print("\nExecution Result:")
print(f"  Status: {result.status}")
print(f"  Duration: {result.duration:.2f} seconds")
print(f"  Execution ID: {result.execution_id}")
print(f"  Start Time: {result.start_time}")

if result.status == "success":
    print(f"\n✓ Flow executed successfully!")
    if result.output:
        print(f"  Output: {result.output}")
else:
    print(f"\n✗ Flow execution failed!")
    print(f"  Error: {result.error}")

print()
print("="*60)

# EXERCISE
print("\n💡 EXERCISE:")
print("1. Change the input parameters and run again")
print("2. Try executing with different values")
print("3. Time how long multiple executions take")
print()

# BONUS: Multiple executions
print("BONUS: Running 3 times...")
for i in range(3):
    result = pad.execute_flow("ExampleFlow", {"inputParam2": i})
    print(f"  Run {i+1}: {result.status} ({result.duration:.2f}s)")
