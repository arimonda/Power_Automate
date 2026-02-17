"""
Lesson 1.1: Understanding the Framework
High-level introduction to PAD Framework components.
"""

from pad_framework import PADFramework

print("=" * 60)
print("LESSON 1.1: Understanding the Framework")
print("=" * 60)
print()

print("What is PAD Framework?")
print("  A Python framework to manage and execute Power Automate flows.")
print()

print("Main capabilities:")
print("  1. Create and manage flows")
print("  2. Execute flows with retry and timeout")
print("  3. Monitor performance")
print("  4. Run tests and generate reports")
print("  5. Integrate with external systems")
print()

print("Initializing framework...")
pad = PADFramework()
print("✓ Framework initialized")
print()

health = pad.get_health_status()
print("Health Check:")
print(f"  Status: {health['status']}")
print(f"  Version: {health['version']}")
print(f"  Flows available: {health['flows_available']}")
print(f"  Active schedules: {health['active_schedules']}")
print()

print("=" * 60)
print("✓ Lesson complete")
print("=" * 60)
print()

print("💡 EXERCISE:")
print("1. Run this script and inspect output")
print("2. Call pad.list_flows() and print each flow")
print("3. Call pad.get_performance_stats() and inspect data")
