"""
Main Framework Class
Central orchestration for Power Automate Desktop operations
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from .config import Config
from .exceptions import PADException, FlowExecutionError
from ..flows.flow_manager import FlowManager
from ..flows.flow_executor import FlowExecutor
from ..testing.test_runner import TestRunner
from ..utils.logger import Logger
from ..monitoring.performance_monitor import PerformanceMonitor
from ..integrations.integration_manager import IntegrationManager


class PADFramework:
    """
    Main framework class for Power Automate Desktop operations.
    Provides unified interface for all framework features.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PAD Framework
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = Config(config_path)
        self.logger = Logger(self.config)
        
        # Initialize core components
        self.flow_manager = FlowManager(self.config, self.logger)
        self.flow_executor = FlowExecutor(self.config, self.logger)
        self.test_runner = TestRunner(self.config, self.logger)
        self.performance_monitor = PerformanceMonitor(self.config, self.logger)
        self.integration_manager = IntegrationManager(self.config, self.logger)
        self.integration_manager.set_framework(self)
        
        self.logger.info("PAD Framework initialized successfully")
        
    def execute_flow(
        self,
        flow_name: str,
        input_variables: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        retry_count: int = 0
    ) -> 'FlowExecutionResult':
        """
        Execute a Power Automate Desktop flow
        
        Args:
            flow_name: Name of the flow to execute
            input_variables: Input variables for the flow
            timeout: Execution timeout in seconds
            retry_count: Number of retry attempts
            
        Returns:
            FlowExecutionResult object
        """
        self.logger.info(f"Executing flow: {flow_name}")
        
        try:
            with self.performance_monitor.track(flow_name):
                result = self.flow_executor.execute(
                    flow_name=flow_name,
                    input_variables=input_variables or {},
                    timeout=timeout,
                    retry_count=retry_count
                )
            
            self.logger.info(f"Flow {flow_name} completed: {result.status}")
            return result
            
        except Exception as e:
            self.logger.error(f"Flow execution failed: {str(e)}")
            raise FlowExecutionError(f"Failed to execute flow {flow_name}: {str(e)}")
    
    def list_flows(self, search_pattern: Optional[str] = None) -> List[str]:
        """
        List available flows
        
        Args:
            search_pattern: Optional search pattern to filter flows
            
        Returns:
            List of flow names
        """
        return self.flow_manager.list_flows(search_pattern)
    
    def validate_flow(self, flow_name: str) -> Dict[str, Any]:
        """
        Validate a flow configuration
        
        Args:
            flow_name: Name of the flow to validate
            
        Returns:
            Validation results
        """
        return self.flow_manager.validate_flow(flow_name)
    
    def run_tests(
        self,
        test_pattern: Optional[str] = None,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Run framework tests
        
        Args:
            test_pattern: Optional pattern to filter tests
            verbose: Enable verbose output
            
        Returns:
            Test results
        """
        self.logger.info("Running tests...")
        return self.test_runner.run(test_pattern, verbose)
    
    def get_performance_stats(self, flow_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Args:
            flow_name: Optional flow name to filter stats
            
        Returns:
            Performance statistics
        """
        return self.performance_monitor.get_stats(flow_name)
    
    def create_flow(self, flow_name: str, template: Optional[str] = None) -> bool:
        """
        Create a new flow from template
        
        Args:
            flow_name: Name for the new flow
            template: Optional template name
            
        Returns:
            Success status
        """
        return self.flow_manager.create_flow(flow_name, template)
    
    def export_flow(self, flow_name: str, output_path: str) -> bool:
        """
        Export a flow
        
        Args:
            flow_name: Name of the flow to export
            output_path: Path to export the flow
            
        Returns:
            Success status
        """
        return self.flow_manager.export_flow(flow_name, output_path)
    
    def import_flow(self, flow_path: str, flow_name: Optional[str] = None) -> bool:
        """
        Import a flow
        
        Args:
            flow_path: Path to the flow file
            flow_name: Optional name for the imported flow
            
        Returns:
            Success status
        """
        return self.flow_manager.import_flow(flow_path, flow_name)
    
    def schedule_flow(
        self,
        flow_name: str,
        schedule: str,
        input_variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a flow execution
        
        Args:
            flow_name: Name of the flow to schedule
            schedule: Schedule expression (cron-like)
            input_variables: Input variables for the flow
            
        Returns:
            Schedule ID
        """
        return self.flow_executor.schedule(flow_name, schedule, input_variables)
    
    def cancel_schedule(self, schedule_id: str) -> bool:
        """
        Cancel a scheduled flow
        
        Args:
            schedule_id: ID of the schedule to cancel
            
        Returns:
            Success status
        """
        return self.flow_executor.cancel_schedule(schedule_id)
    
    def get_logs(
        self,
        flow_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve logs
        
        Args:
            flow_name: Optional flow name filter
            start_time: Optional start time filter
            end_time: Optional end time filter
            level: Optional log level filter
            
        Returns:
            List of log entries
        """
        return self.logger.get_logs(flow_name, start_time, end_time, level)
    
    def integrate(self, service: str, **kwargs) -> Any:
        """
        Integrate with external services
        
        Args:
            service: Service name (email, database, api, etc.)
            **kwargs: Service-specific parameters
            
        Returns:
            Integration result
        """
        return self.integration_manager.integrate(service, **kwargs)
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get framework health status
        
        Returns:
            Health status information
        """
        return {
            "status": "healthy",
            "version": "1.0.0",
            "flows_available": len(self.list_flows()),
            "active_schedules": self.flow_executor.get_active_schedules_count(),
            "performance": self.performance_monitor.get_summary(),
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup(self) -> None:
        """Cleanup framework resources"""
        self.logger.info("Cleaning up framework resources...")
        self.flow_executor.cleanup()
        self.performance_monitor.cleanup()
        self.logger.info("Framework cleanup completed")
