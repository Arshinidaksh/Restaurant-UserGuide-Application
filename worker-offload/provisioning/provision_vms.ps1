<#
.SYNOPSIS
    Provisions screenshot-vm and image-stitcher-vm on DigitalOcean with SSH configured on Port 2222.
#>
param(
    [string]$Region = "blr1",
    [string]$Size = "s-4vcpu-8gb",
    [string]$Image = "ubuntu-22-04-x64"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Resolve-Path "$ScriptDir\.."

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  DigitalOcean VM Provisioning (Port 2222 SSH & Docker)  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check doctl
try {
    $account = doctl account get --format Email,Status --no-header
    Write-Host "[OK] doctl authenticated: $account" -ForegroundColor Green
} catch {
    Write-Error "doctl is not authenticated or not installed. Please run 'doctl auth init'."
    exit 1
}

# 2. Get SSH Key IDs
$sshKeyOutput = doctl compute ssh-key list --format ID --no-header
$sshKeys = ($sshKeyOutput -split "`r?`n" | Where-Object { $_ -match '^\d+$' }) -join ","
if (-not $sshKeys) {
    Write-Warning "No existing SSH keys found in doctl. VM will generate root password via email."
} else {
    Write-Host "[OK] Embedding SSH Keys: $sshKeys" -ForegroundColor Green
}

# 3. Cloud-Init file paths
$screenshotCloudInit = Resolve-Path "$BaseDir\cloud-init\screenshot-vm-cloud-init.sh"
$stitcherCloudInit = Resolve-Path "$BaseDir\cloud-init\image-stitcher-vm-cloud-init.sh"

Write-Host "`n[1/3] Provisioning 'screenshot-vm' ($Size in $Region)..." -ForegroundColor Yellow
$createArgs1 = @(
    "compute", "droplet", "create", "screenshot-vm",
    "--region", $Region,
    "--size", $Size,
    "--image", $Image,
    "--user-data-file", $screenshotCloudInit,
    "--tag-names", "worker-offload,screenshot-worker",
    "--wait"
)
if ($sshKeys) {
    $createArgs1 += @("--ssh-keys", $sshKeys)
}

& doctl @createArgs1

Write-Host "`n[2/3] Provisioning 'image-stitcher-vm' ($Size in $Region)..." -ForegroundColor Yellow
$createArgs2 = @(
    "compute", "droplet", "create", "image-stitcher-vm",
    "--region", $Region,
    "--size", $Size,
    "--image", $Image,
    "--user-data-file", $stitcherCloudInit,
    "--tag-names", "worker-offload,stitcher-worker",
    "--wait"
)
if ($sshKeys) {
    $createArgs2 += @("--ssh-keys", $sshKeys)
}

& doctl @createArgs2

# 4. Fetch droplet details
Write-Host "`n[3/3] Retrieving droplet IP addresses..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

$dropletsJson = doctl compute droplet list --tag-name "worker-offload" --format ID,Name,PublicIPv4,Status -o json | ConvertFrom-Json

$screenshotIp = ($dropletsJson | Where-Object { $_.name -eq "screenshot-vm" }).networks.v4 | Where-Object { $_.type -eq "public" } | Select-Object -ExpandProperty ip_address
$stitcherIp = ($dropletsJson | Where-Object { $_.name -eq "image-stitcher-vm" }).networks.v4 | Where-Object { $_.type -eq "public" } | Select-Object -ExpandProperty ip_address

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  VM PROVISIONING COMPLETE!                              " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  screenshot-vm:     IP: $screenshotIp" -ForegroundColor Cyan
Write-Host "  image-stitcher-vm: IP: $stitcherIp" -ForegroundColor Cyan
Write-Host ""
Write-Host "  SSH Access (Port 2222):" -ForegroundColor Yellow
Write-Host "    ssh -p 2222 root@$screenshotIp"
Write-Host "    ssh -p 2222 root@$stitcherIp"
Write-Host ""
Write-Host "  Worker HTTP Endpoints:" -ForegroundColor Yellow
Write-Host "    http://$screenshotIp`:8000/health"
Write-Host "    http://$stitcherIp`:8000/health"
Write-Host "==========================================================" -ForegroundColor Green

# 5. Update client/config.json
$clientConfigFile = "$BaseDir\client\config.json"
$configData = @{
    screenshot_worker_url = "http://$screenshotIp`:8000"
    stitcher_worker_url = "http://$stitcherIp`:8000"
    screenshot_concurrency = 10
    stitcher_concurrency = 16
    request_timeout_sec = 120
}
$configData | ConvertTo-Json -Depth 4 | Set-Content -Path $clientConfigFile -Encoding utf8
Write-Host "`n[OK] Updated client configuration at $clientConfigFile" -ForegroundColor Green
