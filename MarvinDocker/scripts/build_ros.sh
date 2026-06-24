#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)/ros2_ws"
if [ -d /ros2_ws/src ]; then
    DEFAULT_WORKSPACE_DIR="/ros2_ws"
fi
WORKSPACE_DIR="${WORKSPACE_DIR:-${DEFAULT_WORKSPACE_DIR}}"

echo "==> Enter workspace: ${WORKSPACE_DIR}"
cd "${WORKSPACE_DIR}"
for dir in "${WORKSPACE_DIR}/build" "${WORKSPACE_DIR}/log" "${WORKSPACE_DIR}/install"; do
    mkdir -p "${dir}"
    find "${dir}" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
done

echo "==> Source ROS Humble"
source /opt/ros/humble/setup.bash

if [ -f "${WORKSPACE_DIR}/install/setup.bash" ]; then
    echo "==> Source existing workspace install/setup.bash"
    source "${WORKSPACE_DIR}/install/setup.bash"
fi

echo "==> Step 1: build marvin_msgs"
colcon build  --packages-select marvin_msgs fake_interface_pkg
colcon build  --packages-select marvin_description dm_gripper_py
if [ "${SKIP_ROSDEP:-0}" = "1" ]; then
    echo "==> Step 2: skip rosdep (SKIP_ROSDEP=1)"
else
    echo "==> Step 2: install dependencies with rosdep"
    rosdep install --from-paths src --ignore-src -r -y
fi

echo "==> Step 3: build marvin_ros_control with CPU_ARCH=x86"
colcon build  --packages-select marvin_ros_control --cmake-args -DCPU_ARCH=x86

echo "==> Step 4: build marvin_fabric with CPU_ARCH=x86"
colcon build  --packages-select marvin_fabric --cmake-args -DCPU_ARCH=x86

echo "==> All steps completed successfully."
