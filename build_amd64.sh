#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

ARCH="amd64"
IMAGE_NAME="kanban-pyinstaller-amd64"

echo ">>> Construindo imagem para arquitetura: $ARCH (linux/amd64)"

docker build \
  -f Dockerfile.pyinstaller \
  -t "$IMAGE_NAME" \
  .

echo ">>> Extraindo binário do container..."

CID="$(docker create "$IMAGE_NAME")"
mkdir -p dist
docker cp "$CID":/usr/local/bin/kanban "dist/kanban-$ARCH"
docker rm "$CID" >/dev/null

echo ">>> Binário gerado em: dist/kanban-$ARCH"
echo ">>> Para rodar localmente (no host compatível):"
echo "    ./dist/kanban-$ARCH"
