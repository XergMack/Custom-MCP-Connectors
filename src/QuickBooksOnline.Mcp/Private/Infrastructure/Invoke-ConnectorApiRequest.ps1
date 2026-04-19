function Invoke-ConnectorApiRequest {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet('Get', 'Post', 'Put', 'Delete')]
        [string]$Method,

        [Parameter(Mandatory)]
        [hashtable]$AuthContext,

        [Parameter(Mandatory)]
        [string]$RelativePath,

        [hashtable]$QueryParameters,

        [object]$Body,

        [string]$RawBody,

        [string]$ContentType = 'application/json',

        [string]$Accept = 'application/json',

        [switch]$PassThruMetadata
    )

    foreach ($requiredKey in @('BaseUri', 'RealmId')) {
        if (-not $AuthContext.ContainsKey($requiredKey) -or [string]::IsNullOrWhiteSpace([string]$AuthContext[$requiredKey])) {
            throw "AuthContext is missing required value: $requiredKey"
        }
    }

    $tokenContext = Invoke-ConnectorTokenRefresh -AuthContext $AuthContext

    $basePath = "$($AuthContext.BaseUri.TrimEnd('/'))/v3/company/$($AuthContext.RealmId)"
    $relative = $RelativePath.TrimStart('/')
    $uri = "$basePath/$relative"

    $queryMap = @{}
    if ($null -ne $QueryParameters) {
        foreach ($key in $QueryParameters.Keys) {
            $queryMap[$key] = $QueryParameters[$key]
        }
    }

    if ($null -ne $AuthContext.MinorVersion -and -not $queryMap.ContainsKey('minorversion')) {
        $queryMap['minorversion'] = [string]$AuthContext.MinorVersion
    }

    if ($queryMap.Count -gt 0) {
        $pairs = New-Object System.Collections.Generic.List[string]

        foreach ($key in ($queryMap.Keys | Sort-Object)) {
            $value = $queryMap[$key]
            if ($null -eq $value) {
                continue
            }

            $pairs.Add(
                ('{0}={1}' -f [uri]::EscapeDataString([string]$key), [uri]::EscapeDataString([string]$value))
            )
        }

        if ($pairs.Count -gt 0) {
            $uri = "$uri?$($pairs -join '&')"
        }
    }

    $headers = @{
        Authorization = "Bearer $($tokenContext.AccessToken)"
        Accept        = $Accept
    }

    $invokeArgs = @{
        Method  = $Method
        Uri     = $uri
        Headers = $headers
    }

    if ($Method -notin @('Get', 'Delete')) {
        if ($PSBoundParameters.ContainsKey('RawBody')) {
            $invokeArgs['Body'] = $RawBody
            $invokeArgs['ContentType'] = $ContentType
        }
        elseif ($null -ne $Body) {
            $invokeArgs['Body'] = ($Body | ConvertTo-Json -Depth 50 -Compress)
            $invokeArgs['ContentType'] = $ContentType
        }
    }

    try {
        $response = Invoke-RestMethod @invokeArgs
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

        $message = "QuickBooks API request failed. Method=$Method Uri=$uri"
        if ($null -ne $statusCode) {
            $message += " StatusCode=$statusCode"
        }
        if (-not [string]::IsNullOrWhiteSpace($responseBody)) {
            $message += " ResponseBody=$responseBody"
        }

        throw $message
    }

    if ($PassThruMetadata) {
        return [pscustomobject]@{
            data = $response
            request = [pscustomobject]@{
                method = $Method
                uri    = $uri
            }
            auth = [pscustomobject]@{
                realm_id                 = [string]$AuthContext.RealmId
                base_uri                 = [string]$AuthContext.BaseUri
                access_token_expires_in  = $tokenContext.AccessTokenExpiresIn
                refresh_token            = $tokenContext.RefreshToken
                refresh_token_changed    = $tokenContext.RefreshTokenChanged
                refresh_token_expires_in = $tokenContext.RefreshTokenExpiresIn
                refreshed_at_utc         = $tokenContext.RefreshedAtUtc
            }
        }
    }

    return $response
}
