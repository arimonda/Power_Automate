"""
Main entry point for PAD Framework
Quick start script
"""

from pad_framework import PADFramework
from pad_framework.utils.logger import Logger
from pad_framework.core.config import Config


def main():
    """Main function"""
    print("=" * 60)
    print("Power Automate Desktop Framework")
    print("Version 1.0.0 - All Features Enabled")
    print("=" * 60)
    print()
    
    try:
        # Initialize framework
        print("Initializing framework...")
        pad = PADFramework()
        print("✓ Framework initialized successfully")
        print()
        
        # Show health status
        print("Framework Health Status:")
        print("-" * 40)
        health = pad.get_health_status()
        for key, value in health.items():
            print(f"  {key}: {value}")
        print()
        
        # List available flows
        print("Available Flows:")
        print("-" * 40)
        flows = pad.list_flows()
        if flows:
            for i, flow in enumerate(flows, 1):
                print(f"  {i}. {flow}")
        else:
            print("  No flows found. Create your first flow!")
            print()
            print("  Example:")
            print("    pad.create_flow('MyFirstFlow', template='basic')")
        print()
        
        # Show configuration
        print("Configuration:")
        print("-" * 40)
        print(f"  Flows Path: {pad.config.get_path('flows')}")
        print(f"  Logs Path: {pad.config.get_path('logs')}")
        print(f"  Data Path: {pad.config.get_path('data')}")
        print(f"  Log Level: {pad.config.get('logging.level')}")
        print(f"  Performance Monitoring: {pad.config.get('performance.monitoring_enabled')}")
        print()
        
        # Show available features
        print("Enabled Features:")
        print("-" * 40)
        features = [
            "✓ Flow Execution & Management",
            "✓ Performance Monitoring",
            "✓ Logging & Error Handling",
            "✓ Testing Framework",
            "✓ Configuration Management",
            "✓ Retry & Timeout Support",
            "✓ Scheduling",
            "✓ Database Integration",
            "✓ Email Integration",
            "✓ API Integration",
            "✓ Web Automation",
            "✓ File Operations",
            "✓ Credential Management",
            "✓ Notification System"
        ]
        
        for feature in features:
            print(f"  {feature}")
        print()
        
        print("=" * 60)
        print("Framework ready! Check the examples folder to get started.")
        print("Documentation: docs/getting_started.md")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
