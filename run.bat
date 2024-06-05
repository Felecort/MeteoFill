
python pre_launch.py
start "Docker" C:\"Program Files"\Docker\Docker\"Docker Desktop.exe"

% echo off
timeout 5
docker compose up --build

pause