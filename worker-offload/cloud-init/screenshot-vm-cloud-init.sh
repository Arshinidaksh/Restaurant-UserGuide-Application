#!/bin/bash
set -e

exec >> /var/log/worker-setup.log 2>&1
echo "=== Starting screenshot-vm Cloud-Init Setup at $(date) ==="

# 1. Configure SSH to listen on Port 2222
echo "[1/4] Configuring SSH on Port 2222..."
if systemctl list-unit-files | grep -q "ssh.socket"; then
    systemctl stop ssh.socket || true
    systemctl disable --now ssh.socket || true
fi

sed -i -e 's/^#*Port [0-9]*/Port 2222/' /etc/ssh/sshd_config
mkdir -p /etc/ssh/sshd_config.d
cat << 'EOF' > /etc/ssh/sshd_config.d/port.conf
Port 2222
EOF

systemctl daemon-reload
systemctl unmask ssh || true
systemctl unmask sshd || true
systemctl enable --now ssh || systemctl enable --now sshd || true
systemctl restart ssh || systemctl restart sshd || true

# 2. Install Docker & Docker Compose
echo "[2/4] Installing Docker engine..."
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker

# 3. Clone repository
echo "[3/4] Fetching application code..."
mkdir -p /opt/app
if [ ! -d "/opt/app/.git" ]; then
    git clone https://github.com/Arshinidaksh/Restaurant-UserGuide-Application.git /opt/app
else
    cd /opt/app && git pull origin main || true
fi

# 4. Build and launch screenshot-worker container
echo "[4/4] Launching screenshot-worker Docker container..."
cd /opt/app/worker-offload/screenshot-worker
docker compose up -d --build

echo "=== screenshot-vm setup successfully completed at $(date) ==="
