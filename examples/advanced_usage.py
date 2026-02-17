"""
Advanced Usage Examples
Demonstrates advanced framework features
"""

from pad_framework import PADFramework, FlowConfig
from datetime import datetime, timedelta
import asyncio


def example_batch_execution():
    """Example: Execute multiple flows in batch"""
    print("=== Batch Execution Example ===")
    
    pad = PADFramework()
    
    flows_to_execute = [
        ("Flow1", {"param": "value1"}),
        ("Flow2", {"param": "value2"}),
        ("Flow3", {"param": "value3"}),
    ]
    
    results = []
    for flow_name, input_vars in flows_to_execute:
        result = pad.execute_flow(flow_name, input_vars)
        results.append(result)
        print(f"Executed {flow_name}: {result.status}")
    
    return results


def example_error_handling():
    """Example: Advanced error handling"""
    print("\n=== Error Handling Example ===")
    
    pad = PADFramework()
    
    try:
        result = pad.execute_flow(
            flow_name="RiskyFlow",
            input_variables={},
            retry_count=3
        )
        
        if result.status == "success":
            print("Flow completed successfully")
        else:
            print(f"Flow failed: {result.error}")
            
    except Exception as e:
        print(f"Caught exception: {str(e)}")
        # Handle error appropriately
        # - Log to monitoring system
        # - Send notification
        # - Trigger fallback flow


def example_conditional_execution():
    """Example: Conditional flow execution"""
    print("\n=== Conditional Execution Example ===")
    
    pad = PADFramework()
    
    # Execute flow based on conditions
    current_hour = datetime.now().hour
    
    if 9 <= current_hour <= 17:
        flow_name = "BusinessHoursFlow"
    else:
        flow_name = "AfterHoursFlow"
    
    print(f"Executing: {flow_name}")
    result = pad.execute_flow(flow_name, {})
    print(f"Result: {result.status}")


def example_data_pipeline():
    """Example: Build a data processing pipeline"""
    print("\n=== Data Pipeline Example ===")
    
    pad = PADFramework()
    
    pipeline = [
        ("ExtractData", {"source": "database"}),
        ("TransformData", {"rules": "standard"}),
        ("ValidateData", {"schema": "v1"}),
        ("LoadData", {"destination": "warehouse"}),
    ]
    
    for flow_name, input_vars in pipeline:
        print(f"Running: {flow_name}")
        result = pad.execute_flow(flow_name, input_vars)
        
        if result.status != "success":
            print(f"Pipeline failed at: {flow_name}")
            break
        
        # Pass output to next stage
        if "output" in result.output:
            input_vars = result.output["output"]
    
    print("Pipeline completed")


def example_monitoring_and_alerts():
    """Example: Monitor flows and trigger alerts"""
    print("\n=== Monitoring & Alerts Example ===")
    
    pad = PADFramework()
    
    # Execute flow
    result = pad.execute_flow("CriticalFlow", {})
    
    # Check performance
    stats = pad.get_performance_stats("CriticalFlow")
    
    if stats.get("avg_duration", 0) > 60:
        print("ALERT: Flow execution time exceeds threshold!")
        # Send notification
        pad.integrate("notification", 
                     message="Critical flow is slow",
                     severity="warning")
    
    # Check for failures
    if result.status == "failed":
        print("ALERT: Critical flow failed!")
        # Send urgent notification
        pad.integrate("notification",
                     message=f"Critical failure: {result.error}",
                     severity="critical")


def example_dynamic_flow_generation():
    """Example: Dynamically create and execute flows"""
    print("\n=== Dynamic Flow Generation Example ===")
    
    pad = PADFramework()
    
    # Create flow dynamically
    flow_name = f"DynamicFlow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    pad.create_flow(flow_name, template="basic")
    
    # Execute it
    result = pad.execute_flow(flow_name, {})
    print(f"Dynamic flow result: {result.status}")


def example_parallel_execution():
    """Example: Execute flows in parallel"""
    print("\n=== Parallel Execution Example ===")
    
    # Note: This would require async implementation
    pad = PADFramework()
    
    flows = ["Flow1", "Flow2", "Flow3"]
    
    print("Starting parallel execution...")
    # In a real implementation, use asyncio or threading
    for flow in flows:
        print(f"  Executing {flow} (async)")
        # result = await pad.execute_flow_async(flow, {})


def example_reporting():
    """Example: Generate execution reports"""
    print("\n=== Reporting Example ===")
    
    pad = PADFramework()
    
    # Execute some flows
    flows = ["ReportFlow1", "ReportFlow2"]
    results = []
    
    for flow in flows:
        result = pad.execute_flow(flow, {})
        results.append(result)
    
    # Generate report
    print("\n=== Execution Report ===")
    print(f"Total Flows: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r.status == 'success')}")
    print(f"Failed: {sum(1 for r in results if r.status == 'failed')}")
    print(f"Total Duration: {sum(r.duration for r in results):.2f}s")


def example_flow_chaining():
    """Example: Chain flows together"""
    print("\n=== Flow Chaining Example ===")
    
    pad = PADFramework()
    
    # Execute flows in sequence, passing output to input
    result1 = pad.execute_flow("Step1", {"input": "data"})
    
    if result1.status == "success":
        output1 = result1.output
        result2 = pad.execute_flow("Step2", output1)
        
        if result2.status == "success":
            output2 = result2.output
            result3 = pad.execute_flow("Step3", output2)
            
            print(f"Chain completed: {result3.status}")


if __name__ == "__main__":
    print("Power Automate Desktop Framework - Advanced Examples")
    print("=" * 50)
    
    try:
        # example_batch_execution()
        # example_error_handling()
        # example_conditional_execution()
        # example_data_pipeline()
        example_monitoring_and_alerts()
        # example_dynamic_flow_generation()
        # example_reporting()
        # example_flow_chaining()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
