"""
Performance Monitor
Monitors and tracks performance metrics
"""

import time
import psutil
from typing import Dict, Any, Optional
from contextlib import contextmanager
from datetime import datetime
from collections import defaultdict


class PerformanceMonitor:
    """Monitors framework performance"""
    
    def __init__(self, config, logger):
        """
        Initialize Performance Monitor
        
        Args:
            config: Configuration object
            logger: Logger object
        """
        self.config = config
        self.logger = logger
        self.metrics = defaultdict(list)
        self.enabled = config.get("performance.monitoring_enabled", True)
        
    @contextmanager
    def track(self, flow_name: str):
        """
        Context manager to track flow execution
        
        Args:
            flow_name: Name of the flow being tracked
        """
        if not self.enabled:
            yield
            return
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent(interval=0.1)
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent(interval=0.1)
            
            metrics = {
                "flow_name": flow_name,
                "timestamp": datetime.now().isoformat(),
                "duration": end_time - start_time,
                "memory_start_mb": start_memory,
                "memory_end_mb": end_memory,
                "memory_delta_mb": end_memory - start_memory,
                "cpu_start_percent": start_cpu,
                "cpu_end_percent": end_cpu
            }
            
            self.metrics[flow_name].append(metrics)
            
            # Log performance warnings
            if metrics["duration"] > 60:
                self.logger.warning(
                    f"Flow {flow_name} took {metrics['duration']:.2f}s"
                )
            
            if metrics["memory_delta_mb"] > 100:
                self.logger.warning(
                    f"Flow {flow_name} used {metrics['memory_delta_mb']:.2f}MB memory"
                )
    
    def get_stats(self, flow_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Args:
            flow_name: Optional flow name to filter stats
            
        Returns:
            Performance statistics
        """
        if flow_name:
            if flow_name not in self.metrics:
                return {}
            
            flow_metrics = self.metrics[flow_name]
            return self._calculate_stats(flow_metrics)
        
        # Return stats for all flows
        all_stats = {}
        for flow, metrics_list in self.metrics.items():
            all_stats[flow] = self._calculate_stats(metrics_list)
        
        return all_stats
    
    def _calculate_stats(self, metrics_list: list) -> Dict[str, Any]:
        """
        Calculate statistics from metrics list
        
        Args:
            metrics_list: List of metrics
            
        Returns:
            Calculated statistics
        """
        if not metrics_list:
            return {}
        
        durations = [m["duration"] for m in metrics_list]
        memory_deltas = [m["memory_delta_mb"] for m in metrics_list]
        
        return {
            "execution_count": len(metrics_list),
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "avg_memory_delta_mb": sum(memory_deltas) / len(memory_deltas),
            "max_memory_delta_mb": max(memory_deltas),
            "last_execution": metrics_list[-1]["timestamp"]
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get performance summary
        
        Returns:
            Summary statistics
        """
        total_executions = sum(len(m) for m in self.metrics.values())
        
        return {
            "total_flows_tracked": len(self.metrics),
            "total_executions": total_executions,
            "system_cpu_percent": psutil.cpu_percent(interval=0.1),
            "system_memory_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
    
    def cleanup(self) -> None:
        """Cleanup monitor resources"""
        self.logger.debug("Performance monitor cleanup completed")
