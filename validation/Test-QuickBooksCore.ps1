param(
    [string]$ConnectorSourceRoot = '.\src\QuickBooksOnline.Mcp',

    [Parameter(Mandatory)]
    [string]$ClientId,

    [Parameter(Mandatory)]
    [string]$ClientSecret,

    [Parameter(Mandatory)]
    [string]$RefreshToken,

    [Parameter(Mandatory)]
    [string]$RealmId,

    [ValidateSet('Production', 'Sandbox')]
    [string]$Environment = 'Production',

    [string]$BaseUri,

    [Nullable[int]]$MinorVersion
)

$ErrorActionPreference = 'Stop'

$resolvedSourceRoot = Resolve-Path $ConnectorSourceRoot
$infrastructureRoot = Join-Path $resolvedSourceRoot 'Private\Infrastructure'
$coreRoot = Join-Path $resolvedSourceRoot 'Private\Core'

Get-ChildItem -Path $infrastructureRoot -Filter '*.ps1' -File | Sort-Object Name | ForEach-Object {
    . $_.FullName
}
Get-ChildItem -Path $coreRoot -Filter '*.ps1' -File | Sort-Object Name | ForEach-Object {
    . $_.FullName
}

$authContextArgs = @{
    ClientId = $ClientId
    ClientSecret = $ClientSecret
    RefreshToken = $RefreshToken
    RealmId = $RealmId
    Environment = $Environment
}

if (-not [string]::IsNullOrWhiteSpace($BaseUri)) {
    $authContextArgs['BaseUri'] = $BaseUri
}
if ($PSBoundParameters.ContainsKey('MinorVersion') -and $null -ne $MinorVersion) {
    $authContextArgs['MinorVersion'] = [int]$MinorVersion
}

$authContext = New-ConnectorAuthContext @authContextArgs
$result = Get-ConnectorCompanyInfo -AuthContext $authContext

$result | ConvertTo-Json -Depth 20
