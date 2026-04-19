function Invoke-ConnectorApiRequest {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet('Get','Post','Put','Delete')]
        [string]$Method,

        [Parameter(Mandatory)]
        [string]$BaseUri,

        [Parameter(Mandatory)]
        [string]$RelativePath,

        [Parameter()]
        [hashtable]$AuthContext,

        [Parameter()]
        [hashtable]$Body
    )

    $uri = "$BaseUri/$RelativePath".TrimEnd('/')

    $headers = @{
        "authtoken" = [string]$AuthContext.ApiKey
        "Accept"    = "application/vnd.manageengine.sdp.v3+json"
    }

    $inputDataJson = $null
    if ($null -ne $Body) {
        $inputDataJson = ($Body | ConvertTo-Json -Depth 20 -Compress)
    }

    try {
        if ($Method -eq "Get") {
            if ($inputDataJson) {
                $uri = "$uri?input_data=$([uri]::EscapeDataString($inputDataJson))"
            }

            Write-Verbose "ServiceDesk API request: $Method $uri"

            return Invoke-RestMethod `
                -Method Get `
                -Uri $uri `
                -Headers $headers
        }

        $formBody = @{}
        if ($inputDataJson) {
            $formBody["input_data"] = $inputDataJson
        }

        Write-Verbose "ServiceDesk API request: $Method $uri"

        return Invoke-RestMethod `
            -Method $Method `
            -Uri $uri `
            -Headers $headers `
            -ContentType "application/x-www-form-urlencoded" `
            -Body $formBody
    }
    catch {
        $statusCode = $null
        $responseBody = $null

        if ($_.Exception.Response) {
            try {
                $statusCode = [int]$_.Exception.Response.StatusCode
            } catch {}

            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $responseBody = $reader.ReadToEnd()
                $reader.Dispose()
            } catch {}
        }

        $message = "ServiceDesk API request failed. Method=$Method Uri=$uri"
        if ($null -ne $statusCode) {
            $message += " StatusCode=$statusCode"
        }
        if (-not [string]::IsNullOrWhiteSpace($responseBody)) {
            $message += " ResponseBody=$responseBody"
        }

        throw $message
    }
}
