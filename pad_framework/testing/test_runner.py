"""
Test Runner
Framework testing utilities
"""

import pytest
from typing import Dict, Any, Optional
from pathlib import Path


class TestRunner:
    """Test runner for PAD Framework"""
    
    def __init__(self, config, logger):
        """
        Initialize Test Runner
        
        Args:
            config: Configuration object
            logger: Logger object
        """
        self.config = config
        self.logger = logger
        self.tests_path = config.get_path("tests")
        
    def run(
        self,
        test_pattern: Optional[str] = None,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run tests
        
        Args:
            test_pattern: Optional pattern to filter tests
            verbose: Enable verbose output
            
        Returns:
            Test results
        """
        self.logger.info("Running framework tests...")
        
        try:
            # Build pytest arguments
            args = [str(self.tests_path)]
            
            if test_pattern:
                args.extend(["-k", test_pattern])
            
            if verbose:
                args.append("-v")
            
            # Add coverage
            args.extend([
                "--cov=pad_framework",
                "--cov-report=term",
                "--cov-report=html"
            ])
            
            # Run tests
            exit_code = pytest.main(args)
            
            results = {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "message": "Tests passed" if exit_code == 0 else "Tests failed"
            }
            
            self.logger.info(f"Test run completed: {results['message']}")
            return results
            
        except Exception as e:
            self.logger.error(f"Error running tests: {str(e)}")
            return {
                "success": False,
                "exit_code": -1,
                "message": str(e)
            }
    
    def run_flow_test(self, flow_name: str) -> Dict[str, Any]:
        """
        Run tests for a specific flow
        
        Args:
            flow_name: Name of the flow to test
            
        Returns:
            Test results
        """
        self.logger.info(f"Running tests for flow: {flow_name}")
        return self.run(test_pattern=f"test_{flow_name}")
