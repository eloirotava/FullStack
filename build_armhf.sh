#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# --- O ALVO ---
# 'armhf' (ARM 32-bit hard float) é chamado de 'linux/arm/v7' no Docker.
ARCH="armhf"
PLATFORM="linux/arm/v7"
OUTPUT_NAME="kanban-$ARCH"

echo ">>> Construindo para arquitetura: $ARCH (plataforma $PLATFORM)"

# --- A MÁGICA (BUILDX) ---
# 1. 'buildx build': O comando de cross-compile
# 2. '--platform': "Finja" ser um Linux ARM 32-bit (QEMU faz a mágica)
# 3. '--output': A "fuga" (extrai o binário sem o 'docker cp')
# 4. '-f': O seu Dockerfile (que está perfeito)
# 5. '.': O diretório atual

docker buildx build \
  --platform "$PLATFORM" \
  -f Dockerfile.pyinstaller \
  --output "type=local,dest=./dist-temp" \
  .

echo ">>> Build concluído! O binário está em: ./dist-temp/usr/local/bin/kanban"

# --- Limpeza e Fuga ---
# Move o binário para o lugar certo e limpa o lixo
mkdir -p dist
mv "./dist-temp/usr/local/bin/kanban" "./dist/$OUTPUT_NAME"
rm -rf ./dist-temp

echo ">>> Binário 'pilantra' gerado com sucesso em: dist/$OUTPUT_NAME"
echo ">>> Pronto para entregar na TV Box S805 e sumir!"