param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

. "$PSScriptRoot\_bootstrap.ps1" -JsonPayload $JsonPayload

$result = New-ConnectorItem `
    -Name $payload.name `
    -Description $payload.description `
    -AuthContext $authContext `
    -BaseUri $baseUri

$result | ConvertTo-Json -Depth 20
