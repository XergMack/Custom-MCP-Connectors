param(
    [Parameter(Mandatory = True)][string]
)

Stop = "Stop"

application/json, text/event-stream = "application/json, text/event-stream"
2024-11-05 = "2024-11-05"
.\_smoke = ".\_aca_smoke"
New-Item -ItemType Directory -Force -Path .\_smoke | Out-Null

.\_smoke\init-headers.txt = Join-Path .\_smoke "init-headers.txt"
.\_smoke\init-body.json = Join-Path .\_smoke "init-body.json"
.\_smoke\ready-body.txt = Join-Path .\_smoke "ready-body.txt"
.\_smoke\tools-body.json = Join-Path .\_smoke "tools-body.json"
.\_smoke\health-body.json = Join-Path .\_smoke "health-body.json"

.\_smoke\init-payload.json = Join-Path .\_smoke "init-payload.json"
.\_smoke\ready-payload.json = Join-Path .\_smoke "ready-payload.json"
.\_smoke\tools-payload.json = Join-Path .\_smoke "tools-payload.json"
.\_smoke\health-payload.json = Join-Path .\_smoke "health-payload.json"

Set-Content -Path .\_smoke\init-payload.json -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"aca-smoke","version":"1.0"}}}'
Set-Content -Path .\_smoke\ready-payload.json -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","method":"notifications/initialized"}'
Set-Content -Path .\_smoke\tools-payload.json -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
Set-Content -Path .\_smoke\health-payload.json -Encoding UTF8 -NoNewline -Value '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"health","arguments":{}}}'

curl.exe -sS -D .\_smoke\init-headers.txt -o .\_smoke\init-body.json -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" -X POST  --data-binary "@.\_smoke\init-payload.json"

C:\Users\matt\OneDrive - caberlink.com\GitHub\Custom-MCP-Connectors\servicedesk-mcp-next\runtime\_smoke\init-headers.txt:5:mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0 = Select-String -Path .\_smoke\init-headers.txt -Pattern "^mcp-session-id:\s*(.+)$" -CaseSensitive:False | Select-Object -First 1
if (-not C:\Users\matt\OneDrive - caberlink.com\GitHub\Custom-MCP-Connectors\servicedesk-mcp-next\runtime\_smoke\init-headers.txt:5:mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0) { throw "No mcp-session-id returned from initialize." }
55309e3d2aa2407eac1a2b0e5d109cf0 = C:\Users\matt\OneDrive - caberlink.com\GitHub\Custom-MCP-Connectors\servicedesk-mcp-next\runtime\_smoke\init-headers.txt:5:mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0.Matches[0].Groups[1].Value.Trim()

curl.exe -sS -o .\_smoke\ready-body.txt -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" -H "MCP-Protocol-Version: 2024-11-05" -H "mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0" -X POST  --data-binary "@.\_smoke\ready-payload.json"
curl.exe -sS -o .\_smoke\tools-body.json -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" -H "MCP-Protocol-Version: 2024-11-05" -H "mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0" -X POST  --data-binary "@.\_smoke\tools-payload.json"
curl.exe -sS -o .\_smoke\health-body.json -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" -H "MCP-Protocol-Version: 2024-11-05" -H "mcp-session-id: 55309e3d2aa2407eac1a2b0e5d109cf0" -X POST  --data-binary "@.\_smoke\health-payload.json"

Write-Host "===== init ====="
Get-Content .\_smoke\init-body.json
Write-Host ""
Write-Host "===== tools ====="
Get-Content .\_smoke\tools-body.json
Write-Host ""
Write-Host "===== health ====="
Get-Content .\_smoke\health-body.json
