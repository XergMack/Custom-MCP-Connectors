param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

. "$PSScriptRoot\_bootstrap.ps1" -JsonPayload $JsonPayload

$result = Update-ConnectorItem `
    -ItemId $payload.item_id `
    -Fields $payload.fields `
    -AuthContext $authContext `
    -BaseUri $baseUri

$result | ConvertTo-Json -Depth 20
