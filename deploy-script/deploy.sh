#!/bin/bash
set -e

APP_DIR=/home/ubuntu/ml-app

apt-get update -y
apt-get install -y python3-venv python3-pip

if [ ! -d /opt/ml-venv ]; then
    python3 -m venv /opt/ml-venv
fi

cd "$APP_DIR"
/opt/ml-venv/bin/pip install --no-cache-dir -r requirements.txt
/opt/ml-venv/bin/python train.py

cat > /etc/systemd/system/ml-app.service <<'SERVICE'
[Unit]
Description=Student Result Predictor
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/ml-app
Environment=MODEL_Version=1.0
ExecStart=/opt/ml-venv/bin/gunicorn --bind 0.0.0.0:80 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable ml-app
systemctl restart ml-app

echo "Student Result Predictor deployed!"
