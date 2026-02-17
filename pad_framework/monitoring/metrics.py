"""
Metrics System
Prometheus-compatible metrics collection
"""

from typing import Dict, Any, Optional
from prometheus_client import (
    Counter, Histogram, Gauge, Summary,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)
from datetime import datetime
import time


class MetricsCollector:
    """
    Collects and exposes metrics in Prometheus format
    """
    
    def __init__(self, registry: Optional[CollectorRegistry] = None):
        """
        Initialize metrics collector
        
        Args:
            registry: Optional custom registry
        """
        self.registry = registry or CollectorRegistry()
        
        # Flow execution metrics
        self.flow_executions_total = Counter(
            'pad_flow_executions_total',
            'Total number of flow executions',
            ['flow_name', 'status'],
            registry=self.registry
        )
        
        self.flow_execution_duration = Histogram(
            'pad_flow_execution_duration_seconds',
            'Flow execution duration in seconds',
            ['flow_name'],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0),
            registry=self.registry
        )
        
        self.flow_execution_errors = Counter(
            'pad_flow_execution_errors_total',
            'Total number of flow execution errors',
            ['flow_name', 'error_type'],
            registry=self.registry
        )
        
        self.active_flow_executions = Gauge(
            'pad_active_flow_executions',
            'Number of currently executing flows',
            registry=self.registry
        )
        
        # Flow metrics
        self.flows_registered = Gauge(
            'pad_flows_registered_total',
            'Total number of registered flows',
            registry=self.registry
        )
        
        self.flow_validation_failures = Counter(
            'pad_flow_validation_failures_total',
            'Total number of flow validation failures',
            ['flow_name'],
            registry=self.registry
        )
        
        # Schedule metrics
        self.schedules_active = Gauge(
            'pad_schedules_active',
            'Number of active schedules',
            registry=self.registry
        )
        
        self.schedule_executions = Counter(
            'pad_schedule_executions_total',
            'Total number of scheduled executions',
            ['flow_name', 'status'],
            registry=self.registry
        )
        
        # Resource metrics
        self.memory_usage_bytes = Gauge(
            'pad_memory_usage_bytes',
            'Memory usage in bytes',
            ['type'],
            registry=self.registry
        )
        
        self.cpu_usage_percent = Gauge(
            'pad_cpu_usage_percent',
            'CPU usage percentage',
            registry=self.registry
        )
        
        # Integration metrics
        self.integration_calls = Counter(
            'pad_integration_calls_total',
            'Total number of integration calls',
            ['integration', 'operation', 'status'],
            registry=self.registry
        )
        
        self.integration_duration = Histogram(
            'pad_integration_duration_seconds',
            'Integration call duration',
            ['integration', 'operation'],
            registry=self.registry
        )
        
        # Performance metrics
        self.retry_attempts = Counter(
            'pad_retry_attempts_total',
            'Total number of retry attempts',
            ['flow_name'],
            registry=self.registry
        )
        
        self.timeout_occurrences = Counter(
            'pad_timeout_occurrences_total',
            'Total number of timeout occurrences',
            ['flow_name'],
            registry=self.registry
        )
        
        # Framework metrics
        self.framework_uptime_seconds = Gauge(
            'pad_framework_uptime_seconds',
            'Framework uptime in seconds',
            registry=self.registry
        )
        
        self.framework_info = Gauge(
            'pad_framework_info',
            'Framework information',
            ['version', 'python_version'],
            registry=self.registry
        )
        
        # Track start time
        self.start_time = time.time()
    
    def record_flow_execution(
        self,
        flow_name: str,
        status: str,
        duration: float,
        error_type: Optional[str] = None
    ) -> None:
        """
        Record flow execution metrics
        
        Args:
            flow_name: Name of the flow
            status: Execution status (success, failed, timeout)
            duration: Execution duration in seconds
            error_type: Type of error if failed
        """
        self.flow_executions_total.labels(
            flow_name=flow_name,
            status=status
        ).inc()
        
        self.flow_execution_duration.labels(
            flow_name=flow_name
        ).observe(duration)
        
        if error_type:
            self.flow_execution_errors.labels(
                flow_name=flow_name,
                error_type=error_type
            ).inc()
    
    def record_validation_failure(self, flow_name: str) -> None:
        """Record flow validation failure"""
        self.flow_validation_failures.labels(
            flow_name=flow_name
        ).inc()
    
    def set_active_executions(self, count: int) -> None:
        """Set number of active executions"""
        self.active_flow_executions.set(count)
    
    def set_registered_flows(self, count: int) -> None:
        """Set number of registered flows"""
        self.flows_registered.set(count)
    
    def set_active_schedules(self, count: int) -> None:
        """Set number of active schedules"""
        self.schedules_active.set(count)
    
    def record_integration_call(
        self,
        integration: str,
        operation: str,
        status: str,
        duration: float
    ) -> None:
        """
        Record integration call metrics
        
        Args:
            integration: Integration name
            operation: Operation name
            status: Call status
            duration: Call duration in seconds
        """
        self.integration_calls.labels(
            integration=integration,
            operation=operation,
            status=status
        ).inc()
        
        self.integration_duration.labels(
            integration=integration,
            operation=operation
        ).observe(duration)
    
    def record_retry_attempt(self, flow_name: str) -> None:
        """Record retry attempt"""
        self.retry_attempts.labels(flow_name=flow_name).inc()
    
    def record_timeout(self, flow_name: str) -> None:
        """Record timeout occurrence"""
        self.timeout_occurrences.labels(flow_name=flow_name).inc()
    
    def update_resource_metrics(
        self,
        memory_used: int,
        memory_available: int,
        cpu_percent: float
    ) -> None:
        """
        Update resource usage metrics
        
        Args:
            memory_used: Used memory in bytes
            memory_available: Available memory in bytes
            cpu_percent: CPU usage percentage
        """
        self.memory_usage_bytes.labels(type='used').set(memory_used)
        self.memory_usage_bytes.labels(type='available').set(memory_available)
        self.cpu_usage_percent.set(cpu_percent)
    
    def update_uptime(self) -> None:
        """Update framework uptime"""
        uptime = time.time() - self.start_time
        self.framework_uptime_seconds.set(uptime)
    
    def set_framework_info(self, version: str, python_version: str) -> None:
        """Set framework information"""
        self.framework_info.labels(
            version=version,
            python_version=python_version
        ).set(1)
    
    def export_metrics(self) -> bytes:
        """
        Export metrics in Prometheus format
        
        Returns:
            Metrics in Prometheus text format
        """
        return generate_latest(self.registry)
    
    def get_content_type(self) -> str:
        """Get content type for metrics endpoint"""
        return CONTENT_TYPE_LATEST


class MetricsMiddleware:
    """
    Middleware for automatic metrics collection
    """
    
    def __init__(self, metrics_collector: MetricsCollector):
        """
        Initialize middleware
        
        Args:
            metrics_collector: MetricsCollector instance
        """
        self.metrics = metrics_collector
    
    def before_execution(self, flow_name: str) -> Dict[str, Any]:
        """
        Called before flow execution
        
        Args:
            flow_name: Name of the flow
            
        Returns:
            Context dictionary
        """
        return {
            "start_time": time.time(),
            "flow_name": flow_name
        }
    
    def after_execution(
        self,
        context: Dict[str, Any],
        status: str,
        error_type: Optional[str] = None
    ) -> None:
        """
        Called after flow execution
        
        Args:
            context: Context from before_execution
            status: Execution status
            error_type: Error type if failed
        """
        duration = time.time() - context["start_time"]
        
        self.metrics.record_flow_execution(
            flow_name=context["flow_name"],
            status=status,
            duration=duration,
            error_type=error_type
        )


# Singleton metrics collector
_default_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get default metrics collector"""
    global _default_collector
    if _default_collector is None:
        _default_collector = MetricsCollector()
    return _default_collector


def record_execution_metrics(
    flow_name: str,
    status: str,
    duration: float,
    error_type: Optional[str] = None
) -> None:
    """
    Convenience function to record execution metrics
    
    Args:
        flow_name: Name of the flow
        status: Execution status
        duration: Execution duration
        error_type: Error type if failed
    """
    collector = get_metrics_collector()
    collector.record_flow_execution(flow_name, status, duration, error_type)
