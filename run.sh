#!/usr/bin/env bash
set -euo pipefail

NAME="${FUSION_CONTAINER_NAME:-TJfusion}"
IMAGE="${FUSION_IMAGE:-tjfusion:latest}"
PORT="${1:-8765}"
URL="http://127.0.0.1:${PORT}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER=(docker)

if ! docker ps >/dev/null 2>&1; then
  if sudo docker ps >/dev/null 2>&1; then
    DOCKER=(sudo docker)
  else
    echo "Docker is not accessible. Start Docker or run with a user that can access Docker."
    exit 1
  fi
fi

echo "==> Allow Docker root user to connect to X11..."
xhost +local:root 2>/dev/null || true

if ! "${DOCKER[@]}" ps --format '{{.Names}}' | grep -qx "$NAME"; then
  if "${DOCKER[@]}" ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
    echo "==> Starting existing ${NAME} container..."
    "${DOCKER[@]}" start "$NAME" >/dev/null
  else
    echo "==> Creating ${NAME} container..."
	    "${DOCKER[@]}" run -d --name "$NAME" \
	      --gpus all \
	      --network host \
	      --privileged \
	      -e DISPLAY="${DISPLAY:-}" \
	      -e HOST_WORKSPACE_ROOT="$ROOT_DIR" \
	      -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	      -v /var/run/docker.sock:/var/run/docker.sock \
	      -v /usr/bin/docker:/usr/bin/docker:ro \
	      -v "$ROOT_DIR:/workspace" \
	      -v /dev:/dev \
      -v /run/udev:/run/udev:ro \
      -w /workspace \
      "$IMAGE" \
      tail -f /dev/null >/dev/null
  fi
fi

if ! "${DOCKER[@]}" exec "$NAME" bash -lc 'test -S /var/run/docker.sock && command -v docker >/dev/null && test -n "${HOST_WORKSPACE_ROOT:-}"' >/dev/null 2>&1; then
  echo "==> Warning: ${NAME} was created before MarvinDocker web control support."
  echo "==> Recreate it once to enable the Fusion UI Marvin buttons:"
  echo "    docker rm -f ${NAME}"
  echo "    ./run.sh ${PORT}"
fi

if "${DOCKER[@]}" exec "$NAME" bash -lc "python - <<PY
import socket
s = socket.socket()
try:
    s.settimeout(0.3)
    s.connect(('127.0.0.1', ${PORT}))
    print('open')
except OSError:
    print('closed')
finally:
    s.close()
PY" | grep -qx open; then
  if "${DOCKER[@]}" exec "$NAME" bash -lc "pgrep -af 'python -m mindbridge.src.fusion serve-ui.*--ui-port ${PORT}' >/dev/null"; then
    echo "==> Fusion UI already running in ${NAME}: ${URL}"
  else
    echo "==> Port ${PORT} is already open, but not by Fusion UI in ${NAME}."
    echo "==> Stop the old UI/container using this port or run: ./run.sh <another-port>"
    exit 1
  fi
else
  echo "==> Starting Fusion UI in Docker conda env: flowpose"
  "${DOCKER[@]}" exec -d "$NAME" bash -lc "
    cd /workspace
    mkdir -p logs
    source \$(conda info --base)/etc/profile.d/conda.sh
    conda activate flowpose
    exec python -m mindbridge.src.fusion serve-ui \
      --ui-host 0.0.0.0 \
      --ui-port ${PORT} \
      --control \
      > logs/fusion-ui.log 2>&1
  "
fi

sleep 1

echo "==> Opening ${URL}"
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 || echo "Open manually: ${URL}"
else
  echo "Open manually: ${URL}"
fi
