"""
Professional Command Line Interface
Production-ready CLI for PAD Framework
"""

import click
import json
import sys
from pathlib import Path
from typing import Optional
from tabulate import tabulate
from datetime import datetime

from .core.framework import PADFramework
from .core.error_codes import PADError


# Color helpers
def success(msg: str) -> str:
    return click.style(msg, fg='green')


def error(msg: str) -> str:
    return click.style(msg, fg='red')


def warning(msg: str) -> str:
    return click.style(msg, fg='yellow')


def info(msg: str) -> str:
    return click.style(msg, fg='cyan')


@click.group()
@click.version_option(version='1.0.0', prog_name='PAD Framework')
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    Power Automate Desktop Framework CLI
    
    Professional command-line interface for managing and executing flows.
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    
    try:
        ctx.obj['pad'] = PADFramework(config_path=config)
    except Exception as e:
        click.echo(error(f"Failed to initialize framework: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.pass_context
def health(ctx):
    """Check framework health status"""
    pad = ctx.obj['pad']
    
    try:
        status = pad.get_health_status()
        
        click.echo("\n" + "="*60)
        click.echo(success("FRAMEWORK HEALTH STATUS"))
        click.echo("="*60 + "\n")
        
        # Overall status
        status_color = 'green' if status['status'] == 'healthy' else 'red'
        click.echo(f"Status: {click.style(status['status'].upper(), fg=status_color)}")
        click.echo(f"Version: {status['version']}")
        click.echo(f"Timestamp: {status['timestamp']}")
        click.echo(f"\nFlows Available: {status['flows_available']}")
        click.echo(f"Active Schedules: {status['active_schedules']}")
        
        # Performance summary
        if 'performance' in status:
            perf = status['performance']
            click.echo(f"\nPerformance:")
            click.echo(f"  Total Flows Tracked: {perf.get('total_flows_tracked', 0)}")
            click.echo(f"  Total Executions: {perf.get('total_executions', 0)}")
            click.echo(f"  System CPU: {perf.get('system_cpu_percent', 0):.1f}%")
            click.echo(f"  System Memory: {perf.get('system_memory_percent', 0):.1f}%")
        
        click.echo("\n" + "="*60 + "\n")
        
    except Exception as e:
        click.echo(error(f"Health check failed: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.option('--search', '-s', help='Search pattern for filtering flows')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def list(ctx, search, output_json):
    """List all available flows"""
    pad = ctx.obj['pad']
    
    try:
        flows = pad.list_flows(search_pattern=search)
        
        if output_json:
            click.echo(json.dumps({"flows": flows}, indent=2))
            return
        
        if not flows:
            click.echo(warning("No flows found"))
            return
        
        click.echo(f"\n{success('Available Flows')} ({len(flows)} found):\n")
        
        for i, flow in enumerate(flows, 1):
            click.echo(f"  {i}. {flow}")
        
        click.echo()
        
    except Exception as e:
        click.echo(error(f"Failed to list flows: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.argument('flow_name')
@click.option('--input', '-i', help='Input variables as JSON string or @file.json')
@click.option('--timeout', '-t', type=int, help='Execution timeout in seconds')
@click.option('--retry', '-r', type=int, default=0, help='Number of retry attempts')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def execute(ctx, flow_name, input, timeout, retry, output_json):
    """Execute a flow"""
    pad = ctx.obj['pad']
    
    # Parse input variables
    input_vars = {}
    if input:
        try:
            if input.startswith('@'):
                # Load from file
                with open(input[1:], 'r') as f:
                    input_vars = json.load(f)
            else:
                # Parse JSON string
                input_vars = json.loads(input)
        except Exception as e:
            click.echo(error(f"Failed to parse input: {str(e)}"))
            sys.exit(1)
    
    # Execute
    try:
        if not output_json:
            click.echo(f"\n{info('Executing flow')}: {flow_name}\n")
        
        result = pad.execute_flow(
            flow_name=flow_name,
            input_variables=input_vars,
            timeout=timeout,
            retry_count=retry
        )
        
        if output_json:
            # JSON output
            output = {
                "flow_name": result.flow_name,
                "status": result.status,
                "duration": result.duration,
                "execution_id": result.execution_id,
                "start_time": result.start_time.isoformat(),
                "end_time": result.end_time.isoformat(),
                "output": result.output,
                "error": result.error
            }
            click.echo(json.dumps(output, indent=2))
        else:
            # Human-readable output
            if result.status == "success":
                click.echo(success(f"✓ Flow executed successfully"))
            else:
                click.echo(error(f"✗ Flow execution failed"))
            
            click.echo(f"\nExecution Details:")
            click.echo(f"  Status: {result.status}")
            click.echo(f"  Duration: {result.duration:.2f}s")
            click.echo(f"  Execution ID: {result.execution_id}")
            
            if result.error:
                click.echo(f"\n{error('Error')}: {result.error}")
            
            if result.output and ctx.obj['verbose']:
                click.echo(f"\nOutput:")
                click.echo(json.dumps(result.output, indent=2))
            
            click.echo()
        
    except PADError as e:
        if output_json:
            click.echo(json.dumps(e.to_dict(), indent=2))
        else:
            click.echo(error(f"Execution failed: {str(e)}"))
        sys.exit(1)
    except Exception as e:
        click.echo(error(f"Unexpected error: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.argument('flow_name')
@click.option('--template', '-t', help='Template to use')
@click.pass_context
def create(ctx, flow_name, template):
    """Create a new flow"""
    pad = ctx.obj['pad']
    
    try:
        success_flag = pad.create_flow(flow_name, template=template)
        
        if success_flag:
            click.echo(success(f"✓ Flow '{flow_name}' created successfully"))
        else:
            click.echo(error(f"✗ Failed to create flow '{flow_name}'"))
            sys.exit(1)
            
    except Exception as e:
        click.echo(error(f"Creation failed: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.argument('flow_name')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def validate(ctx, flow_name, output_json):
    """Validate a flow"""
    pad = ctx.obj['pad']
    
    try:
        result = pad.validate_flow(flow_name)
        
        if output_json:
            click.echo(json.dumps(result, indent=2))
            return
        
        click.echo(f"\n{info('Validation Results')} for '{flow_name}':\n")
        
        if result['valid']:
            click.echo(success("✓ Flow is valid"))
        else:
            click.echo(error("✗ Flow has errors"))
        
        if result['errors']:
            click.echo(f"\n{error('Errors')}:")
            for err in result['errors']:
                click.echo(f"  • {err}")
        
        if result['warnings']:
            click.echo(f"\n{warning('Warnings')}:")
            for warn in result['warnings']:
                click.echo(f"  • {warn}")
        
        if result['info']:
            click.echo(f"\n{info('Info')}:")
            for inf in result['info']:
                click.echo(f"  • {inf}")
        
        click.echo()
        
    except Exception as e:
        click.echo(error(f"Validation failed: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.argument('flow_name')
@click.argument('schedule')
@click.option('--input', '-i', help='Input variables as JSON string')
@click.pass_context
def schedule(ctx, flow_name, schedule, input):
    """Schedule a flow execution"""
    pad = ctx.obj['pad']
    
    # Parse input
    input_vars = {}
    if input:
        try:
            input_vars = json.loads(input)
        except Exception as e:
            click.echo(error(f"Failed to parse input: {str(e)}"))
            sys.exit(1)
    
    try:
        schedule_id = pad.schedule_flow(flow_name, schedule, input_vars)
        click.echo(success(f"✓ Flow scheduled successfully"))
        click.echo(f"Schedule ID: {schedule_id}")
        click.echo(f"Schedule: {schedule}")
        
    except Exception as e:
        click.echo(error(f"Scheduling failed: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.argument('flow_name', required=False)
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def stats(ctx, flow_name, output_json):
    """Show performance statistics"""
    pad = ctx.obj['pad']
    
    try:
        stats = pad.get_performance_stats(flow_name)
        
        if output_json:
            click.echo(json.dumps(stats, indent=2))
            return
        
        if not stats:
            click.echo(warning("No statistics available"))
            return
        
        click.echo(f"\n{info('Performance Statistics')}\n")
        
        if flow_name:
            # Single flow stats
            click.echo(f"Flow: {flow_name}")
            click.echo(f"  Executions: {stats.get('execution_count', 0)}")
            click.echo(f"  Avg Duration: {stats.get('avg_duration', 0):.2f}s")
            click.echo(f"  Min Duration: {stats.get('min_duration', 0):.2f}s")
            click.echo(f"  Max Duration: {stats.get('max_duration', 0):.2f}s")
            click.echo(f"  Avg Memory: {stats.get('avg_memory_delta_mb', 0):.2f}MB")
        else:
            # All flows stats - table format
            table_data = []
            for flow, flow_stats in stats.items():
                table_data.append([
                    flow,
                    flow_stats.get('execution_count', 0),
                    f"{flow_stats.get('avg_duration', 0):.2f}s",
                    f"{flow_stats.get('max_duration', 0):.2f}s"
                ])
            
            click.echo(tabulate(
                table_data,
                headers=['Flow', 'Executions', 'Avg Duration', 'Max Duration'],
                tablefmt='grid'
            ))
        
        click.echo()
        
    except Exception as e:
        click.echo(error(f"Failed to get statistics: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.option('--level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']))
@click.option('--flow', '-f', help='Filter by flow name')
@click.option('--lines', '-n', type=int, default=50, help='Number of lines to show')
@click.pass_context
def logs(ctx, level, flow, lines):
    """View logs"""
    pad = ctx.obj['pad']
    
    try:
        log_entries = pad.get_logs(flow_name=flow, level=level)
        
        # Show last N entries
        log_entries = log_entries[-lines:] if len(log_entries) > lines else log_entries
        
        if not log_entries:
            click.echo(warning("No log entries found"))
            return
        
        click.echo(f"\n{info('Log Entries')} (showing last {len(log_entries)}):\n")
        
        for entry in log_entries:
            timestamp = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            level_str = entry['level']
            message = entry['message']
            
            # Color code by level
            if level_str == 'ERROR' or level_str == 'CRITICAL':
                level_str = click.style(level_str, fg='red')
            elif level_str == 'WARNING':
                level_str = click.style(level_str, fg='yellow')
            else:
                level_str = click.style(level_str, fg='cyan')
            
            click.echo(f"[{timestamp}] {level_str:20} {message}")
        
        click.echo()
        
    except Exception as e:
        click.echo(error(f"Failed to get logs: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.pass_context
def config(ctx):
    """Show current configuration"""
    pad = ctx.obj['pad']
    
    try:
        config_dict = pad.config.to_dict()
        click.echo(json.dumps(config_dict, indent=2))
        
    except Exception as e:
        click.echo(error(f"Failed to show configuration: {str(e)}"))
        sys.exit(1)


@cli.command()
@click.option('--pattern', '-p', help='Test pattern to filter')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def test(ctx, pattern, verbose):
    """Run tests"""
    pad = ctx.obj['pad']
    
    try:
        click.echo(f"\n{info('Running tests...')}\n")
        
        results = pad.run_tests(test_pattern=pattern, verbose=verbose)
        
        if results['success']:
            click.echo(success("✓ All tests passed"))
        else:
            click.echo(error("✗ Tests failed"))
        
        click.echo(f"\nExit code: {results['exit_code']}")
        click.echo()
        
    except Exception as e:
        click.echo(error(f"Test execution failed: {str(e)}"))
        sys.exit(1)


def main():
    """Main entry point"""
    cli(obj={})


if __name__ == '__main__':
    main()
