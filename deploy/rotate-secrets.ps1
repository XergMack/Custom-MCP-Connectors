param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,

    [Parameter(Mandatory)]
    [string]$AppName,

    [ValidateSet('ApiKey', 'QuickBooksOAuth')]
    [string]$ConnectorAuthMode = 'QuickBooksOAuth',

    [string]$ConnectorApiKey,

    [string]$QboClientSecret,

    [string]$QboRefreshToken
)

$ErrorActionPreference = 'Stop'

$settings = @()

switch ($ConnectorAuthMode) {
    'ApiKey' {
        if ([string]::IsNullOrWhiteSpace($ConnectorApiKey)) {
            throw 'ConnectorApiKey is required for ApiKey mode.'
        }

        $settings += "CONNECTOR_API_KEY=$ConnectorApiKey"
    }

    'QuickBooksOAuth' {
        if ([string]::IsNullOrWhiteSpace($QboClientSecret) -and [string]::IsNullOrWhiteSpace($QboRefreshToken)) {
            throw 'Provide QboClientSecret and/or QboRefreshToken for QuickBooksOAuth mode.'
        }

        if (-not [string]::IsNullOrWhiteSpace($QboClientSecret)) {
            $settings += "QBO_CLIENT_SECRET=$QboClientSecret"
        }
        if (-not [string]::IsNullOrWhiteSpace($QboRefreshToken)) {
            $settings += "QBO_REFRESH_TOKEN=$QboRefreshToken"
        }
    }
}

& az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings $settings | Out-Null

az webapp restart --name $AppName --resource-group $ResourceGroup | Out-Null
