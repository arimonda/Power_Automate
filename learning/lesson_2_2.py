"""
Lesson 2.2: Creating Flows
Learn how to create and validate flows
"""

from pad_framework import PADFramework

print("="*60)
print("LESSON 2.2: Creating Flows")
print("="*60)
print()

pad = PADFramework()

# Create a new flow
flow_name = "MyLearningFlow"
print(f"Creating flow: {flow_name}")
print("-"*40)

success = pad.create_flow(flow_name, template="basic")

if success:
    print(f"✓ Flow '{flow_name}' created successfully!")
    print()
    
    # Validate the flow
    print("Validating flow...")
    validation = pad.validate_flow(flow_name)
    
    if validation["valid"]:
        print("✓ Flow is valid!")
        print(f"  Info: {validation['info']}")
    else:
        print("✗ Flow has errors:")
        for error in validation["errors"]:
            print(f"  - {error}")
    
    if validation["warnings"]:
        print("⚠ Warnings:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")
    
    print()
    
    # List all flows to confirm
    print("All available flows:")
    flows = pad.list_flows()
    for i, flow in enumerate(flows, 1):
        mark = "✓" if flow == flow_name else " "
        print(f"  {mark} {i}. {flow}")
else:
    print(f"✗ Failed to create flow '{flow_name}'")

print()
print("="*60)

# EXERCISE
print("\n💡 EXERCISE:")
print("1. Create a flow with your own name")
print("2. Validate it and check for any warnings")
print("3. Look at the JSON file in flows/ folder")
print()

# CLEANUP OPTION
cleanup = input("Delete the learning flow? (y/n): ")
if cleanup.lower() == 'y':
    pad.flow_manager.delete_flow(flow_name)
    print(f"✓ Deleted {flow_name}")
