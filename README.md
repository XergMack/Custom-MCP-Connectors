# MCP Connector Starter

This repository is the reusable baseline for CaberLink hosted MCP-style connectors.

## Purpose

This starter exists so new connectors do not have to re-solve:

- HTTP host design
- PowerShell route execution
- container filesystem layout
- Azure App Service packaging
- runtime path handling
- environment-variable configuration
- validation sequence

The intended pattern is:

HTTP host -> PowerShell route -> PowerShell core -> vendor API

## Design rules

### 1. The host stays dumb
The FastAPI host is only responsible for:

- exposing HTTP endpoints
- mapping endpoint names to route scripts
- passing JSON payloads to PowerShell
- returning JSON output
- exposing `/healthz`

The host should not contain vendor-specific logic.

### 2. Routes stay thin
Each route script should:

- accept `-JsonPayload`
- dot-source `_bootstrap.ps1`
- call exactly one core function
- emit JSON output

Routes should not contain business logic.

### 3. The core is authoritative
The PowerShell core owns:

- vendor API endpoint mapping
- auth/header semantics
- request formatting
- normalization of responses
- create/update/search behavior
- vendor quirks

This is the only layer that should materially change from connector to connector.

### 4. Environment owns config
Runtime configuration must come from environment variables, not hardcoded local paths.

Standard variables:

- `CONNECTOR_BASE_URI`
- `CONNECTOR_API_KEY`
- `MCP_ROUTES_ROOT`
- `MCP_SRC_ROOT`
- `WEBSITES_PORT`

### 5. Container layout is fixed
Azure container layout should remain:

- `/service/host-python`
- `/service/powershell`
- `/service/src`

Do not redesign this unless there is a compelling reason.

## What changes for a new connector

For a new system, replace only:

- `src\<ConnectorName>\Private\Infrastructure\Invoke-ConnectorApiRequest.ps1`
- `src\<ConnectorName>\Private\Infrastructure\New-ConnectorAuthContext.ps1`
- `src\<ConnectorName>\Private\Core\*.ps1`

Optionally rename route nouns if `item` is not the right generic object name.

Keep these as the baseline:

- `azure-host/host-python/app.py`
- `azure-host/powershell/Routes/_bootstrap.ps1`
- `azure-host/Dockerfile.appservice`
- `deploy/*.ps1`
- `docs/*.md`

## Bring-up / validation ladder

Always validate in this exact order:

1. Raw vendor API call
2. Direct PowerShell core function
3. Local `/healthz`
4. Local route invocation
5. Azure image build
6. Azure `/healthz`
7. Azure read route
8. Azure write route
9. Secret rotation after proof

Do not skip layers. Skipping layers reintroduces ambiguity.

## ServiceDesk Plus-specific note

ServiceDesk Plus v3 does NOT use generic Bearer-token JSON requests in this implementation.

The proven contract is:

- `authtoken: <api key>`
- `Accept: application/vnd.manageengine.sdp.v3+json`
- GET reads against `/api/v3/...`
- POST/PUT using `application/x-www-form-urlencoded`
- structured payload passed as `input_data=<json>`

That behavior belongs in the core infrastructure layer, not the HTTP host.

## Outcome this starter is meant to preserve

This starter is intended to preserve a repeatable connector pattern:

- deterministic validation
- reusable transport
- reusable deployment
- reusable pathing
- system-specific core only

The guiding rule is:

**Everything reusable stays above the core. Everything system-specific stays in the core.**


