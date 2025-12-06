# Start all 8 REAL AI-powered software engineering agents
# Each agent runs on a separate port and uses OpenAI GPT-4 for intelligent responses

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting 8 REAL AI Software Agents" -ForegroundColor Cyan
Write-Host "Powered by OpenAI GPT-4" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kill any existing node processes to ensure clean start
Write-Host "Cleaning up existing node processes..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2

# Array of ports for each agent
$ports = @(12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008)

$agentNames = @{
    12001 = "code-debugging-assistant"
    12002 = "api-design-advisor"
    12003 = "backend-database-optimizer"
    12004 = "frontend-ux-refiner"
    12005 = "devops-ci-cd-orchestrator"
    12006 = "secure-code-auditor"
    12007 = "test-automation-engineer"
    12008 = "software-architecture-consultant"
}

# Start each agent in a new PowerShell window
foreach ($port in $ports) {
    $agentName = $agentNames[$port]
    Write-Host "Starting $agentName on port $port..." -ForegroundColor Green
    
    # Change to typescript directory and run ts-node
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; npx ts-node real_software_a2a_agent.ts $port"
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All 8 REAL AI agents started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agent Endpoints:" -ForegroundColor Yellow
foreach ($port in $ports) {
    $agentName = $agentNames[$port]
    Write-Host "  - http://localhost:$port - $agentName" -ForegroundColor White
}
Write-Host ""
Write-Host "Each agent uses OpenAI GPT-4 for intelligent responses!" -ForegroundColor Cyan
Write-Host "Close the individual PowerShell windows to stop agents." -ForegroundColor Yellow
Write-Host ""
