"""
Lesson 1.3: Your First Script
Learn the basics of using the PAD Framework
"""

from pad_framework import PADFramework

print("="*60)
print("LESSON 1.3: Your First Script")
print("="*60)
print()

# Step 1: Create framework instance
print("Step 1: Initializing framework...")
pad = PADFramework()
print("✓ Framework ready!")
print()

# Step 2: Check health
print("Step 2: Checking health...")
health = pad.get_health_status()
print(f"  Status: {health['status']}")
print(f"  Version: {health['version']}")
print(f"  Flows Available: {health['flows_available']}")
print()

# Step 3: List available flows
print("Step 3: Listing flows...")
flows = pad.list_flows()
print(f"  Found {len(flows)} flows:")
for i, flow in enumerate(flows, 1):
    print(f"    {i}. {flow}")
print()

print("="*60)
print("✓ Script completed successfully!")
print("="*60)
print()

# EXERCISE: Try modifying this script!
# 1. Add a search for flows containing "Example"
# 2. Print the total number of active schedules
# 3. Add your own message at the end

print("💡 TIP: Modify this script to practice!")
print("   Try adding pad.list_flows(search_pattern='Example')")
