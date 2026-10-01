<#
.SYNOPSIS
    Deletes screenshot-vm and image-stitcher-vm droplets from DigitalOcean.
#>
param(
    [switch]$Force = $true
)

Write-Host "Tearing down screenshot-vm and image-stitcher-vm droplets..." -ForegroundColor Yellow
$droplets = doctl compute droplet list --tag-name "worker-offload" --format ID,Name --no-header

if (-not $droplets) {
    Write-Host "No active droplets found with tag 'worker-offload'." -ForegroundColor Cyan
    exit 0
}

Write-Host "Found droplets:"
$droplets | ForEach-Object { Write-Host " - $_" }

if ($Force) {
    doctl compute droplet delete screenshot-vm image-stitcher-vm --force
    Write-Host "[OK] Droplets deleted successfully." -ForegroundColor Green
} else {
    Write-Host "Rerun with -Force to confirm deletion."
}
