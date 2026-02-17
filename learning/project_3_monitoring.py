"""
PROJECT 3: Health Monitoring Tool
Build a monitoring utility for flow health, performance, and alerts.

REQUIREMENTS:
- Check framework health status
- Measure per-flow performance trends
- Detect failures and slow executions
- Produce a simple health report
- Trigger alerts when thresholds are exceeded

YOUR TASK: Complete and customize TODO sections.
"""

from datetime import datetime

from pad_framework import PADFramework


class HealthMonitor:
    """Template for monitoring framework and flow health."""

    def __init__(self):
        self.pad = PADFramework()
        self.timestamp = datetime.now().isoformat()
        self.slow_threshold = 5.0
        self.failure_threshold = 0.10  # 10%
        print("✓ Health Monitor initialized")

    def run(self):
        """Run full health checks and print a report."""
        print("\n" + "=" * 60)
        print("PROJECT 3: HEALTH MONITORING")
        print("=" * 60)

        health = self._check_framework_health()
        flow_report = self._check_flow_performance()
        alerts = self._build_alerts(flow_report)
        self._print_report(health, flow_report, alerts)

        if alerts:
            self._send_alerts(alerts)

        return {"health": health, "flows": flow_report, "alerts": alerts}

    def _check_framework_health(self):
        """Collect top-level framework health details."""
        print("\nStep 1: Checking framework health...")
        health = self.pad.get_health_status()
        print(f"  Status: {health.get('status')}")
        print(f"  Version: {health.get('version')}")
        print(f"  Flows available: {health.get('flows_available')}")
        return health

    def _check_flow_performance(self):
        """Inspect per-flow stats and compute simple flags."""
        print("\nStep 2: Checking flow performance...")
        report = []
        flows = self.pad.list_flows()

        for flow_name in flows:
            stats = self.pad.get_performance_stats(flow_name)
            if not stats:
                continue

            avg_duration = float(stats.get("avg_duration", 0.0))
            execution_count = int(stats.get("execution_count", 0))
            error_rate = float(stats.get("error_rate", 0.0)) if "error_rate" in stats else 0.0

            row = {
                "flow_name": flow_name,
                "execution_count": execution_count,
                "avg_duration": avg_duration,
                "error_rate": error_rate,
                "is_slow": avg_duration > self.slow_threshold,
                "is_unstable": error_rate > self.failure_threshold,
            }
            report.append(row)

        print(f"  Checked {len(report)} flow(s)")
        return report

    def _build_alerts(self, flow_report):
        """Create alerts from slow or unstable flow conditions."""
        print("\nStep 3: Evaluating alerts...")
        alerts = []
        for row in flow_report:
            if row["is_slow"]:
                alerts.append(
                    f"[SLOW] {row['flow_name']} avg duration "
                    f"{row['avg_duration']:.2f}s exceeds {self.slow_threshold:.2f}s"
                )
            if row["is_unstable"]:
                alerts.append(
                    f"[UNSTABLE] {row['flow_name']} error rate "
                    f"{row['error_rate']:.1%} exceeds {self.failure_threshold:.1%}"
                )

        print(f"  Alerts generated: {len(alerts)}")
        return alerts

    def _send_alerts(self, alerts):
        """TODO: Replace with real email/Slack alert integration."""
        print("\nStep 4: Sending alerts...")
        for alert in alerts:
            print(f"  ALERT: {alert}")
        self.pad.logger.warning("Health monitor alerts generated", alerts=alerts)

    def _print_report(self, health, flow_report, alerts):
        """Print plain-text health report."""
        print("\n" + "-" * 60)
        print("HEALTH REPORT")
        print("-" * 60)
        print(f"Timestamp: {self.timestamp}")
        print(f"Framework status: {health.get('status')}")
        print(f"Flows analyzed: {len(flow_report)}")
        print(f"Alerts: {len(alerts)}")

        if flow_report:
            print("\nFlow summary:")
            for row in flow_report:
                print(
                    f"  - {row['flow_name']}: runs={row['execution_count']}, "
                    f"avg={row['avg_duration']:.2f}s, err={row['error_rate']:.1%}"
                )


def main():
    monitor = HealthMonitor()
    monitor.run()

    print("\n" + "=" * 60)
    print("🎯 YOUR TASKS:")
    print("1. Add hourly scheduler for this monitor")
    print("2. Persist report output to JSON/HTML")
    print("3. Add email or Slack alert integration")
    print("4. Track trends day-over-day")
    print("5. Add environment-based thresholds")
    print("=" * 60)


if __name__ == "__main__":
    main()
