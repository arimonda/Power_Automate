"""
Lesson 1.2: Installation Check
Verify environment and framework setup.
"""

import os
import platform
import sys

from pad_framework import PADFramework

print("=" * 60)
print("LESSON 1.2: Installation Check")
print("=" * 60)
print()

print("Environment:")
print(f"  Python version: {sys.version.split()[0]}")
print(f"  Platform: {platform.system()} {platform.release()}")
print(f"  Working directory: {os.getcwd()}")
print()

print("Checking framework initialization...")
pad = PADFramework()
print("✓ PADFramework imported and initialized")
print()

print("Checking core operations...")
flows = pad.list_flows()
health = pad.get_health_status()
print(f"✓ list_flows() returned {len(flows)} flow(s)")
print(f"✓ get_health_status(): {health['status']}")
print()

print("Checking folder paths from config...")
for key in ["flows", "logs", "data", "configs", "tests"]:
    path = pad.config.get_path(key)
    exists = path.exists()
    print(f"  {key:8} -> {path} (exists: {exists})")
print()

print("=" * 60)
print("✓ Installation check completed")
print("=" * 60)
print()

print("💡 EXERCISE:")
print("1. Open configs/config.yaml and change logging level")
print("2. Re-run this script to verify settings are loaded")
print("3. Create a new flow with pad.create_flow('MyFirstFlow')")
