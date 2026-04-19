param(
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

    [string]$TokenUri = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($BaseUri)) {
    switch ($Environment) {
        'Sandbox' { $BaseUri = 'https://sandbox-quickbooks.api.intuit.com' }
        default   { $BaseUri = 'https://quickbooks.api.intuit.com' }
    }
}

$credentialBytes = [System.Text.Encoding]::ASCII.GetBytes("${ClientId}:${ClientSecret}")
$basicToken = [Convert]::ToBase64String($credentialBytes)

$tokenHeaders = @{
    Authorization = "Basic $basicToken"
    Accept        = 'application/json'
}

$tokenBody = "grant_type=refresh_token&refresh_token=$([uri]::EscapeDataString($RefreshToken))"
$tokenResponse = Invoke-RestMethod `
    -Method Post `
    -Uri $TokenUri `
    -Headers $tokenHeaders `
    -ContentType 'application/x-www-form-urlencoded' `
    -Body $tokenBody

if ([string]::IsNullOrWhiteSpace([string]$tokenResponse.access_token)) {
    throw 'Token refresh succeeded but did not return an access_token.'
}

$query = 'select * from companyinfo'
$queryUri = "$($BaseUri.TrimEnd('/'))/v3/company/$RealmId/query?query=$([uri]::EscapeDataString($query))"

$apiHeaders = @{
    Authorization = "Bearer $($tokenResponse.access_token)"
    Accept        = 'application/json'
}

$companyResponse = Invoke-RestMethod `
    -Method Get `
    -Uri $queryUri `
    -Headers $apiHeaders

$companyInfo = $null
if ($null -ne $companyResponse.QueryResponse) {
    if ($companyResponse.QueryResponse.CompanyInfo -is [System.Array]) {
        if ($companyResponse.QueryResponse.CompanyInfo.Count -gt 0) {
            $companyInfo = $companyResponse.QueryResponse.CompanyInfo[0]
        }
    }
    else {
        $companyInfo = $companyResponse.QueryResponse.CompanyInfo
    }
}

if ($null -eq $companyInfo) {
    throw 'Raw QuickBooks company query succeeded but returned no CompanyInfo entity.'
}

[pscustomobject]@{
    ok                    = $true
    environment           = $Environment
    token_uri             = $TokenUri
    api_base_uri          = $BaseUri
    realm_id              = $RealmId
    access_token_present  = $true
    access_token_expires  = $tokenResponse.expires_in
    refresh_token_changed = ([string]$tokenResponse.refresh_token -ne [string]$RefreshToken)
    new_refresh_token     = [string]$tokenResponse.refresh_token
    company_name          = [string]($companyInfo.CompanyName ?? $companyInfo.LegalName ?? $companyInfo.Name)
    company_id            = [string]($companyInfo.Id ?? $RealmId)
    raw_company_info      = $companyInfo
} | ConvertTo-Json -Depth 20
