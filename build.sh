#!/usr/bin/env bash
set -e

IMAGE_NAME="mindbridge"
CMD_PATH="$HOME/.local/bin/mindbridge"

echo "==> 1. 构建镜像: $IMAGE_NAME"
sudo docker build -t "$IMAGE_NAME" .

echo "==> 2. 安装 mindbridge 命令 -> $CMD_PATH"
mkdir -p "$HOME/.local/bin"

cat > "$CMD_PATH" <<'SCRIPT'
#!/usr/bin/env bash
NAME="mindbridge"
if ! docker ps --format '{{.Names}}' | grep -qx "$NAME"; then
  echo "==> 允许 X11 连接..."
  xhost +local: 2>/dev/null || true
  echo "==> 启动容器..."
    docker run -d --name mindbridge \
     --gpus all \
     --network host \
     --privileged \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
     -v "$(pwd):/workspace" \
     -v /dev:/dev \
     -v /run/udev:/run/udev:ro \
     -w /workspace \
     mindbridge \
     tail -f /dev/null
fi
exec docker exec -it "$NAME" bash
SCRIPT

chmod +x "$CMD_PATH"

echo "==> 3. 验证 PATH"
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  echo "已添加 ~/.local/bin 到 PATH，请执行: source ~/.bashrc"
fi

echo "==> build mindbridge docker successfully! You can now run 'mindbridge' command to start the container and access the workspace."
