"""
Lesson 3.2: Flow Scheduling
Learn how to schedule and cancel recurring flow executions.
"""

from pad_framework import PADFramework

print("=" * 60)
print("LESSON 3.2: Flow Scheduling")
print("=" * 60)
print()

pad = PADFramework()
flow_name = "ExampleFlow"
schedule = "*/30 * * * *"  # Every 30 minutes

print(f"Scheduling flow '{flow_name}' with cron: {schedule}")
print("-" * 60)

try:
    schedule_id = pad.schedule_flow(
        flow_name=flow_name,
        schedule=schedule,
        input_variables={"scheduled_run": True},
    )
    print("✓ Schedule created")
    print(f"  Schedule ID: {schedule_id}")
except Exception as exc:
    print(f"✗ Failed to schedule flow: {exc}")
    schedule_id = None

print()
print("Current health status:")
health = pad.get_health_status()
print(f"  Active schedules: {health.get('active_schedules', 0)}")
print()

if schedule_id:
    print("Cancelling schedule for cleanup...")
    cancelled = pad.cancel_schedule(schedule_id)
    print(f"  Cancelled: {cancelled}")
    print()

print("=" * 60)
print("✓ Lesson complete")
print("=" * 60)
print()

print("💡 EXERCISE:")
print("1. Schedule two different flows with different intervals")
print("2. Store schedule IDs in a file")
print("3. Build a cleanup script to cancel old schedules")
