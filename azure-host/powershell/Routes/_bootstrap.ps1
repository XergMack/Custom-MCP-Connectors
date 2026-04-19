param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

$ErrorActionPreference = "Stop"

$payload = $JsonPayload | ConvertFrom-Json -AsHashtable

$baseUri = $env:CONNECTOR_BASE_URI
$apiKey  = $env:CONNECTOR_API_KEY
$srcRoot = $env:MCP_SRC_ROOT

if ([string]::IsNullOrWhiteSpace($baseUri)) { throw "CONNECTOR_BASE_URI is not set." }
if ([string]::IsNullOrWhiteSpace($apiKey))  { throw "CONNECTOR_API_KEY is not set." }

if ([string]::IsNullOrWhiteSpace($srcRoot)) {
    $srcRoot = "/service/src/ServiceDeskPlus.Mcp"
}

if (-not (Test-Path $srcRoot)) {
    throw "Connector source root not found: $srcRoot"
}

. (Join-Path $srcRoot "Private\Infrastructure\Invoke-ConnectorApiRequest.ps1")
. (Join-Path $srcRoot "Private\Infrastructure\New-ConnectorAuthContext.ps1")
. (Join-Path $srcRoot "Private\Core\Get-ConnectorItem.ps1")
. (Join-Path $srcRoot "Private\Core\Search-ConnectorItems.ps1")
. (Join-Path $srcRoot "Private\Core\New-ConnectorItem.ps1")
. (Join-Path $srcRoot "Private\Core\Update-ConnectorItem.ps1")

$authContext = New-ConnectorAuthContext -ApiKey $apiKey




