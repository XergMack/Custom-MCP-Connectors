param(
    [Parameter(Mandatory)]
    [string]$ConnectorName,

    [Parameter()]
    [string]$RemoteUrl = "https://github.com/XergMack/Custom-MCP-Connectors.git",

    [Parameter()]
    [string]$InitialTag = "v0.1.0"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$templatePath = ".\src\Connector.Template.Mcp"
$targetPath   = ".\src\$ConnectorName"

if (Test-Path $templatePath) {
    Rename-Item $templatePath $ConnectorName
}

$filesToPatch = @(
    ".\README.md",
    ".\azure-host\host-python\app.py",
    ".\azure-host\powershell\Routes\_bootstrap.ps1",
    ".\deploy\deploy-azure.ps1",
    ".\docs\architecture.md",
    ".\docs\route-contract.md",
    ".\docs\validation-checklist.md"
) | Where-Object { Test-Path $_ }

foreach ($file in $filesToPatch) {
    $content = Get-Content $file -Raw
    $content = $content -replace 'Connector\.Template\.Mcp', $ConnectorName
    Set-Content $file $content -Encoding UTF8
}

git rev-parse --is-inside-work-tree 1>$null 2>$null
if ($LASTEXITCODE -ne 0) {
    git init | Out-Null
}

$hasName  = git config user.name
$hasEmail = git config user.email

if (-not $hasName) {
    git config user.name "Matt MacKinnon"
}
if (-not $hasEmail) {
    git config user.email "matt@caberlink.com"
}

git remote get-url origin 1>$null 2>$null
if ($LASTEXITCODE -eq 0) {
    git remote remove origin
}

git remote add origin $RemoteUrl

git add .
git commit -m "Initialize $ConnectorName from MCP connector starter"
git tag -f $InitialTag

Write-Host ""
Write-Host "Initialized connector repo." -ForegroundColor Green
Write-Host "ConnectorName : $ConnectorName"
Write-Host "RemoteUrl     : $RemoteUrl"
Write-Host "InitialTag    : $InitialTag"
Write-Host ""
Write-Host "Next commands:" -ForegroundColor Cyan
Write-Host "git branch -M main"
Write-Host "git push -u origin main --tags"
