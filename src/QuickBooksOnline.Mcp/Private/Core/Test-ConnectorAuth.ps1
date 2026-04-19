function Test-ConnectorAuth {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$AuthContext
    )

    $companyInfo = Get-ConnectorCompanyInfo -AuthContext $AuthContext

    [pscustomobject]@{
        ok           = $true
        vendor       = 'QuickBooksOnline'
        auth_mode    = [string]$AuthContext.AuthMode
        environment  = [string]$AuthContext.Environment
        realm_id     = [string]$AuthContext.RealmId
        company_name = $companyInfo.company_name
        company_info = $companyInfo
    }
}
