function New-ConnectorAuthContext {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ApiKey
    )

    @{
        Mode   = "ApiKey"
        ApiKey = $ApiKey
    }
}
