function Invoke-ConnectorTokenRefresh {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$AuthContext
    )

    foreach ($requiredKey in @('ClientId', 'ClientSecret', 'RefreshToken', 'TokenUri')) {
        if (-not $AuthContext.ContainsKey($requiredKey) -or [string]::IsNullOrWhiteSpace([string]$AuthContext[$requiredKey])) {
            throw "AuthContext is missing required value: $requiredKey"
        }
    }

    $credentialBytes = [System.Text.Encoding]::ASCII.GetBytes("$($AuthContext.ClientId):$($AuthContext.ClientSecret)")
    $basicToken = [Convert]::ToBase64String($credentialBytes)

    $headers = @{
        Authorization = "Basic $basicToken"
        Accept        = 'application/json'
    }

    $body = "grant_type=refresh_token&refresh_token=$([uri]::EscapeDataString([string]$AuthContext.RefreshToken))"

    try {
        $response = Invoke-RestMethod `
            -Method Post `
            -Uri $AuthContext.TokenUri `
            -Headers $headers `
            -ContentType 'application/x-www-form-urlencoded' `
            -Body $body
    }
    catch {
        $statusCode = $null
        $responseBody = $null

        if ($_.Exception.Response) {
            try {
                $statusCode = [int]$_.Exception.Response.StatusCode
            }
            catch {}

            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $responseBody = $reader.ReadToEnd()
                $reader.Dispose()
            }
            catch {}
        }

        $message = "QuickBooks token refresh failed. TokenUri=$($AuthContext.TokenUri)"
        if ($null -ne $statusCode) {
            $message += " StatusCode=$statusCode"
        }
        if (-not [string]::IsNullOrWhiteSpace($responseBody)) {
            $message += " ResponseBody=$responseBody"
        }

        throw $message
    }

    $newRefreshToken = [string]$AuthContext.RefreshToken
    if ($null -ne $response.PSObject.Properties['refresh_token'] -and -not [string]::IsNullOrWhiteSpace([string]$response.refresh_token)) {
        $newRefreshToken = [string]$response.refresh_token
    }

    $refreshTokenExpiresIn = $null
    if ($null -ne $response.PSObject.Properties['x_refresh_token_expires_in'] -and $null -ne $response.x_refresh_token_expires_in) {
        $refreshTokenExpiresIn = [int]$response.x_refresh_token_expires_in
    }

    [pscustomobject]@{
        AccessToken            = [string]$response.access_token
        RefreshToken           = $newRefreshToken
        RefreshTokenChanged    = ($newRefreshToken -ne [string]$AuthContext.RefreshToken)
        TokenType              = [string]$response.token_type
        AccessTokenExpiresIn   = [int]$response.expires_in
        RefreshTokenExpiresIn  = $refreshTokenExpiresIn
        RefreshedAtUtc         = (Get-Date).ToUniversalTime().ToString('o')
        Raw                    = $response
    }
}
