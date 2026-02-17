"""
Basic Usage Examples
Demonstrates common framework operations
"""

from pad_framework import PADFramework


def example_execute_flow():
    """Example: Execute a flow"""
    print("=== Execute Flow Example ===")
    
    # Initialize framework
    pad = PADFramework()
    
    # Execute a flow
    result = pad.execute_flow(
        flow_name="MyTestFlow",
        input_variables={
            "param1": "value1",
            "param2": 42
        },
        timeout=60,
        retry_count=2
    )
    
    print(f"Flow Status: {result.status}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Output: {result.output}")


def example_list_flows():
    """Example: List all flows"""
    print("\n=== List Flows Example ===")
    
    pad = PADFramework()
    
    # List all flows
    flows = pad.list_flows()
    print(f"Available flows: {len(flows)}")
    for flow in flows:
        print(f"  - {flow}")
    
    # Search for specific flows
    search_flows = pad.list_flows(search_pattern="test")
    print(f"\nFlows matching 'test': {search_flows}")


def example_create_flow():
    """Example: Create a new flow"""
    print("\n=== Create Flow Example ===")
    
    pad = PADFramework()
    
    # Create a new flow
    success = pad.create_flow(
        flow_name="NewExampleFlow",
        template="basic"
    )
    
    if success:
        print("Flow created successfully!")
    else:
        print("Failed to create flow")


def example_validate_flow():
    """Example: Validate a flow"""
    print("\n=== Validate Flow Example ===")
    
    pad = PADFramework()
    
    # Validate flow
    result = pad.validate_flow("MyTestFlow")
    
    print(f"Valid: {result['valid']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")
    if result['warnings']:
        print(f"Warnings: {result['warnings']}")


def example_performance_stats():
    """Example: Get performance statistics"""
    print("\n=== Performance Stats Example ===")
    
    pad = PADFramework()
    
    # Execute a flow first
    pad.execute_flow("MyTestFlow", {})
    
    # Get performance stats
    stats = pad.get_performance_stats("MyTestFlow")
    print(f"Performance Stats: {stats}")


def example_integration():
    """Example: Use integrations"""
    print("\n=== Integration Example ===")
    
    pad = PADFramework()
    
    # Email integration
    email_integration = pad.integrate(
        "email",
        server="smtp.gmail.com",
        port=587
    )
    print(f"Email Integration: {email_integration}")
    
    # API integration
    api_integration = pad.integrate(
        "api",
        endpoint="https://api.example.com"
    )
    print(f"API Integration: {api_integration}")


def example_health_check():
    """Example: Check framework health"""
    print("\n=== Health Check Example ===")
    
    pad = PADFramework()
    
    health = pad.get_health_status()
    print(f"Framework Health:")
    for key, value in health.items():
        print(f"  {key}: {value}")


def example_scheduling():
    """Example: Schedule a flow"""
    print("\n=== Scheduling Example ===")
    
    pad = PADFramework()
    
    # Schedule a flow
    schedule_id = pad.schedule_flow(
        flow_name="MyTestFlow",
        schedule="0 9 * * *",  # Daily at 9 AM
        input_variables={"daily_run": True}
    )
    
    print(f"Flow scheduled with ID: {schedule_id}")
    
    # Cancel schedule
    # pad.cancel_schedule(schedule_id)


if __name__ == "__main__":
    print("Power Automate Desktop Framework - Examples")
    print("=" * 50)
    
    # Run examples
    try:
        example_list_flows()
        example_health_check()
        # example_execute_flow()
        # example_create_flow()
        # example_validate_flow()
        # example_performance_stats()
        # example_integration()
        # example_scheduling()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
