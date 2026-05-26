#!/usr/bin/env bash
set -e

IMAGE_NAME="mindbridge"

sudo docker build -t "$IMAGE_NAME" .


sudo docker run --rm -it \
  --name mindbridge \
  --gpus all \
  --network host \
  -v "$(pwd):/workspace" \
  "$IMAGE_NAME"
