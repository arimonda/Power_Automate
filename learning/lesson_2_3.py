"""
Lesson 2.3: Error Handling and Retry
Learn robust execution with retries and clear error handling.
"""

from pad_framework import PADFramework

print("=" * 60)
print("LESSON 2.3: Error Handling and Retry")
print("=" * 60)
print()

pad = PADFramework()

print("Case 1: Execute a valid flow with retry")
print("-" * 60)
try:
    result = pad.execute_flow(
        flow_name="ExampleFlow",
        input_variables={"inputParam1": "retry-demo", "inputParam2": 1},
        timeout=120,
        retry_count=2,
    )
    print(f"  Status: {result.status}")
    print(f"  Duration: {result.duration:.2f}s")
    print(f"  Execution ID: {result.execution_id}")
except Exception as exc:
    print(f"  Unexpected error: {exc}")
print()

print("Case 2: Execute an invalid flow to see failure handling")
print("-" * 60)
try:
    result = pad.execute_flow(
        flow_name="FlowThatDoesNotExist",
        timeout=30,
        retry_count=1,
    )
    print(f"  Status: {result.status}")
    print(f"  Error: {result.error}")
except Exception as exc:
    print(f"  Caught exception: {exc}")
print()

print("Case 3: Validate before execution (recommended)")
print("-" * 60)
validation = pad.validate_flow("ExampleFlow")
print(f"  Valid: {validation.get('valid')}")
print(f"  Errors: {len(validation.get('errors', []))}")
print(f"  Warnings: {len(validation.get('warnings', []))}")
print()

print("=" * 60)
print("✓ Lesson complete")
print("=" * 60)
print()

print("💡 EXERCISE:")
print("1. Wrap execute_flow in a reusable try/except helper")
print("2. Add fallback logic when flow execution fails")
print("3. Retry with different input values on failure")
