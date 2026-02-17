"""
Flow Executor
Executes Power Automate Desktop flows
"""

import subprocess
import time
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class FlowExecutionResult:
    """Result of flow execution"""
    flow_name: str
    status: str  # success, failed, timeout, cancelled
    start_time: datetime
    end_time: datetime
    duration: float
    output: Dict[str, Any]
    error: Optional[str] = None
    execution_id: str = ""
    
    def __post_init__(self):
        if not self.execution_id:
            self.execution_id = str(uuid.uuid4())


class FlowExecutor:
    """Executes PAD flows"""
    
    # PAD CLI path (adjust based on installation)
    PAD_CONSOLE_PATH = r"C:\Program Files (x86)\Power Automate Desktop\PAD.Console.Host.exe"
    
    def __init__(self, config, logger):
        """
        Initialize Flow Executor
        
        Args:
            config: Configuration object
            logger: Logger object
        """
        self.config = config
        self.logger = logger
        self.active_executions = {}
        self.scheduled_flows = {}
        
    def execute(
        self,
        flow_name: str,
        input_variables: Dict[str, Any],
        timeout: Optional[int] = None,
        retry_count: int = 0
    ) -> FlowExecutionResult:
        """
        Execute a flow
        
        Args:
            flow_name: Name of the flow to execute
            input_variables: Input variables for the flow
            timeout: Execution timeout in seconds
            retry_count: Number of retry attempts
            
        Returns:
            FlowExecutionResult
        """
        execution_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        self.logger.info(f"Starting flow execution: {flow_name} (ID: {execution_id})")
        
        try:
            # Prepare execution
            timeout = timeout or self.config.get("execution.default_timeout", 300)
            
            # Execute with retry if configured
            if retry_count > 0:
                result = self._execute_with_retry(
                    flow_name,
                    input_variables,
                    timeout,
                    retry_count
                )
            else:
                result = self._execute_flow(flow_name, input_variables, timeout)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return FlowExecutionResult(
                flow_name=flow_name,
                status="success",
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                output=result,
                execution_id=execution_id
            )
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.error(f"Flow execution failed: {flow_name} - {str(e)}")
            
            return FlowExecutionResult(
                flow_name=flow_name,
                status="failed",
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                output={},
                error=str(e),
                execution_id=execution_id
            )
    
    def _execute_flow(
        self,
        flow_name: str,
        input_variables: Dict[str, Any],
        timeout: int
    ) -> Dict[str, Any]:
        """
        Internal method to execute flow
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            timeout: Timeout in seconds
            
        Returns:
            Execution output
        """
        self.logger.debug(f"Executing flow: {flow_name}")
        
        # Build command
        cmd = self._build_command(flow_name, input_variables)
        
        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=True
            )
            
            output = {
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
            if result.returncode != 0:
                raise Exception(f"Flow execution failed with code {result.returncode}: {result.stderr}")
            
            return output
            
        except subprocess.TimeoutExpired:
            raise Exception(f"Flow execution timed out after {timeout} seconds")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _execute_with_retry(
        self,
        flow_name: str,
        input_variables: Dict[str, Any],
        timeout: int,
        retry_count: int
    ) -> Dict[str, Any]:
        """
        Execute flow with retry logic
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            timeout: Timeout in seconds
            retry_count: Number of retries
            
        Returns:
            Execution output
        """
        return self._execute_flow(flow_name, input_variables, timeout)
    
    def _build_command(self, flow_name: str, input_variables: Dict[str, Any]) -> List[str]:
        """
        Build PAD execution command
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            
        Returns:
            Command list
        """
        # Note: Adjust command structure based on actual PAD CLI requirements
        cmd = [self.PAD_CONSOLE_PATH]
        
        # Add flow name
        cmd.extend(["-flow", flow_name])
        
        # Add input variables
        for key, value in input_variables.items():
            cmd.extend(["-var", f"{key}={value}"])
        
        return cmd
    
    def execute_async(
        self,
        flow_name: str,
        input_variables: Dict[str, Any],
        callback: Optional[callable] = None
    ) -> str:
        """
        Execute flow asynchronously
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            callback: Optional callback function
            
        Returns:
            Execution ID
        """
        execution_id = str(uuid.uuid4())
        
        # Implementation would use threading or asyncio
        # Placeholder for now
        self.logger.info(f"Async execution started: {flow_name} (ID: {execution_id})")
        
        return execution_id
    
    def cancel_execution(self, execution_id: str) -> bool:
        """
        Cancel a running execution
        
        Args:
            execution_id: ID of the execution to cancel
            
        Returns:
            Success status
        """
        if execution_id in self.active_executions:
            # Implementation would cancel the process
            self.logger.info(f"Cancelled execution: {execution_id}")
            return True
        
        return False
    
    def schedule(
        self,
        flow_name: str,
        schedule: str,
        input_variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a flow execution
        
        Args:
            flow_name: Name of the flow
            schedule: Schedule expression
            input_variables: Input variables
            
        Returns:
            Schedule ID
        """
        schedule_id = str(uuid.uuid4())
        
        self.scheduled_flows[schedule_id] = {
            "flow_name": flow_name,
            "schedule": schedule,
            "input_variables": input_variables or {},
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }
        
        self.logger.info(f"Flow scheduled: {flow_name} (ID: {schedule_id})")
        return schedule_id
    
    def cancel_schedule(self, schedule_id: str) -> bool:
        """
        Cancel a scheduled flow
        
        Args:
            schedule_id: ID of the schedule
            
        Returns:
            Success status
        """
        if schedule_id in self.scheduled_flows:
            del self.scheduled_flows[schedule_id]
            self.logger.info(f"Schedule cancelled: {schedule_id}")
            return True
        
        return False
    
    def get_active_schedules_count(self) -> int:
        """Get count of active schedules"""
        return len(self.scheduled_flows)
    
    def cleanup(self) -> None:
        """Cleanup executor resources"""
        # Cancel all active executions
        for execution_id in list(self.active_executions.keys()):
            self.cancel_execution(execution_id)
        
        self.logger.info("Flow executor cleanup completed")
