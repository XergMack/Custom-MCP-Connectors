function Get-ConnectorCompanyInfo {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$AuthContext
    )

    $result = Invoke-ConnectorApiRequest `
        -Method Get `
        -AuthContext $AuthContext `
        -RelativePath 'query' `
        -QueryParameters @{ query = 'select * from companyinfo' } `
        -PassThruMetadata

    $queryResponse = $result.data.QueryResponse
    $companyInfo = $null

    if ($null -ne $queryResponse) {
        if ($queryResponse.CompanyInfo -is [System.Array]) {
            if ($queryResponse.CompanyInfo.Count -gt 0) {
                $companyInfo = $queryResponse.CompanyInfo[0]
            }
        }
        else {
            $companyInfo = $queryResponse.CompanyInfo
        }
    }

    if ($null -eq $companyInfo) {
        throw 'QuickBooks CompanyInfo query succeeded but returned no CompanyInfo entity.'
    }

    $companyId = [string]$AuthContext.RealmId
    if ($null -ne $companyInfo.PSObject.Properties['Id'] -and -not [string]::IsNullOrWhiteSpace([string]$companyInfo.Id)) {
        $companyId = [string]$companyInfo.Id
    }

    $displayName = $null
    foreach ($candidate in @($companyInfo.CompanyName, $companyInfo.LegalName, $companyInfo.Name)) {
        if (-not [string]::IsNullOrWhiteSpace([string]$candidate)) {
            $displayName = [string]$candidate
            break
        }
    }

    $emailAddress = $null
    if ($null -ne $companyInfo.PSObject.Properties['Email'] -and $null -ne $companyInfo.Email) {
        if ($null -ne $companyInfo.Email.PSObject.Properties['Address'] -and -not [string]::IsNullOrWhiteSpace([string]$companyInfo.Email.Address)) {
            $emailAddress = [string]$companyInfo.Email.Address
        }
    }

    $webAddress = $null
    if ($null -ne $companyInfo.PSObject.Properties['WebAddr'] -and $null -ne $companyInfo.WebAddr) {
        if ($null -ne $companyInfo.WebAddr.PSObject.Properties['URI'] -and -not [string]::IsNullOrWhiteSpace([string]$companyInfo.WebAddr.URI)) {
            $webAddress = [string]$companyInfo.WebAddr.URI
        }
    }

    [pscustomobject]@{
        id           = $companyId
        realm_id     = [string]$AuthContext.RealmId
        company_name = $displayName
        legal_name   = [string]$companyInfo.LegalName
        country      = [string]$companyInfo.Country
        email        = $emailAddress
        web_addr     = $webAddress
        sync_token   = [string]$companyInfo.SyncToken
        request      = $result.request
        auth         = $result.auth
        raw          = $companyInfo
    }
}
