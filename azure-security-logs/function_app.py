"""Azure Function: Event Grid (BlobCreated) -> analyze login log -> write report blob.

Event Grid delivers a BlobCreated event when a file lands in the `logs` container.
The function downloads that blob, runs analyzer.analyze_login_log, and uploads a
JSON report to the `reports` container.

Credentials come from app settings / Managed Identity — never from source code.
"""

from __future__ import annotations

import json
import logging
import os
from urllib.parse import unquote, urlparse

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from analyzer import analyze_login_log

app = func.FunctionApp()

logger = logging.getLogger(__name__)


def _blob_service_client() -> BlobServiceClient:
    """Build a Blob client from connection string or account URL + DefaultAzureCredential."""
    conn = os.environ.get("AzureWebJobsStorage") or os.environ.get("STORAGE_CONNECTION_STRING")
    if conn and "AccountKey=" in conn:
        return BlobServiceClient.from_connection_string(conn)

    account_url = os.environ.get("STORAGE_ACCOUNT_URL")
    if not account_url:
        raise RuntimeError(
            "Set STORAGE_ACCOUNT_URL (preferred) or AzureWebJobsStorage with an account key."
        )
    return BlobServiceClient(account_url, credential=DefaultAzureCredential())


def _parse_blob_url(url: str) -> tuple[str, str]:
    """Return (container, blob_path) from an Event Grid blob URL."""
    parsed = urlparse(url)
    parts = [unquote(p) for p in parsed.path.lstrip("/").split("/", 1)]
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError(f"Cannot parse container/blob from URL: {url}")
    return parts[0], parts[1]


@app.function_name(name="AnalyzeLoginLog")
@app.event_grid_trigger(arg_name="event")
def analyze_login_log_handler(event: func.EventGridEvent) -> None:
    """Handle BlobCreated events for login-log JSON files."""
    data = event.get_json()
    blob_url = data.get("url") if isinstance(data, dict) else None
    if not blob_url:
        logger.warning("Event missing data.url; ignoring. subject=%s", event.subject)
        return

    container, blob_name = _parse_blob_url(blob_url)
    reports_container = os.environ.get("REPORTS_CONTAINER", "reports")
    logs_container = os.environ.get("LOGS_CONTAINER", "logs")

    # Ignore writes to the reports container (or any non-logs container).
    if container != logs_container:
        logger.info("Ignoring blob outside logs container: %s/%s", container, blob_name)
        return

    if not blob_name.lower().endswith(".json"):
        logger.info("Ignoring non-JSON blob: %s/%s", container, blob_name)
        return

    client = _blob_service_client()
    downloader = client.get_blob_client(container, blob_name).download_blob()
    payload = json.loads(downloader.readall())

    report = analyze_login_log(payload, source_blob=f"{container}/{blob_name}")
    report_name = f"{os.path.splitext(os.path.basename(blob_name))[0]}-report.json"

    report_client = client.get_blob_client(reports_container, report_name)
    report_client.upload_blob(
        json.dumps(report, indent=2),
        overwrite=True,
        content_type="application/json",
    )
    logger.info(
        "Wrote report %s/%s (flagged=%s)",
        reports_container,
        report_name,
        report["flagged_count"],
    )
