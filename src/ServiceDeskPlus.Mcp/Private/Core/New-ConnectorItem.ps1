function New-ConnectorItem {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name,
        [string]$Description,
        [Parameter(Mandatory)]
        [hashtable]$AuthContext,
        [Parameter(Mandatory)]
        [string]$BaseUri
    )

    $body = @{
        name = $Name
    }

    if ($Description) {
        $body.description = $Description
    }

    return Invoke-ConnectorApiRequest `
        -Method Post `
        -BaseUri $BaseUri `
        -RelativePath "items" `
        -AuthContext $AuthContext `
        -Body $body
}
