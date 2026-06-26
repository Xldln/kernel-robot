#!/bin/bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IP="${1:-192.168.12.190}"
MODE="${2:-all}"
ATTACH=1
if [ "${3:-}" = "--no-attach" ] || [ "${ATTACH:-}" = "0" ]; then
  ATTACH=0
fi

if [ -n "${MARVIN_HOST_ROOT_DIR:-}" ]; then
  DOCKER_ROOT_DIR="${MARVIN_HOST_ROOT_DIR}"
elif [ -n "${HOST_WORKSPACE_ROOT:-}" ]; then
  DOCKER_ROOT_DIR="${HOST_WORKSPACE_ROOT}/MarvinDocker"
else
  DOCKER_ROOT_DIR="${ROOT_DIR}"
fi

if [ ! -f "${ROOT_DIR}/ros2_ws/install/setup.bash" ]; then
  echo "[ERROR] Host ROS workspace is not built yet:"
  echo "  ${ROOT_DIR}/ros2_ws/install/setup.bash"
  echo ""
  echo "Build it on the host first:"
  echo "  cd ${ROOT_DIR}"
  echo "  ./build_container_ws.sh"
  exit 1
fi

mkdir -p "${ROOT_DIR}/ros2_ws/log/runtime"

if docker ps --format '{{.Names}}' | grep -qx marvin_dev; then
  if [ "${MODE}" = "base" ] || [ "${MODE}" = "action" ] || [ "${MODE}" = "run" ]; then
    if [ "${ATTACH}" = "0" ]; then
      echo "[INFO] marvin_dev is already running; executing ${MODE} (background)."
      docker exec -d marvin_dev bash -lc "/scripts/StartAll.sh '${IP}' '${MODE}' --no-attach"
      exit 0
    fi
    echo "[INFO] marvin_dev is already running; restarting ${MODE} and attaching..."
    docker exec -d marvin_dev bash -lc "/scripts/StartAll.sh '${IP}' 'base' --no-attach"
    sleep 3
    exec docker exec -it marvin_dev bash -lc 'tmux attach -t marvin || bash'
  fi
  # MODE=all (default): attach to existing session, or restart base if tmux is dead
  if docker exec marvin_dev tmux has-session -t marvin 2>/dev/null; then
    echo "[INFO] marvin_dev is already running; attaching to tmux session."
    exec docker exec -it marvin_dev bash -lc 'tmux attach -t marvin || bash'
  fi
  echo "[INFO] marvin_dev running but no tmux session; restarting base..."
  docker exec -d marvin_dev bash -lc "/scripts/StartAll.sh '${IP}' 'base' --no-attach"
  sleep 3
  exec docker exec -it marvin_dev bash -lc 'tmux attach -t marvin || bash'
fi

if [ "${MODE}" = "action" ] || [ "${MODE}" = "run" ]; then
  echo "[ERROR] marvin_dev is not running. Start Marvin base first."
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -qx marvin_dev; then
  echo "[INFO] Removing stopped marvin_dev container."
  docker rm marvin_dev >/dev/null
fi

# 允许容器访问本机 X11（只对本次会话生效）
xhost +local:docker >/dev/null 2>&1 || true

DOCKER_RUN_ARGS=(
  --network host \
  --privileged \
  -e DISPLAY="${DISPLAY:-}" \
  -e ROS_DOMAIN_ID=13 \
  -e ROS_LOG_DIR=/ros2_ws/log/runtime \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e QT_X11_NO_MITSHM=1 \
  -e TERM=xterm-256color \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "${DOCKER_ROOT_DIR}/ros2_ws/src":/ros2_ws/src \
  -v "${DOCKER_ROOT_DIR}/ros2_ws/build":/ros2_ws/build \
  -v "${DOCKER_ROOT_DIR}/ros2_ws/install":/ros2_ws/install \
  -v "${DOCKER_ROOT_DIR}/ros2_ws/log":/ros2_ws/log \
  -v "${DOCKER_ROOT_DIR}/scripts":/scripts \
  -v "${DOCKER_ROOT_DIR}/robotaction":/robotaction \
  -w /ros2_ws \
  --name marvin_dev \
)

CONTAINER_CMD='
cat > /root/.tmux.conf <<EOF
set -g mouse on
set -g history-limit 100000
setw -g mode-keys vi
EOF
cat >> ~/.bashrc <<'"'"'EOF'"'"'
[ -f /opt/ros/humble/setup.bash ] && source /opt/ros/humble/setup.bash
[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash
EOF
/scripts/StartAll.sh '"${IP}"' '"${MODE}"' '"$([ "${ATTACH}" = "0" ] && printf %s "--no-attach")"'
if [ '"${ATTACH}"' = "0" ]; then
  tail -f /dev/null
fi
'

if [ "${ATTACH}" = "0" ]; then
  docker run -d "${DOCKER_RUN_ARGS[@]}" marvinfabric:latest bash -lc "${CONTAINER_CMD}" >/dev/null
else
  docker run -it "${DOCKER_RUN_ARGS[@]}" marvinfabric:latest bash -lc "${CONTAINER_CMD}"
fi
