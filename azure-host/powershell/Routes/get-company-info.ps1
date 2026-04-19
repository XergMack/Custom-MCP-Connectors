param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

. "$PSScriptRoot\_bootstrap.ps1" -JsonPayload $JsonPayload

$result = Get-ConnectorCompanyInfo -AuthContext $authContext

$result | ConvertTo-Json -Depth 20
