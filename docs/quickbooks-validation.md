# QuickBooks Online Validation Runbook

This runbook validates the QuickBooks Online connector in the same strict order used for the proven starter pattern.

## Required values

- `QBO_CLIENT_ID`
- `QBO_CLIENT_SECRET`
- `QBO_REFRESH_TOKEN`
- `QBO_REALM_ID`
- `QBO_ENVIRONMENT` (`Production` or `Sandbox`)
- optional: `QBO_MINOR_VERSION`

## 1. Raw vendor auth + API proof

Run:

```powershell
pwsh ./validation/Test-QuickBooksRawAuth.ps1 `
  -ClientId $env:QBO_CLIENT_ID `
  -ClientSecret $env:QBO_CLIENT_SECRET `
  -RefreshToken $env:QBO_REFRESH_TOKEN `
  -RealmId $env:QBO_REALM_ID `
  -Environment $env:QBO_ENVIRONMENT
```

Success criteria:

- token refresh succeeds
- access token is returned
- `select * from companyinfo` succeeds
- company identity is returned
- note whether a new refresh token was returned

If a new refresh token is returned, persist it before moving on.

## 2. Direct core proof

Run:

```powershell
pwsh ./validation/Test-QuickBooksCore.ps1 `
  -ConnectorSourceRoot ./src/QuickBooksOnline.Mcp `
  -ClientId $env:QBO_CLIENT_ID `
  -ClientSecret $env:QBO_CLIENT_SECRET `
  -RefreshToken $env:QBO_REFRESH_TOKEN `
  -RealmId $env:QBO_REALM_ID `
  -Environment $env:QBO_ENVIRONMENT
```

Success criteria:

- PowerShell auth context builds
- token refresh happens through infrastructure layer
- `Get-ConnectorCompanyInfo` succeeds
- normalized JSON is returned

## 3. Local host proof

Example local environment:

```powershell
$env:CONNECTOR_AUTH_MODE = 'QuickBooksOAuth'
$env:MCP_SRC_ROOT = '/service/src/QuickBooksOnline.Mcp'
$env:MCP_ROUTES_ROOT = '/service/powershell/Routes'
$env:QBO_CLIENT_ID = '<client id>'
$env:QBO_CLIENT_SECRET = '<client secret>'
$env:QBO_REFRESH_TOKEN = '<refresh token>'
$env:QBO_REALM_ID = '<realm id>'
$env:QBO_ENVIRONMENT = 'Sandbox'
```

Then validate:

```powershell
pwsh ./validation/Test-QuickBooksLocalHost.ps1 -BaseUrl 'http://localhost:8000'
```

Success criteria:

- `/healthz` returns `connectorAuthMode=QuickBooksOAuth`
- `/api/get-company-info` succeeds
- returned company info matches direct core proof

## 4. Azure hosted proof

Deploy with QuickBooks settings:

```powershell
pwsh ./deploy/deploy-azure.ps1 `
  -ResourceGroup '<rg>' `
  -AppName '<app>' `
  -AcrName '<acr>' `
  -ImageTag 'qbo-proof' `
  -ConnectorAuthMode QuickBooksOAuth `
  -ConnectorSourceRoot '/service/src/QuickBooksOnline.Mcp' `
  -QboClientId $env:QBO_CLIENT_ID `
  -QboClientSecret $env:QBO_CLIENT_SECRET `
  -QboRefreshToken $env:QBO_REFRESH_TOKEN `
  -QboRealmId $env:QBO_REALM_ID `
  -QboEnvironment $env:QBO_ENVIRONMENT
```

Then validate:

```powershell
pwsh ./validation/Test-QuickBooksHostedRoute.ps1 -BaseUrl 'https://<app>.azurewebsites.net'
```

Success criteria:

- hosted `/healthz` reports QuickBooks auth mode
- hosted `/api/get-company-info` succeeds
- company identity matches raw and local proofs

## Refresh token handling

QuickBooks may return a new refresh token during refresh. If so:

1. persist the new value
2. update Azure app settings
3. restart the app if needed

Use:

```powershell
pwsh ./deploy/rotate-secrets.ps1 `
  -ResourceGroup '<rg>' `
  -AppName '<app>' `
  -ConnectorAuthMode QuickBooksOAuth `
  -QboRefreshToken '<new refresh token>'
```

Do not continue testing with an old refresh token after a successful refresh returned a newer value.
