param(
    [Parameter(Mandatory)]
    [string]$ResourceGroup,
    [Parameter(Mandatory)]
    [string]$AppName,
    [Parameter(Mandatory)]
    [string]$AcrName,
    [Parameter(Mandatory)]
    [string]$ImageTag,
    [Parameter(Mandatory)]
    [string]$ConnectorBaseUri,
    [Parameter(Mandatory)]
    [string]$ConnectorApiKey
)

$ErrorActionPreference = "Stop"

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

az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings `
        WEBSITES_PORT=8000 `
        CONNECTOR_BASE_URI=$ConnectorBaseUri `
        CONNECTOR_API_KEY=$ConnectorApiKey `
        MCP_ROUTES_ROOT=/service/powershell/Routes `
        MCP_SRC_ROOT=/service/src/ServiceDeskPlus.Mcp | Out-Null

az webapp restart --name $AppName --resource-group $ResourceGroup | Out-Null


