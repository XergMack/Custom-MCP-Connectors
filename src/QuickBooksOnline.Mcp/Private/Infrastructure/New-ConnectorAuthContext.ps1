function New-ConnectorAuthContext {
    [CmdletBinding()]
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

        [string]$TokenUri = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer',

        [Nullable[int]]$MinorVersion
    )

    if ([string]::IsNullOrWhiteSpace($BaseUri)) {
        switch ($Environment) {
            'Sandbox' {
                $BaseUri = 'https://sandbox-quickbooks.api.intuit.com'
            }
            default {
                $BaseUri = 'https://quickbooks.api.intuit.com'
            }
        }
    }

    $resolvedMinorVersion = $null
    if ($PSBoundParameters.ContainsKey('MinorVersion') -and $null -ne $MinorVersion) {
        $resolvedMinorVersion = [int]$MinorVersion
    }

    @{
        Vendor                         = 'QuickBooksOnline'
        AuthMode                       = 'OAuth2RefreshToken'
        ClientId                       = $ClientId
        ClientSecret                   = $ClientSecret
        RefreshToken                   = $RefreshToken
        RealmId                        = $RealmId
        Environment                    = $Environment
        BaseUri                        = $BaseUri.TrimEnd('/')
        TokenUri                       = $TokenUri.TrimEnd('/')
        MinorVersion                   = $resolvedMinorVersion
        RequiresRefreshTokenPersistence = $true
    }
}
