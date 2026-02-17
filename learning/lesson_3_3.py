"""
Lesson 3.3: Integrations
Learn how to call external integrations from the framework.
"""

from pad_framework import PADFramework

print("=" * 60)
print("LESSON 3.3: Integrations")
print("=" * 60)
print()

pad = PADFramework()

print("Listing available integrations...")
print("-" * 60)
try:
    integrations = pad.integration_manager.list_integrations()
    print(f"  Found {len(integrations)} integration(s): {integrations}")
except Exception as exc:
    print(f"  Could not list integrations: {exc}")
print()

print("Example integration call patterns")
print("-" * 60)
print("1) Email integration (example)")
print("   pad.integrate('email', to='user@example.com', subject='Hello', body='Test')")
print()
print("2) API integration (example)")
print("   pad.integrate('api', method='GET', url='https://example.com/api/status')")
print()
print("3) Database integration (example)")
print("   pad.integrate('database', operation='query', sql='SELECT 1')")
print()

print("Running a safe sample call with graceful error handling...")
try:
    response = pad.integrate("api", method="GET", url="https://httpbin.org/get")
    print(f"  Response: {response}")
except Exception as exc:
    print(f"  Integration call failed (expected in some setups): {exc}")

print()
print("=" * 60)
print("✓ Lesson complete")
print("=" * 60)
print()

print("💡 EXERCISE:")
print("1. Register a mock integration and call it")
print("2. Add retry logic around integration failures")
print("3. Log request/response details for troubleshooting")
