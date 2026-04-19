param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [Parameter(Mandatory)]
    [string]$AppName,

    [Parameter(Mandatory)]
    [string]$AcrName,

    [Parameter(Mandatory)]
    [string]$ImageTag,

    [ValidateSet('ApiKey', 'QuickBooksOAuth')]
    [string]$ConnectorAuthMode = 'QuickBooksOAuth',

    [string]$ConnectorSourceRoot = '/service/src/QuickBooksOnline.Mcp',

    [string]$ConnectorBaseUri,

    [string]$ConnectorApiKey,

    [string]$QboClientId,

    [string]$QboClientSecret,

    [string]$QboRefreshToken,

    [string]$QboRealmId,

    [ValidateSet('Production', 'Sandbox')]
    [string]$QboEnvironment = 'Production',

    [Nullable[int]]$QboMinorVersion
)

$ErrorActionPreference = 'Stop'

$acrLoginServer = az acr show --name $AcrName --resource-group $ResourceGroup --query loginServer -o tsv
$imageRef = "$acrLoginServer/connector-template-mcp`:$ImageTag"

az acr build `
    --registry $AcrName `
    --image "connector-template-mcp`:$ImageTag" `
    --file ".\azure-host\Dockerfile.appservice" `
    .

$acrUser = az acr credential show --name $AcrName --resource-group $ResourceGroup --query username -o tsv
$acrPass = az acr credential show --name $AcrName --resource-group $ResourceGroup --query "passwords[0].value" -o tsv

az webapp config container set `
    --name $AppName `
    --resource-group $ResourceGroup `
    --container-image-name $imageRef `
    --container-registry-url "https://$acrLoginServer" `
    --container-registry-user $acrUser `
    --container-registry-password $acrPass | Out-Null

$settings = @(
    'WEBSITES_PORT=8000',
    "CONNECTOR_AUTH_MODE=$ConnectorAuthMode",
    'MCP_ROUTES_ROOT=/service/powershell/Routes',
    "MCP_SRC_ROOT=$ConnectorSourceRoot"
)

if (-not [string]::IsNullOrWhiteSpace($ConnectorBaseUri)) {
    $settings += "CONNECTOR_BASE_URI=$ConnectorBaseUri"
}

switch ($ConnectorAuthMode) {
    'ApiKey' {
        if ([string]::IsNullOrWhiteSpace($ConnectorBaseUri)) { throw 'ConnectorBaseUri is required for ApiKey mode.' }
        if ([string]::IsNullOrWhiteSpace($ConnectorApiKey)) { throw 'ConnectorApiKey is required for ApiKey mode.' }

        $settings += "CONNECTOR_API_KEY=$ConnectorApiKey"
    }

    'QuickBooksOAuth' {
        if ([string]::IsNullOrWhiteSpace($QboClientId)) { throw 'QboClientId is required for QuickBooksOAuth mode.' }
        if ([string]::IsNullOrWhiteSpace($QboClientSecret)) { throw 'QboClientSecret is required for QuickBooksOAuth mode.' }
        if ([string]::IsNullOrWhiteSpace($QboRefreshToken)) { throw 'QboRefreshToken is required for QuickBooksOAuth mode.' }
        if ([string]::IsNullOrWhiteSpace($QboRealmId)) { throw 'QboRealmId is required for QuickBooksOAuth mode.' }

        $settings += @(
            "QBO_CLIENT_ID=$QboClientId",
            "QBO_CLIENT_SECRET=$QboClientSecret",
            "QBO_REFRESH_TOKEN=$QboRefreshToken",
            "QBO_REALM_ID=$QboRealmId",
            "QBO_ENVIRONMENT=$QboEnvironment"
        )

        if ($PSBoundParameters.ContainsKey('QboMinorVersion') -and $null -ne $QboMinorVersion) {
            $settings += "QBO_MINOR_VERSION=$([int]$QboMinorVersion)"
        }
    }
}

& az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings $settings | Out-Null

az webapp restart --name $AppName --resource-group $ResourceGroup | Out-Null
