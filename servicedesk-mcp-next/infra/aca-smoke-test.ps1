param(
    [Parameter(Mandatory = $true)]
    [string]$McpUrl
)

$ErrorActionPreference = "Stop"

$AcceptHeader = "application/json, text/event-stream"
$ProtocolHeader = "2024-11-05"
$OutDir = ".\_aca_smoke"

Remove-Item -Recurse -Force $OutDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$InitHeaders = Join-Path $OutDir "init-headers.txt"
$InitBody = Join-Path $OutDir "init-body.json"
$ReadyBody = Join-Path $OutDir "ready-body.txt"
$ToolsBody = Join-Path $OutDir "tools-body.json"
$HealthBody = Join-Path $OutDir "health-body.json"

$InitPayloadFile = Join-Path $OutDir "init-payload.json"
$ReadyPayloadFile = Join-Path $OutDir "ready-payload.json"
$ToolsPayloadFile = Join-Path $OutDir "tools-payload.json"
$HealthPayloadFile = Join-Path $OutDir "health-payload.json"

Set-Content -Path $InitPayloadFile -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"aca-smoke","version":"1.0"}}}'
Set-Content -Path $ReadyPayloadFile -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","method":"notifications/initialized"}'
Set-Content -Path $ToolsPayloadFile -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
Set-Content -Path $HealthPayloadFile -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"health","arguments":{}}}'

curl.exe -sS -D $InitHeaders -o $InitBody -H "Accept: $AcceptHeader" -H "Content-Type: application/json" -X POST $McpUrl --data-binary "@$InitPayloadFile"

$sessionLine = Select-String -Path $InitHeaders -Pattern "^mcp-session-id:\s*(.+)$" -CaseSensitive:$false | Select-Object -First 1
if (-not $sessionLine) { throw "No mcp-session-id returned from initialize." }
$sessionId = $sessionLine.Matches[0].Groups[1].Value.Trim()

curl.exe -sS -o $ReadyBody -H "Accept: $AcceptHeader" -H "Content-Type: application/json" -H "MCP-Protocol-Version: $ProtocolHeader" -H "mcp-session-id: $sessionId" -X POST $McpUrl --data-binary "@$ReadyPayloadFile"
curl.exe -sS -o $ToolsBody -H "Accept: $AcceptHeader" -H "Content-Type: application/json" -H "MCP-Protocol-Version: $ProtocolHeader" -H "mcp-session-id: $sessionId" -X POST $McpUrl --data-binary "@$ToolsPayloadFile"
curl.exe -sS -o $HealthBody -H "Accept: $AcceptHeader" -H "Content-Type: application/json" -H "MCP-Protocol-Version: $ProtocolHeader" -H "mcp-session-id: $sessionId" -X POST $McpUrl --data-binary "@$HealthPayloadFile"

Write-Host "===== init ====="
Get-Content $InitBody
Write-Host ""
Write-Host "===== tools ====="
Get-Content $ToolsBody
Write-Host ""
Write-Host "===== health ====="
Get-Content $HealthBody
