#!/usr/bin/env python3
"""
generate_alerting_rules.py — Generates Prometheus/Alertmanager alerting rules
for common application metrics, tailored by stack type.

Usage:
    python3 generate_alerting_rules.py --app myapp --stack api --output alerts.yml
    python3 generate_alerting_rules.py --app workerapp --stack worker --output worker-alerts.yml
    python3 generate_alerting_rules.py --app postgres --stack database --output db-alerts.yml
"""

import argparse
import sys
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None  # fallback to manual YAML rendering


# ---------------------------------------------------------------------------
# Rule definitions per stack
# ---------------------------------------------------------------------------

def get_web_api_rules(app: str) -> list:
    """Alerting rules for web and API stacks."""
    return [
        {
            "alert": f"{app}_HighLatencyP95",
            "expr": (
                f'histogram_quantile(0.95, sum(rate({app}_http_request_duration_seconds_bucket[5m])) by (le, handler))'
                f' > 0.5'
            ),
            "for": "5m",
            "labels": {"severity": "warning", "app": app, "stack": "api"},
            "annotations": {
                "summary": f"High p95 latency on {app}",
                "description": (
                    f"The 95th percentile latency for {app} HTTP requests has exceeded 500ms "
                    f"for more than 5 minutes. Current value: {{{{ $value | humanizeDuration }}}}. "
                    f"Handler: {{{{ $labels.handler }}}}."
                ),
            },
        },
        {
            "alert": f"{app}_HighErrorRate",
            "expr": (
                f'sum(rate({app}_http_requests_total{{status=~"5.."}}[5m])) / '
                f'sum(rate({app}_http_requests_total[5m])) > 0.01'
            ),
            "for": "2m",
            "labels": {"severity": "critical", "app": app, "stack": "api"},
            "annotations": {
                "summary": f"High HTTP error rate on {app}",
                "description": (
                    f"The HTTP 5xx error rate for {app} has exceeded 1% over the last 5 minutes. "
                    f"Current rate: {{{{ $value | humanizePercentage }}}}."
                ),
            },
        },
        {
            "alert": f"{app}_LowAvailability",
            "expr": (
                f'avg_over_time(up{{job="{app}"}}[5m]) < 0.999'
            ),
            "for": "1m",
            "labels": {"severity": "critical", "app": app, "stack": "api"},
            "annotations": {
                "summary": f"Availability below 99.9% for {app}",
                "description": (
                    f"{app} availability has dropped below 99.9% over the last 5 minutes. "
                    f"Current availability: {{{{ $value | humanizePercentage }}}}."
                ),
            },
        },
        {
            "alert": f"{app}_HighMemoryUsage",
            "expr": (
                f'process_resident_memory_bytes{{job="{app}"}} / '
                f'node_memory_MemTotal_bytes * 100 > 80'
            ),
            "for": "10m",
            "labels": {"severity": "warning", "app": app, "stack": "api"},
            "annotations": {
                "summary": f"High memory usage on {app}",
                "description": (
                    f"{app} is using more than 80% of available memory for over 10 minutes. "
                    f"Current usage: {{{{ $value | humanize }}}}%."
                ),
            },
        },
    ]


def get_worker_rules(app: str) -> list:
    """Alerting rules for worker/queue-based stacks."""
    return [
        {
            "alert": f"{app}_HighQueueDepth",
            "expr": f'{app}_queue_depth > 1000',
            "for": "5m",
            "labels": {"severity": "warning", "app": app, "stack": "worker"},
            "annotations": {
                "summary": f"Queue depth too high for {app}",
                "description": (
                    f"The job queue depth for {app} has exceeded 1000 items for more than 5 minutes. "
                    f"Current depth: {{{{ $value }}}} jobs. Check consumer health and throughput."
                ),
            },
        },
        {
            "alert": f"{app}_HighJobFailureRate",
            "expr": (
                f'sum(rate({app}_jobs_failed_total[10m])) / '
                f'sum(rate({app}_jobs_processed_total[10m])) > 0.05'
            ),
            "for": "5m",
            "labels": {"severity": "critical", "app": app, "stack": "worker"},
            "annotations": {
                "summary": f"High job failure rate for {app}",
                "description": (
                    f"The job failure rate for {app} has exceeded 5% over the last 10 minutes. "
                    f"Current rate: {{{{ $value | humanizePercentage }}}}. "
                    f"Check dead-letter queue and worker error logs."
                ),
            },
        },
        {
            "alert": f"{app}_HighProcessingLag",
            "expr": (
                f'time() - {app}_last_job_processed_timestamp > 300'
            ),
            "for": "2m",
            "labels": {"severity": "warning", "app": app, "stack": "worker"},
            "annotations": {
                "summary": f"Processing lag exceeds 5 minutes for {app}",
                "description": (
                    f"No job has been processed by {app} in the last 5 minutes. "
                    f"Lag: {{{{ $value | humanizeDuration }}}}. "
                    f"Verify that workers are running and the queue broker is reachable."
                ),
            },
        },
    ]


def get_database_rules(app: str) -> list:
    """Alerting rules for database stacks."""
    return [
        {
            "alert": f"{app}_HighConnectionUsage",
            "expr": (
                f'pg_stat_activity_count{{datname="{app}"}} / '
                f'pg_settings_max_connections * 100 > 80'
            ),
            "for": "5m",
            "labels": {"severity": "warning", "app": app, "stack": "database"},
            "annotations": {
                "summary": f"Database connection pool near capacity for {app}",
                "description": (
                    f"The PostgreSQL connection count for {app} has exceeded 80% of max_connections "
                    f"for more than 5 minutes. "
                    f"Current usage: {{{{ $value | humanize }}}}%. Consider adding a connection pooler (PgBouncer)."
                ),
            },
        },
        {
            "alert": f"{app}_ReplicationLag",
            "expr": (
                f'pg_replication_lag{{job="{app}"}} > 30'
            ),
            "for": "2m",
            "labels": {"severity": "critical", "app": app, "stack": "database"},
            "annotations": {
                "summary": f"High replication lag for {app}",
                "description": (
                    f"PostgreSQL replication lag for {app} has exceeded 30 seconds. "
                    f"Current lag: {{{{ $value | humanizeDuration }}}}. "
                    f"Check replica connectivity and I/O capacity."
                ),
            },
        },
        {
            "alert": f"{app}_SlowQueriesP95",
            "expr": (
                f'histogram_quantile(0.95, sum(rate({app}_query_duration_seconds_bucket[5m])) by (le))'
                f' > 0.1'
            ),
            "for": "5m",
            "labels": {"severity": "warning", "app": app, "stack": "database"},
            "annotations": {
                "summary": f"Slow queries detected on {app}",
                "description": (
                    f"The p95 query duration for {app} has exceeded 100ms for more than 5 minutes. "
                    f"Current p95: {{{{ $value | humanizeDuration }}}}. "
                    f"Review slow query logs and check for missing indexes."
                ),
            },
        },
    ]


# ---------------------------------------------------------------------------
# Recording rules (base metrics)
# ---------------------------------------------------------------------------

def get_recording_rules(app: str, stack: str) -> list:
    """Recording rules to pre-aggregate base metrics."""
    common = [
        {
            "record": f"job:up:avg5m",
            "expr": f'avg_over_time(up{{job="{app}"}}[5m])',
        },
    ]

    if stack in ("web", "api"):
        common += [
            {
                "record": f"{app}:http_request_rate5m",
                "expr": f'sum(rate({app}_http_requests_total[5m])) by (handler, status)',
            },
            {
                "record": f"{app}:http_error_rate5m",
                "expr": (
                    f'sum(rate({app}_http_requests_total{{status=~"5.."}}[5m])) / '
                    f'sum(rate({app}_http_requests_total[5m]))'
                ),
            },
            {
                "record": f"{app}:http_latency_p95_5m",
                "expr": (
                    f'histogram_quantile(0.95, sum(rate({app}_http_request_duration_seconds_bucket[5m])) by (le, handler))'
                ),
            },
        ]
    elif stack == "worker":
        common += [
            {
                "record": f"{app}:job_failure_rate10m",
                "expr": (
                    f'sum(rate({app}_jobs_failed_total[10m])) / '
                    f'sum(rate({app}_jobs_processed_total[10m]))'
                ),
            },
            {
                "record": f"{app}:queue_depth_avg5m",
                "expr": f'avg_over_time({app}_queue_depth[5m])',
            },
        ]
    elif stack == "database":
        common += [
            {
                "record": f"{app}:connection_usage_pct",
                "expr": (
                    f'pg_stat_activity_count{{datname="{app}"}} / pg_settings_max_connections * 100'
                ),
            },
            {
                "record": f"{app}:query_latency_p95_5m",
                "expr": (
                    f'histogram_quantile(0.95, sum(rate({app}_query_duration_seconds_bucket[5m])) by (le))'
                ),
            },
        ]

    return common


# ---------------------------------------------------------------------------
# YAML builder
# ---------------------------------------------------------------------------

def build_yaml_document(app: str, stack: str) -> dict:
    """Assemble the full Prometheus rules document."""
    if stack in ("web", "api"):
        alert_rules = get_web_api_rules(app)
    elif stack == "worker":
        alert_rules = get_worker_rules(app)
    elif stack == "database":
        alert_rules = get_database_rules(app)
    else:
        raise ValueError(f"Unknown stack: {stack}. Choose from: web, api, worker, database")

    recording_rules = get_recording_rules(app, stack)

    document = {
        "groups": [
            {
                "name": f"{app}.recording_rules",
                "interval": "30s",
                "rules": recording_rules,
            },
            {
                "name": f"{app}.alerts",
                "rules": alert_rules,
            },
        ]
    }
    return document


# ---------------------------------------------------------------------------
# Manual YAML renderer (fallback when PyYAML is not installed)
# ---------------------------------------------------------------------------

def render_yaml_fallback(document: dict) -> str:
    """Minimal YAML renderer used when PyYAML is unavailable."""
    lines = ["groups:"]
    for group in document["groups"]:
        lines.append(f"  - name: {group['name']}")
        if "interval" in group:
            lines.append(f"    interval: {group['interval']}")
        lines.append("    rules:")
        for rule in group["rules"]:
            first_key = True
            for k, v in rule.items():
                prefix = "      - " if first_key else "        "
                first_key = False
                if isinstance(v, dict):
                    lines.append(f"{prefix}{k}:")
                    for sub_k, sub_v in v.items():
                        if any(c in str(sub_v) for c in (":", "{", "}", "[", "]")):
                            sub_v_str = f"'{str(sub_v)}'"
                        else:
                            sub_v_str = str(sub_v)
                        lines.append(f"          {sub_k}: {sub_v_str}")
                else:
                    if any(c in str(v) for c in (":", "{", "}", "[", "]", ">", "|")):
                        v_str = f"'{str(v)}'"
                    else:
                        v_str = str(v)
                    lines.append(f"{prefix}{k}: {v_str}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate Prometheus/Alertmanager alerting rules YAML "
            "for a given application and stack type."
        )
    )
    parser.add_argument(
        "--app",
        required=True,
        help="Application name (used as label and metric prefix, e.g. myapp)",
    )
    parser.add_argument(
        "--stack",
        required=True,
        choices=["web", "api", "worker", "database"],
        help="Stack type: web, api, worker, or database",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for the generated YAML (e.g. alerts.yml)",
    )

    args = parser.parse_args()

    # Build the rules document
    try:
        document = build_yaml_document(app=args.app, stack=args.stack)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Render to YAML
    header = (
        f"# Prometheus alerting rules for {args.app} ({args.stack} stack)\n"
        f"# Generated by generate_alerting_rules.py on {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"# Load this file in your Prometheus configuration under rule_files:\n"
        f"#   rule_files:\n"
        f"#     - '{args.output}'\n\n"
    )

    if yaml is not None:
        content = header + yaml.dump(document, default_flow_style=False, allow_unicode=True, sort_keys=False)
    else:
        content = header + render_yaml_fallback(document)

    # Write output
    try:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"[OK] Alerting rules written to: {args.output}")
        print(f"     App   : {args.app}")
        print(f"     Stack : {args.stack}")
        total_alerts = sum(
            len([r for r in g["rules"] if "alert" in r])
            for g in document["groups"]
        )
        total_recording = sum(
            len([r for r in g["rules"] if "record" in r])
            for g in document["groups"]
        )
        print(f"     Alerting rules   : {total_alerts}")
        print(f"     Recording rules  : {total_recording}")
    except OSError as exc:
        print(f"Error writing output file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
