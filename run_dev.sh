#!/usr/bin/env bash
set -e

# vai pra pasta onde está o script
cd "$(dirname "$0")"

echo ">>> Criando venv (.venv) se não existir..."
if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

echo ">>> Ativando venv..."
source .venv/bin/activate

echo ">>> Instalando/atualizando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> Subindo app Flask em http://127.0.0.1:5000 ..."
python app.py
