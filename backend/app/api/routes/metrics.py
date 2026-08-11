import os
import psutil
from fastapi import APIRouter, Response
from app.modules.workflow.metrics import workflow_metrics

metrics_router = APIRouter(tags=["Metrics & Telemetry"])


@metrics_router.get("/metrics", response_class=Response)
async def get_prometheus_metrics():
    """Generates Prometheus-formatted metrics text for scraping by Monitoring servers."""
    cpu_percent = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    wf_metrics = workflow_metrics.get_summary()

    prometheus_text = f"""# HELP govtjob_cpu_usage_percent Current CPU utilization percentage
# TYPE govtjob_cpu_usage_percent gauge
govtjob_cpu_usage_percent {cpu_percent}

# HELP govtjob_memory_usage_bytes Current RAM memory usage in bytes
# TYPE govtjob_memory_usage_bytes gauge
govtjob_memory_usage_bytes {mem.used}

# HELP govtjob_memory_available_bytes Available RAM memory in bytes
# TYPE govtjob_memory_available_bytes gauge
govtjob_memory_available_bytes {mem.available}

# HELP govtjob_disk_usage_percent Current disk usage percentage
# TYPE govtjob_disk_usage_percent gauge
govtjob_disk_usage_percent {disk.percent}

# HELP govtjob_workflows_current Total active workflow instances
# TYPE govtjob_workflows_current gauge
govtjob_workflows_current {wf_metrics.get("current_workflows_count", 0)}

# HELP govtjob_workflows_completed_total Cumulative completed workflows
# TYPE govtjob_workflows_completed_total counter
govtjob_workflows_completed_total {wf_metrics.get("completed_workflows_count", 0)}

# HELP govtjob_workflows_failed_total Cumulative failed workflows
# TYPE govtjob_workflows_failed_total counter
govtjob_workflows_failed_total {wf_metrics.get("failed_workflows_count", 0)}

# HELP govtjob_workflows_retries_total Cumulative workflow retries
# TYPE govtjob_workflows_retries_total counter
govtjob_workflows_retries_total {wf_metrics.get("total_retries_count", 0)}

# HELP govtjob_workflows_avg_processing_seconds Average processing duration
# TYPE govtjob_workflows_avg_processing_seconds gauge
govtjob_workflows_avg_processing_seconds {wf_metrics.get("avg_processing_time_seconds", 0.0)}
"""
    return Response(content=prometheus_text, media_type="text/plain; version=0.0.4; charset=utf-8")
