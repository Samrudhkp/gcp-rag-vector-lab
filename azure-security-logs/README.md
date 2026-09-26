# Azure Security Log Lab

Minimal Azure pipeline for fictional login logs:

**Blob Storage (`logs`) → Event Grid (BlobCreated) → Python Azure Function → Blob Storage (`reports`)**

If you already know GCP: this is Cloud Storage → Eventarc → Cloud Functions/Cloud Run, on Azure.

No AI models, databases, Container Apps, Container Registry, or Service Bus.

---

## What each file is

| Path | Purpose |
|------|---------|
| `analyzer.py` | Pure Python analysis: count failures, flag accounts with ≥5 failures. No Azure imports — easy to unit-test. |
| `function_app.py` | Azure Functions (Python v2 model) with an **Event Grid trigger**. Downloads the new log blob, calls `analyzer`, uploads a JSON report. |
| `host.json` | Function host settings (logging + extension bundle). Required by Azure Functions. |
| `local.settings.json.example` | Template for local Function settings. Copy to `local.settings.json` (gitignored). **Never put secrets in Git.** |
| `requirements.txt` | Python packages for the Function (`azure-functions`, blob SDK, identity). |
| `.gitignore` | Ignores `local.settings.json`, venvs, Azure deploy artifacts. |
| `samples/login-log-alice-flagged.json` | Sample with **alice = 5 failures** → should be flagged. |
| `samples/login-log-clean.json` | Sample with no account at the threshold → empty `flagged_accounts`. |
| `samples/login-log-multi-flagged.json` | Sample with **grace (6)** and **heidi (5)** flagged. |
| `scripts/run_local.py` | Run analysis on a sample file with plain Python (no Azure). |
| `tests/test_analyzer.py` | Pytest coverage for the three samples + a bad-input case. |
| `README.md` | This file: local run, GCP comparison, deploy plan, costs, teardown. |

---

## Run and test locally (no Azure account needed)

```bash
cd azure-security-logs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest

# Analyze one sample
python scripts/run_local.py samples/login-log-alice-flagged.json

# Write a report file
python scripts/run_local.py samples/login-log-multi-flagged.json -o out/report.json

# Unit tests
python -m pytest tests/ -v
```

Expected: alice flagged in the first sample; nobody in `clean`; grace + heidi in `multi-flagged`.

---

## GCP → Azure mental model

| You know (GCP) | This lab (Azure) | Notes |
|----------------|------------------|-------|
| Cloud Storage bucket | **Blob Storage** container inside a **Storage Account** | A storage account holds many containers (`logs`, `reports`). Closest to a GCS bucket is a **container**, not the account. |
| Object finalize / create | Blob **created** event | Same idea: new object lands → event fires. |
| Eventarc | **Event Grid** | Eventarc routes Cloud Events; Event Grid routes Azure events (here: `Microsoft.Storage.BlobCreated`) to a Function. |
| Cloud Functions (2nd gen) / Cloud Run | **Azure Functions** (Consumption plan) | Event-driven Python handler. Consumption ≈ Cloud Functions pricing shape (per-execution). |
| Service account + IAM on bucket | **Managed Identity** + RBAC role on the storage account | Prefer identity over keys. This lab can use the Function’s system-assigned identity with `Storage Blob Data Contributor`. |
| `gsutil cp` | `az storage blob upload` | Upload a sample JSON to trigger the pipeline. |
| Cloud Logging | Function **Log stream** / Application Insights (optional) | Start with the Function’s log stream in the portal or `az functionapp log tail`. |

**Wiring difference:** In GCP you often create an Eventarc trigger on `google.cloud.storage.object.v1.finalized`. On Azure you create an **Event Grid subscription** on the storage account (or a system topic) whose endpoint is the Function’s Event Grid trigger.

---

## Deploy plan — wait for your approval

**Do not run these commands until you reply that you approve the resources and cost estimate below.**

### Exact resource list (pricing tiers)

| # | Resource | SKU / tier | Why |
|---|----------|------------|-----|
| 1 | Resource group | n/a | Groups everything for one-command delete. |
| 2 | Storage account | **Standard** / **LRS** / Cool or Hot (Hot is fine) | Holds `logs` + `reports` containers **and** Azure Functions host storage (`AzureWebJobsStorage`). |
| 3 | Function App | **Consumption (Dynamic Y1)** / Python 3.11 or 3.12 / Linux | Runs `AnalyzeLoginLog`. No App Service Plan VM to pay for idle. |
| 4 | Application Insights | **Workspace-based** (optional; can disable after create) | Created by many Function templates. Free daily cap is usually enough for this lab; skip or delete if you want zero telemetry. |
| 5 | Event Grid system topic | Storage account blob events | Publishes `BlobCreated`. |
| 6 | Event Grid subscription | Filter: container `logs`, event `Microsoft.Storage.BlobCreated` | Delivers to the Function endpoint. |

**Not created:** AI services, Cosmos DB/SQL, Container Apps, ACR, Service Bus, Logic Apps.

### Possible charges (pay-as-you-go, rough)

For a few sample uploads and a short lab session, expect **cents**, often **$0** if you stay inside free grants:

| Service | Free grant / low usage | Risk if left running |
|---------|------------------------|----------------------|
| Storage | First few GB + transactions are cheap (~$0.02/GB-mo + tiny per-10k ops) | Leaving large data or many writes increases cost. |
| Functions Consumption | **1 million executions** and **400,000 GB-s** free per month (per subscription) | Idle Consumption apps are usually $0; bill appears only with executions beyond free grant. |
| Event Grid | **100,000 operations/month** free | Lab traffic is negligible. |
| Application Insights | Small free daily ingest; beyond that, pay per GB | Disable or delete if unused. |

Always verify current prices: [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

Suggested names (change the unique suffix):

```bash
RG=rg-sec-logs-lab
LOC=eastus
STORAGE=stseclogslab$RANDOM          # must be globally unique, 3–24 lowercase alphanumeric
FUNC=func-sec-logs-lab-$RANDOM
```

### Commands that would create resources (do not run yet)

```bash
# Login / subscription
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# 1) Resource group
az group create --name "$RG" --location "$LOC"

# 2) Storage account (Standard LRS)
az storage account create \
  --name "$STORAGE" \
  --resource-group "$RG" \
  --location "$LOC" \
  --sku Standard_LRS \
  --kind StorageV2

# Containers
az storage container create --name logs --account-name "$STORAGE" --auth-mode login
az storage container create --name reports --account-name "$STORAGE" --auth-mode login

# 3) Function App on Consumption (Python)
az functionapp create \
  --name "$FUNC" \
  --resource-group "$RG" \
  --storage-account "$STORAGE" \
  --consumption-plan-location "$LOC" \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type Linux

# App settings (no keys in Git — set on the app)
az functionapp config appsettings set \
  --name "$FUNC" \
  --resource-group "$RG" \
  --settings \
    STORAGE_ACCOUNT_URL="https://${STORAGE}.blob.core.windows.net" \
    LOGS_CONTAINER=logs \
    REPORTS_CONTAINER=reports

# Managed Identity + RBAC for blobs
az functionapp identity assign --name "$FUNC" --resource-group "$RG"
PRINCIPAL_ID=$(az functionapp identity show --name "$FUNC" --resource-group "$RG" --query principalId -o tsv)
STORAGE_ID=$(az storage account show --name "$STORAGE" --resource-group "$RG" --query id -o tsv)
az role assignment create \
  --assignee-object-id "$PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_ID"

# Deploy code from ./azure-security-logs
cd azure-security-logs
func azure functionapp publish "$FUNC"

# 4–6) Event Grid subscription: BlobCreated on logs → Function
# (Portal: Storage account → Events → + Event Subscription → endpoint = AnalyzeLoginLog)
# Or CLI equivalent after the function exists — see "After approval" section once you approve.
```

### Delete everything

```bash
# Nuclear option: deletes RG and ALL resources inside it
az group delete --name "$RG" --yes --no-wait
```

Or delete individually (order does not matter much if the whole RG goes):

```bash
az eventgrid event-subscription delete --name logs-to-func --source-resource-id "$STORAGE_ID"
az functionapp delete --name "$FUNC" --resource-group "$RG"
az storage account delete --name "$STORAGE" --resource-group "$RG" --yes
az group delete --name "$RG" --yes
```

---

## After you approve deployment

Reply with something like: **“Approved — deploy with the resource list above.”**  
Then we can run the create/publish/Event Grid commands together, upload a sample from `samples/`, and confirm a report appears in `reports/`.

Until then, only local Python testing is done — **no Azure resources created by this project**.

---

## Sample report shape

```json
{
  "report_type": "failed_login_summary",
  "threshold": 5,
  "total_events": 8,
  "failed_login_counts": {"alice": 5, "carol": 1},
  "flagged_accounts": [
    {"username": "alice", "failed_logins": 5, "reason": ">= 5 failed logins"}
  ],
  "flagged_count": 1
}
```
