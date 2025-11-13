#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# --- O ALVO ---
# Cortex-A53 é ARM 64-bit (AArch64). No Docker, é 'linux/arm64'.
ARCH="aarch64"
PLATFORM="linux/arm64"
OUTPUT_NAME="kanban-$ARCH"

echo ">>> Construindo para arquitetura: $ARCH (plataforma $PLATFORM)"

# --- A MÁGICA (BUILDX) ---
# O comando é IDÊNTICO, só mudamos a plataforma
docker buildx build \
  --platform "$PLATFORM" \
  -f Dockerfile.pyinstaller \
  --output "type=local,dest=./dist-temp" \
  .

echo ">>> Build concluído! O binário está em: ./dist-temp/usr/local/bin/kanban"

# --- Limpeza e Fuga ---
mkdir -p dist
mv "./dist-temp/usr/local/bin/kanban" "./dist/$OUTPUT_NAME"
rm -rf ./dist-temp

echo ">>> Binário 'Cortex-A53' pronto gerado em: dist/$OUTPUT_NAME"