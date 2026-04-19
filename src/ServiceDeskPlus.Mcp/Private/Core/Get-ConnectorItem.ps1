function Get-ConnectorItem {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ItemId,

        [Parameter(Mandatory)]
        [hashtable]$AuthContext,

        [Parameter(Mandatory)]
        [string]$BaseUri
    )

    $raw = Invoke-ConnectorApiRequest `
        -Method Get `
        -BaseUri $BaseUri `
        -RelativePath "items/$ItemId" `
        -AuthContext $AuthContext

    [pscustomobject]@{
        id   = $raw.id
        name = $raw.name
        raw  = $raw
    }
}
