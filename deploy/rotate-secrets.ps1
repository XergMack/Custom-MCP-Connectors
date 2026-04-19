param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,
    [Parameter(Mandatory)]
    [string]$AppName,
    [Parameter(Mandatory)]
    [string]$ConnectorApiKey
)

$ErrorActionPreference = "Stop"

az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings CONNECTOR_API_KEY=$ConnectorApiKey | Out-Null

az webapp restart --name $AppName --resource-group $ResourceGroup | Out-Null
