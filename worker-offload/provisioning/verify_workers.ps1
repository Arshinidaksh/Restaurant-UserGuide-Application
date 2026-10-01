<#
.SYNOPSIS
    Tests SSH connectivity on Port 2222 and verifies HTTP health of the worker containers.
#>
param(
    [int]$TimeoutSeconds = 180
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Resolve-Path "$ScriptDir\.."
$clientConfigFile = "$BaseDir\client\config.json"

if (-not (Test-Path $clientConfigFile)) {
    Write-Error "Config file not found: $clientConfigFile. Please run provision_vms.ps1 first."
    exit 1
}

$cfg = Get-Content -Raw $clientConfigFile | ConvertFrom-Json
$screenshotUrl = $cfg.screenshot_worker_url
$stitcherUrl = $cfg.stitcher_worker_url

$screenshotHost = ([uri]$screenshotUrl).Host
$stitcherHost = ([uri]$stitcherUrl).Host

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Verifying SSH (Port 2222) and Docker Worker Endpoints   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Test SSH Port 2222
Write-Host "`n[1/2] Testing TCP Port 2222 (Bypassing Port 22)..." -ForegroundColor Yellow

$t1 = Test-NetConnection -ComputerName $screenshotHost -Port 2222 -InformationLevel Quiet
if ($t1) {
    Write-Host "  [OK] screenshot-vm ($screenshotHost) listening on PORT 2222" -ForegroundColor Green
} else {
    Write-Host "  [WAIT] screenshot-vm ($screenshotHost) not reachable on PORT 2222 yet." -ForegroundColor Red
}

$t2 = Test-NetConnection -ComputerName $stitcherHost -Port 2222 -InformationLevel Quiet
if ($t2) {
    Write-Host "  [OK] image-stitcher-vm ($stitcherHost) listening on PORT 2222" -ForegroundColor Green
} else {
    Write-Host "  [WAIT] image-stitcher-vm ($stitcherHost) not reachable on PORT 2222 yet." -ForegroundColor Red
}

# 2. Poll HTTP healthcheck endpoints
Write-Host "`n[2/2] Polling HTTP Health Endpoints (waiting for Docker containers to boot)..." -ForegroundColor Yellow

function Wait-Endpoint {
    param([string]$name, [string]$url, [int]$maxWait)
    $healthUrl = "$url/health"
    $elapsed = 0
    while ($elapsed -lt $maxWait) {
        try {
            $resp = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 5 -ErrorAction Stop
            Write-Host "  [ONLINE] $name ($healthUrl) responded: $($resp | ConvertTo-Json -Compress)" -ForegroundColor Green
            return $true
        } catch {
            Write-Host "  ... waiting for $name to be ready ($elapsed/$maxWait s)" -ForegroundColor Gray
            Start-Sleep -Seconds 10
            $elapsed += 10
        }
    }
    Write-Host "  [TIMEOUT] $name was not ready within $maxWait seconds." -ForegroundColor Red
    return $false
}

$ok1 = Wait-Endpoint -name "screenshot-worker" -url $screenshotUrl -maxWait $TimeoutSeconds
$ok2 = Wait-Endpoint -name "stitcher-worker" -url $stitcherUrl -maxWait $TimeoutSeconds

if ($ok1 -and $ok2) {
    Write-Host "`n[SUCCESS] Both workers are fully operational and ready for parallel job dispatch!" -ForegroundColor Green
} else {
    Write-Host "`n[NOTICE] One or more workers are still initializing. Cloud-init typically takes 1-2 minutes on first boot." -ForegroundColor Yellow
}
