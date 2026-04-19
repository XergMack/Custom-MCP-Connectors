param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

. "$PSScriptRoot\_bootstrap.ps1" -JsonPayload $JsonPayload

$result = Get-ConnectorItem `
    -ItemId $payload.item_id `
    -AuthContext $authContext `
    -BaseUri $baseUri

$result | ConvertTo-Json -Depth 20
