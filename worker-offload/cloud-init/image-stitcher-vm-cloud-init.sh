#!/bin/bash
set -e

exec >> /var/log/worker-setup.log 2>&1
echo "=== Starting image-stitcher-vm Cloud-Init Setup at $(date) ==="

# 1. Configure SSH to listen on Port 2222 (and fallback 22)
echo "[1/5] Configuring SSH on Port 2222..."
mkdir -p /etc/ssh/sshd_config.d
cat << 'EOF' > /etc/ssh/sshd_config.d/custom-port.conf
Port 2222
Port 22
EOF

sed -i -e 's/#*Port 22/Port 2222\nPort 22/' /etc/ssh/sshd_config || true

# Systemd socket override for Ubuntu 22.10 / 24.04 LTS
mkdir -p /etc/systemd/system/ssh.socket.d
cat << 'EOF' > /etc/systemd/system/ssh.socket.d/listen.conf
[Socket]
ListenStream=
ListenStream=2222
ListenStream=22
EOF

systemctl daemon-reload
systemctl restart ssh.socket || true
systemctl restart ssh || systemctl restart sshd || true

# 2. Configure Firewall (UFW)
echo "[2/5] Configuring Firewall for port 2222 and 8000..."
if command -v ufw >/dev/null 2>&1; then
    ufw allow 2222/tcp
    ufw allow 22/tcp
    ufw allow 8000/tcp
    ufw allow 80/tcp
    ufw --force enable || true
fi

# 3. Install Docker & Docker Compose
echo "[3/5] Installing Docker engine..."
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker

# 4. Clone repository
echo "[4/5] Fetching application code..."
mkdir -p /opt/app
if [ ! -d "/opt/app/.git" ]; then
    git clone https://github.com/Arshinidaksh/Restaurant-UserGuide-Application.git /opt/app
else
    cd /opt/app && git pull origin main || true
fi

# 5. Build and launch stitcher-worker container
echo "[5/5] Launching stitcher-worker Docker container..."
cd /opt/app/worker-offload/stitcher-worker
docker compose up -d --build

echo "=== image-stitcher-vm setup successfully completed at $(date) ==="
