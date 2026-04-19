function Update-ConnectorItem {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ItemId,
        [Parameter(Mandatory)]
        [hashtable]$Fields,
        [Parameter(Mandatory)]
        [hashtable]$AuthContext,
        [Parameter(Mandatory)]
        [string]$BaseUri
    )

    return Invoke-ConnectorApiRequest `
        -Method Put `
        -BaseUri $BaseUri `
        -RelativePath "items/$ItemId" `
        -AuthContext $AuthContext `
        -Body $Fields
}
