function Search-ConnectorItems {
    [CmdletBinding()]
    param(
        [int]$Page = 1,
        [int]$PageSize = 25,
        [hashtable]$SearchFields,
        [Parameter(Mandatory)]
        [hashtable]$AuthContext,
        [Parameter(Mandatory)]
        [string]$BaseUri
    )

    return Invoke-ConnectorApiRequest `
        -Method Get `
        -BaseUri $BaseUri `
        -RelativePath "items?page=$Page&page_size=$PageSize" `
        -AuthContext $AuthContext
}
