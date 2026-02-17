"""
Asynchronous Flow Executor
Real async/await support for concurrent flow execution
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from datetime import datetime
import uuid

from .flow_executor import FlowExecutor, FlowExecutionResult


class AsyncFlowExecutor:
    """
    Asynchronous flow executor with real async/await support
    """
    
    def __init__(
        self,
        flow_executor: FlowExecutor,
        max_workers: int = 5,
        max_concurrent: int = 10
    ):
        """
        Initialize async executor
        
        Args:
            flow_executor: Underlying flow executor
            max_workers: Maximum number of worker threads
            max_concurrent: Maximum concurrent executions
        """
        self.flow_executor = flow_executor
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.logger = flow_executor.logger
    
    async def execute_async(
        self,
        flow_name: str,
        input_variables: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        retry_count: int = 0,
        callback: Optional[Callable] = None
    ) -> FlowExecutionResult:
        """
        Execute flow asynchronously
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            timeout: Execution timeout
            retry_count: Retry attempts
            callback: Optional callback function
            
        Returns:
            FlowExecutionResult
        """
        async with self.semaphore:
            execution_id = str(uuid.uuid4())
            
            try:
                self.logger.info(f"Async execution started: {flow_name} (ID: {execution_id})")
                
                # Run in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    self._execute_sync,
                    flow_name,
                    input_variables or {},
                    timeout,
                    retry_count
                )
                
                # Call callback if provided
                if callback:
                    await self._call_callback(callback, result)
                
                return result
                
            except Exception as e:
                self.logger.error(f"Async execution failed: {str(e)}")
                raise
    
    def _execute_sync(
        self,
        flow_name: str,
        input_variables: Dict[str, Any],
        timeout: Optional[int],
        retry_count: int
    ) -> FlowExecutionResult:
        """
        Synchronous execution wrapper
        
        Args:
            flow_name: Name of the flow
            input_variables: Input variables
            timeout: Timeout in seconds
            retry_count: Retry attempts
            
        Returns:
            FlowExecutionResult
        """
        return self.flow_executor.execute(
            flow_name=flow_name,
            input_variables=input_variables,
            timeout=timeout,
            retry_count=retry_count
        )
    
    async def _call_callback(
        self,
        callback: Callable,
        result: FlowExecutionResult
    ) -> None:
        """
        Call callback function
        
        Args:
            callback: Callback function
            result: Execution result
        """
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(result)
            else:
                callback(result)
        except Exception as e:
            self.logger.error(f"Callback failed: {str(e)}")
    
    async def execute_batch(
        self,
        executions: List[Dict[str, Any]],
        fail_fast: bool = False
    ) -> List[FlowExecutionResult]:
        """
        Execute multiple flows in parallel
        
        Args:
            executions: List of execution configurations
            fail_fast: Stop on first failure
            
        Returns:
            List of execution results
        """
        tasks = []
        
        for exec_config in executions:
            task = self.execute_async(
                flow_name=exec_config['flow_name'],
                input_variables=exec_config.get('input_variables'),
                timeout=exec_config.get('timeout'),
                retry_count=exec_config.get('retry_count', 0)
            )
            tasks.append(task)
        
        if fail_fast:
            # Stop on first exception
            results = await asyncio.gather(*tasks)
        else:
            # Continue even if some fail
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def execute_with_dependencies(
        self,
        flow_graph: Dict[str, Dict[str, Any]]
    ) -> Dict[str, FlowExecutionResult]:
        """
        Execute flows respecting dependencies (DAG)
        
        Args:
            flow_graph: Dictionary mapping flow names to their config and dependencies
                Example: {
                    "flow1": {"dependencies": []},
                    "flow2": {"dependencies": ["flow1"]},
                    "flow3": {"dependencies": ["flow1", "flow2"]}
                }
        
        Returns:
            Dictionary mapping flow names to results
        """
        results = {}
        remaining = set(flow_graph.keys())
        
        while remaining:
            # Find flows that can be executed now
            ready = [
                flow_name for flow_name in remaining
                if all(
                    dep in results
                    for dep in flow_graph[flow_name].get('dependencies', [])
                )
            ]
            
            if not ready:
                raise ValueError("Circular dependency detected in flow graph")
            
            # Execute ready flows in parallel
            tasks = []
            for flow_name in ready:
                config = flow_graph[flow_name]
                task = self.execute_async(
                    flow_name=flow_name,
                    input_variables=config.get('input_variables'),
                    timeout=config.get('timeout'),
                    retry_count=config.get('retry_count', 0)
                )
                tasks.append((flow_name, task))
            
            # Wait for all ready flows to complete
            for flow_name, task in tasks:
                results[flow_name] = await task
                remaining.remove(flow_name)
        
        return results
    
    async def execute_pipeline(
        self,
        flows: List[Dict[str, Any]],
        pass_output: bool = True
    ) -> List[FlowExecutionResult]:
        """
        Execute flows in sequence as a pipeline
        
        Args:
            flows: List of flow configurations
            pass_output: Pass output of each flow to next
            
        Returns:
            List of execution results
        """
        results = []
        current_input = {}
        
        for flow_config in flows:
            if pass_output and results:
                # Use output from previous flow
                current_input = results[-1].output
            else:
                current_input = flow_config.get('input_variables', {})
            
            result = await self.execute_async(
                flow_name=flow_config['flow_name'],
                input_variables=current_input,
                timeout=flow_config.get('timeout'),
                retry_count=flow_config.get('retry_count', 0)
            )
            
            results.append(result)
            
            # Stop pipeline if flow failed
            if result.status != "success":
                self.logger.warning(f"Pipeline stopped at {flow_config['flow_name']}")
                break
        
        return results
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """
        Cancel a running async execution
        
        Args:
            execution_id: Execution ID to cancel
            
        Returns:
            Success status
        """
        if execution_id in self.active_tasks:
            task = self.active_tasks[execution_id]
            task.cancel()
            del self.active_tasks[execution_id]
            self.logger.info(f"Cancelled execution: {execution_id}")
            return True
        return False
    
    def cleanup(self) -> None:
        """Cleanup async executor resources"""
        self.logger.info("Cleaning up async executor...")
        
        # Cancel all active tasks
        for execution_id in list(self.active_tasks.keys()):
            self.cancel_execution(execution_id)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        self.logger.info("Async executor cleanup completed")


# Convenience functions

async def execute_flows_parallel(
    executor: AsyncFlowExecutor,
    flow_names: List[str],
    **kwargs
) -> List[FlowExecutionResult]:
    """
    Execute multiple flows in parallel
    
    Args:
        executor: AsyncFlowExecutor instance
        flow_names: List of flow names
        **kwargs: Common execution parameters
        
    Returns:
        List of execution results
    """
    executions = [
        {"flow_name": name, **kwargs}
        for name in flow_names
    ]
    return await executor.execute_batch(executions)


async def execute_flows_sequential(
    executor: AsyncFlowExecutor,
    flow_names: List[str],
    **kwargs
) -> List[FlowExecutionResult]:
    """
    Execute multiple flows sequentially
    
    Args:
        executor: AsyncFlowExecutor instance
        flow_names: List of flow names
        **kwargs: Common execution parameters
        
    Returns:
        List of execution results
    """
    results = []
    for flow_name in flow_names:
        result = await executor.execute_async(
            flow_name=flow_name,
            **kwargs
        )
        results.append(result)
        
        # Stop on failure
        if result.status != "success":
            break
    
    return results
