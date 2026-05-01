# group8-midtermproject

## Azure Containerized Deployment Requirements

This project now includes:
- A Dockerized Flask app for Azure App Service, with SSH enabled.
- A GitHub Actions workflow that builds and pushes the Docker image to Azure Container Registry (ACR) and deploys it to Azure App Service.

### 1) Docker Setup (SSH + Web App)

Files added:
- `Dockerfile`
- `startup.sh`
- `sshd_config`

Exposed ports:
- `8000` for the web application (`gunicorn`)
- `2222` for SSH access

### 2) Create Azure Container Registry (ACR)

Run these commands once (update variables for your environment):

```bash
RESOURCE_GROUP="group8-rg"
LOCATION="westeurope"
ACR_NAME="group8acr"

az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
az acr create --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --sku Basic
az acr update --name "$ACR_NAME" --admin-enabled true
az acr credential show --name "$ACR_NAME"
```

Use the returned ACR credentials as GitHub repository secrets:
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`
- `ACR_LOGIN_SERVER` (e.g. `group8acr.azurecr.io`)

### 3) GitHub Actions Workflow

Workflow file:
- `.github/workflows/main_group8-api.yml`

The workflow performs:
1. Azure login with `AZURE_CREDENTIALS`
2. ACR authentication using `REGISTRY_USERNAME` and `REGISTRY_PASSWORD`
3. Docker build and push to ACR
4. Deployment to Azure App Service

Required GitHub secrets:
- `AZURE_CREDENTIALS`
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`
- `ACR_LOGIN_SERVER`
- `APP_SERVICE_NAME`

### 4) User Assigned Identity for App Service + ACR Access

Use a User Assigned Managed Identity and grant `AcrPull`:

```bash
RESOURCE_GROUP="group8-rg"
APP_SERVICE_NAME="group8-api"
IDENTITY_NAME="group8-appsvc-identity"
ACR_NAME="group8acr"

# Create identity
az identity create --resource-group "$RESOURCE_GROUP" --name "$IDENTITY_NAME"

# Get identity resource ID and principal ID
IDENTITY_ID=$(az identity show --resource-group "$RESOURCE_GROUP" --name "$IDENTITY_NAME" --query id -o tsv)
PRINCIPAL_ID=$(az identity show --resource-group "$RESOURCE_GROUP" --name "$IDENTITY_NAME" --query principalId -o tsv)
ACR_ID=$(az acr show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --query id -o tsv)

# Assign identity to web app
az webapp identity assign --resource-group "$RESOURCE_GROUP" --name "$APP_SERVICE_NAME" --identities "$IDENTITY_ID"

# Grant AcrPull on ACR
az role assignment create --assignee "$PRINCIPAL_ID" --scope "$ACR_ID" --role AcrPull

# Configure App Service to use managed identity for ACR pulls
az webapp config set \
  --resource-group "$RESOURCE_GROUP" \
  --name "$APP_SERVICE_NAME" \
  --generic-configurations "{\"acrUseManagedIdentityCreds\": true}"
```

If your app listens on port `8000`, set this app setting on App Service:

```bash
az webapp config appsettings set \
  --resource-group "$RESOURCE_GROUP" \
  --name "$APP_SERVICE_NAME" \
  --settings WEBSITES_PORT=8000
```