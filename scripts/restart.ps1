$port = 8000
Write-Host "Restarting NextGen MCP server on port $port..." -ForegroundColor Cyan

# Find and kill the process using the port
$connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connection) {
    foreach ($conn in $connection) {
        $procId = $conn.OwningProcess
        if ($procId -gt 0) {
            Write-Host "Stopping process $procId..." -ForegroundColor Yellow
            Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 1
}

# Set transport and run
$env:MCP_TRANSPORT="sse"
uv run nextgen-mcp
