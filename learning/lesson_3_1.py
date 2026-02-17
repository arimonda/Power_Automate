"""
Lesson 3.1: Performance Monitoring
Learn how to track and analyze performance
"""

from pad_framework import PADFramework
import time

print("="*60)
print("LESSON 3.1: Performance Monitoring")
print("="*60)
print()

pad = PADFramework()

# Execute flow multiple times
flow_name = "ExampleFlow"
executions = 5

print(f"Running '{flow_name}' {executions} times...")
print("-"*40)

for i in range(executions):
    print(f"Execution {i+1}/{executions}...", end=" ")
    
    result = pad.execute_flow(
        flow_name,
        {"inputParam1": f"Test {i+1}", "inputParam2": i+1}
    )
    
    print(f"✓ Duration: {result.duration:.2f}s")
    time.sleep(0.5)  # Small delay between executions

# Get performance statistics
print()
print("="*60)
print("PERFORMANCE STATISTICS")
print("="*60)

stats = pad.get_performance_stats(flow_name)

if stats:
    print(f"\nFlow: {flow_name}")
    print(f"  Total Executions: {stats['execution_count']}")
    print(f"  Average Duration: {stats['avg_duration']:.2f}s")
    print(f"  Fastest: {stats['min_duration']:.2f}s")
    print(f"  Slowest: {stats['max_duration']:.2f}s")
    print(f"  Avg Memory Usage: {stats['avg_memory_delta_mb']:.2f}MB")
    print(f"  Max Memory Usage: {stats['max_memory_delta_mb']:.2f}MB")
    print(f"  Last Execution: {stats['last_execution']}")
    
    # Performance analysis
    print("\nPerformance Analysis:")
    if stats['avg_duration'] < 1:
        print("  ✓ Excellent performance! (<1s average)")
    elif stats['avg_duration'] < 5:
        print("  ✓ Good performance (1-5s average)")
    elif stats['avg_duration'] < 10:
        print("  ⚠ Acceptable performance (5-10s average)")
    else:
        print("  ⚠ Consider optimization (>10s average)")
    
    if stats['max_memory_delta_mb'] > 100:
        print("  ⚠ High memory usage detected!")
    else:
        print("  ✓ Memory usage is acceptable")
else:
    print("No statistics available")

# System-wide statistics
print("\n" + "="*60)
print("SYSTEM SUMMARY")
print("="*60)

summary = pad.performance_monitor.get_summary()
print(f"  Total Flows Tracked: {summary['total_flows_tracked']}")
print(f"  Total Executions: {summary['total_executions']}")
print(f"  System CPU: {summary['system_cpu_percent']}%")
print(f"  System Memory: {summary['system_memory_percent']}%")
print(f"  Disk Usage: {summary['disk_usage_percent']}%")

print()
print("="*60)

# EXERCISE
print("\n💡 EXERCISE:")
print("1. Run the flow 10 times instead of 5")
print("2. Add alerts for slow executions (>2s)")
print("3. Create a function to export stats to a file")
print()

# CHALLENGE
print("🎯 CHALLENGE:")
print("Create a performance report comparing multiple flows!")
