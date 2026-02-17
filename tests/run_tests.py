"""
Test Runner for Reporting and Assertions
Runs all tests and generates comprehensive test report
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_section(text):
    """Print formatted section"""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70)


def run_tests():
    """Run all tests and display results"""
    
    print_header("PAD FRAMEWORK - COMPREHENSIVE TEST SUITE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    
    # Test files to run
    test_files = [
        ("Reporting System Tests", "tests/test_reporting.py"),
        ("Assertion Framework Tests", "tests/test_assertions.py"),
        ("Integration Tests", "tests/test_integration.py")
    ]
    
    results = []
    total_start = time.time()
    
    for test_name, test_file in test_files:
        print_section(test_name)
        print(f"Running: {test_file}")
        
        start_time = time.time()
        
        # Run pytest
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_file,
                "-v",
                "--tb=short",
                "--color=yes"
            ],
            capture_output=False,
            cwd=Path(__file__).parent
        )
        
        elapsed = time.time() - start_time
        
        results.append({
            "name": test_name,
            "file": test_file,
            "passed": result.returncode == 0,
            "duration": elapsed
        })
        
        print(f"\nCompleted in {elapsed:.2f}s")
    
    total_elapsed = time.time() - total_start
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    
    print(f"Total Test Suites: {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Total Time: {total_elapsed:.2f}s")
    
    print("\nDetailed Results:")
    print("-" * 70)
    
    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        print(f"{status:8} | {result['name']:35} | {result['duration']:6.2f}s")
    
    print("-" * 70)
    
    # Overall result
    if failed_count == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\nReporting and Assertion frameworks are working correctly!")
        return 0
    else:
        print(f"\n✗ {failed_count} TEST SUITE(S) FAILED")
        print("\nPlease review the errors above.")
        return 1


def check_dependencies():
    """Check if pytest is installed"""
    try:
        import pytest
        print(f"pytest version: {pytest.__version__}")
        return True
    except ImportError:
        print("ERROR: pytest is not installed")
        print("\nPlease install it with:")
        print("  pip install pytest")
        return False


def main():
    """Main entry point"""
    print_header("CHECKING DEPENDENCIES")
    
    if not check_dependencies():
        return 1
    
    # Run tests
    exit_code = run_tests()
    
    # Final message
    print("\n" + "="*70)
    if exit_code == 0:
        print("  ✓ TEST RUN COMPLETE - ALL TESTS PASSED")
    else:
        print("  ✗ TEST RUN COMPLETE - SOME TESTS FAILED")
    print("="*70 + "\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
