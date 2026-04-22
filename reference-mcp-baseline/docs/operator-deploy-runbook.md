# Operator Deploy Runbook

## Purpose

This runbook captures the exact operator lessons from a real connector deployment so future threads do not rediscover the same Azure and scripting issues.

## Use Order

1. Build image with `az acr build`
2. First deployment uses `az containerapp create`
3. Later deployments use `az containerapp update`
4. Resolve live FQDN and MCP URL
5. Run ACA smoke script
6. Store evidence in repo

## ACR Build Pattern

Example:

```powershell
az acr build \
  --registry acrcaberlinkwriteapi01 \
  --image caberlink-servicedesk-mcp-next:<tag> \
  --file .\servicedesk-mcp-next\runtime\Dockerfile.deploy \
  .\servicedesk-mcp-next\runtime
```

## Managed Environment Rule

If the managed environment is in a different resource group from the container app, always pass the full managed environment resource ID.

Do not rely on short environment name lookup.

Example:

```powershell
$ManagedEnvId = "/subscriptions/8eb1dbee-a6f3-44b4-9df4-9766109f1ffa/resourceGroups/rg-caberlink-mcp-prod/providers/Microsoft.App/managedEnvironments/cae-caberlink-mcp-prod"
```

## ACA Naming Rule

Azure Container App names must:
- be lower case
- use only alphanumeric characters and '-'
- start with a letter
- end with an alphanumeric character
- not contain '--'
- be less than 32 characters

Prefer shortening system names early.

Example successful name:
- `ca-caberlink-sd-mcp-next`

## First Deploy Pattern

Use `az containerapp create` only when the app does not already exist.

## Update Pattern

Once the app exists, use `az containerapp update`.

Do not rerun `create` blindly, especially when the app already has active revisions pulling from a registry.

## Smoke Script Rule

Commit the smoke script as literal script text.

Do not generate the committed script by interpolating current shell variables into the file body.

## Post-Deploy Capture Rule

After a successful deploy, record all of these in GitHub:
- container app name
- resource group
- managed environment resource ID
- image tag
- FQDN
- MCP URL
- healthy revision
- initialize response
- tools/list response
- health response

## ChatGPT Attachment Rule

After ACA smoke passes, attach the connector in ChatGPT and confirm:
- `health`
- one safe real read call

The deployment is not complete until the connector works from inside ChatGPT, not just from PowerShell.
