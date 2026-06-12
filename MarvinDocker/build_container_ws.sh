#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="${ROOT_DIR}/ros2_ws"

mkdir -p "${WS}/src" "${WS}/build" "${WS}/install" "${WS}/log"

docker run --rm \
  -v "${WS}":/host_ws \
  marvinfabric:latest \
  bash -lc "chown -R $(id -u):$(id -g) /host_ws/build /host_ws/install /host_ws/log || true"

docker run --rm \
  --network host \
  --privileged \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -v "${WS}/src":/ros2_ws/src \
  -v "${WS}/build":/ros2_ws/build \
  -v "${WS}/install":/ros2_ws/install \
  -v "${WS}/log":/ros2_ws/log \
  -v "${ROOT_DIR}/scripts":/scripts \
  -w /ros2_ws \
  marvinfabric:latest \
  bash -lc 'source /opt/ros/humble/setup.bash && SKIP_ROSDEP=1 WORKSPACE_DIR=/ros2_ws bash /scripts/build_ros.sh'

echo "[OK] Container-compatible workspace built into host directories:"
echo "  ${WS}/build"
echo "  ${WS}/install"
echo "  ${WS}/log"
