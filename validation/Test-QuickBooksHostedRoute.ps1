param(
    [Parameter(Mandatory)]
    [string]$BaseUrl
)

$ErrorActionPreference = 'Stop'

$health = Invoke-RestMethod `
    -Method Get `
    -Uri "$($BaseUrl.TrimEnd('/'))/healthz"

$companyInfo = Invoke-RestMethod `
    -Method Post `
    -Uri "$($BaseUrl.TrimEnd('/'))/api/get-company-info" `
    -ContentType 'application/json' `
    -Body '{}'

[pscustomobject]@{
    ok = $true
    base_url = $BaseUrl
    healthz = $health
    company_info = $companyInfo
} | ConvertTo-Json -Depth 20
