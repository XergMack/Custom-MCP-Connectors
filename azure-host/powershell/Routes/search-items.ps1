param(
    [Parameter(Mandatory)]
    [string]$JsonPayload
)

. "$PSScriptRoot\_bootstrap.ps1" -JsonPayload $JsonPayload

$result = Search-ConnectorItems `
    -Page $payload.page `
    -PageSize $payload.page_size `
    -SearchFields $payload.search_fields `
    -AuthContext $authContext `
    -BaseUri $baseUri

$result | ConvertTo-Json -Depth 20
