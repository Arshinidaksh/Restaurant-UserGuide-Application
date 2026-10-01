# Distributed Multi-Worker Slide Generation Architecture

This subsystem decouples and offloads the compute-intensive slide creation workflow into dedicated DigitalOcean cloud workers:
1. **`screenshot-vm`**: Headless browser automation (Playwright/Chromium in Docker) capturing pristine 1920x1080 screens.
2. **`image-stitcher-vm`**: High-performance image composition and resizing engine (FastAPI + Pillow in Docker) fitting screens into PC monitor hardware frames, rendering Rubik brand typography, badges, and exporting 1920x1080 slides.

---

## Network & Port 2222 Configuration

Because outbound traffic on default **TCP Port 22** is blocked by corporate firewalls and certain ISPs, the virtual machines are provisioned with SSH listening on **Port 2222** (alongside systemd socket overrides on Ubuntu 22.04 / 24.04 LTS).

### Connecting to the VMs via SSH:
```bash
# Connect to screenshot-vm
ssh -p 2222 root@<SCREENSHOT_VM_IP>

# Connect to image-stitcher-vm
ssh -p 2222 root@<STITCHER_VM_IP>
```

---

## Architecture Diagram

```
+---------------------------------------------------------------------------------+
|                               Local Orchestrator                                |
|                   (worker-offload/client/async_slide_generator.py)              |
|                                                                                 |
|  - Asynchronous pipeline with connection pooling (httpx)                        |
|  - Throttles concurrency based on worker capacities                             |
+-------------------+---------------------------------------+---------------------+
                    | (1) POST /capture                     | (2) POST /compose
                    v                                       v
+-------------------------------------+   +---------------------------------------+
|            screenshot-vm            |   |           image-stitcher-vm           |
|            (Port: 8000)             |   |             (Port: 8000)              |
|-------------------------------------|   |---------------------------------------|
|  - SSH Port: 2222                   |   |  - SSH Port: 2222                     |
|  - Docker Container: Playwright     |   |  - Docker Container: Pillow & Fonts   |
|  - Chromium Headless                |   |  - PC Hardware Mockup Stitcher        |
|  - Auto POS Activation & Login      |   |  - Brand Rubik Typography Layout      |
|  - Pristine 1920x1080 Screens       |   |  - Resizing & Multi-Variant Generator |
|  - Concurrency Capacity: 4          |   |  - Concurrency Capacity: 8            |
+-------------------------------------+   +---------------------------------------+
```

---

## Directory Structure

```
worker-offload/
├── cloud-init/
│   ├── screenshot-vm-cloud-init.sh       # Cloud-init: Port 2222, Docker, screenshot-worker
│   └── image-stitcher-vm-cloud-init.sh   # Cloud-init: Port 2222, Docker, stitcher-worker
├── screenshot-worker/                    # Microservice for screenshot capture
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py                         # FastAPI + Playwright with concurrency control
│   └── docker-compose.yml
├── stitcher-worker/                      # Microservice for slide stitching & resizing
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py                         # FastAPI + Pillow with ThreadPool execution
│   ├── src/
│   │   ├── composer.py                   # PC Mockup fitting, badges, text wrapping
│   │   └── config.py                     # 1920x1080 coordinates & brand color tokens
│   ├── assets/                           # PC-Screen mockup, background canvas, Rubik fonts
│   └── docker-compose.yml
├── provisioning/
│   ├── provision_vms.ps1                 # Automated doctl provisioning script
│   ├── verify_workers.ps1                # Tests Port 2222 and HTTP health endpoints
│   └── teardown_vms.ps1                  # Destroys droplets when finished
├── client/
│   ├── async_slide_generator.py          # Asynchronous pipeline dispatcher
│   ├── config.py                         # Loads worker endpoints & concurrency limits
│   └── config.json                       # Droplet IPs and active configuration
└── README.md
```

---

## Quickstart

### 1. Provision VMs via `doctl`
Run the automated PowerShell provisioning script:
```powershell
cd worker-offload\provisioning
.\provision_vms.ps1
```
This script will:
1. Verify `doctl` authentication and attach your DigitalOcean SSH keys.
2. Spin up `screenshot-vm` and `image-stitcher-vm` in region `blr1` with 4GB RAM (`s-2vcpu-4gb`).
3. Apply cloud-init scripts to configure **SSH on Port 2222**, install Docker, and launch the workers.
4. Automatically update `worker-offload\client\config.json` with the assigned public IPs.

### 2. Verify Connectivity
Run the health verification script:
```powershell
.\verify_workers.ps1
```
Tests TCP connection to **Port 2222** and polls the `/health` endpoints of both Docker containers.

### 3. Run Asynchronous Multi-Slide Generation
Generate an entire presentation part in parallel:
```powershell
# Using uv (fast Python runner):
uv run --with httpx worker-offload\client\async_slide_generator.py --spec specs\part_l_spec.json

# Or for Part M:
uv run --with httpx worker-offload\client\async_slide_generator.py --spec specs\part_m_spec.json
```

### 4. Tear Down Droplets
When generation work is complete and you want to stop incurring charges:
```powershell
.\teardown_vms.ps1
```
