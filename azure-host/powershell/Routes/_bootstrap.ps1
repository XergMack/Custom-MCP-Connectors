param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

$ErrorActionPreference = "Stop"

$payload = $JsonPayload | ConvertFrom-Json -AsHashtable

$srcRoot = $env:MCP_SRC_ROOT
if ([string]::IsNullOrWhiteSpace($srcRoot)) {
    $srcRoot = "/service/src/QuickBooksOnline.Mcp"
}

if (-not (Test-Path $srcRoot)) {
    throw "Connector source root not found: $srcRoot"
}

$infrastructureRoot = Join-Path $srcRoot "Private\Infrastructure"
$coreRoot = Join-Path $srcRoot "Private\Core"

if (-not (Test-Path $infrastructureRoot)) {
    throw "Connector infrastructure root not found: $infrastructureRoot"
}
if (-not (Test-Path $coreRoot)) {
    throw "Connector core root not found: $coreRoot"
}

Get-ChildItem -Path $infrastructureRoot -Filter '*.ps1' -File | Sort-Object Name | ForEach-Object {
    . $_.FullName
}
Get-ChildItem -Path $coreRoot -Filter '*.ps1' -File | Sort-Object Name | ForEach-Object {
    . $_.FullName
}

$connectorAuthMode = $env:CONNECTOR_AUTH_MODE
if ([string]::IsNullOrWhiteSpace($connectorAuthMode)) {
    $connectorAuthMode = 'ApiKey'
}

$baseUri = $env:CONNECTOR_BASE_URI

switch ($connectorAuthMode) {
    'ApiKey' {
        $apiKey = $env:CONNECTOR_API_KEY

        if ([string]::IsNullOrWhiteSpace($baseUri)) { throw "CONNECTOR_BASE_URI is not set." }
        if ([string]::IsNullOrWhiteSpace($apiKey)) { throw "CONNECTOR_API_KEY is not set." }

        $authContext = New-ConnectorAuthContext -ApiKey $apiKey
    }

    'QuickBooksOAuth' {
        $qboClientId = $env:QBO_CLIENT_ID
        $qboClientSecret = $env:QBO_CLIENT_SECRET
        $qboRefreshToken = $env:QBO_REFRESH_TOKEN
        $qboRealmId = $env:QBO_REALM_ID
        $qboEnvironment = $env:QBO_ENVIRONMENT
        $qboMinorVersion = $env:QBO_MINOR_VERSION

        if ([string]::IsNullOrWhiteSpace($qboClientId)) { throw "QBO_CLIENT_ID is not set." }
        if ([string]::IsNullOrWhiteSpace($qboClientSecret)) { throw "QBO_CLIENT_SECRET is not set." }
        if ([string]::IsNullOrWhiteSpace($qboRefreshToken)) { throw "QBO_REFRESH_TOKEN is not set." }
        if ([string]::IsNullOrWhiteSpace($qboRealmId)) { throw "QBO_REALM_ID is not set." }
        if ([string]::IsNullOrWhiteSpace($qboEnvironment)) { $qboEnvironment = 'Production' }

        $authContextArgs = @{
            ClientId = $qboClientId
            ClientSecret = $qboClientSecret
            RefreshToken = $qboRefreshToken
            RealmId = $qboRealmId
            Environment = $qboEnvironment
        }

        if (-not [string]::IsNullOrWhiteSpace($baseUri)) {
            $authContextArgs['BaseUri'] = $baseUri
        }
        if (-not [string]::IsNullOrWhiteSpace($qboMinorVersion)) {
            $authContextArgs['MinorVersion'] = [int]$qboMinorVersion
        }

        $authContext = New-ConnectorAuthContext @authContextArgs
        $baseUri = [string]$authContext.BaseUri
    }

    default {
        throw "Unsupported CONNECTOR_AUTH_MODE: $connectorAuthMode"
    }
}
