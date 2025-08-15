#!/bin/bash

# Diretório base do deploy
DEPLOY_DIR="/home/deploy-debezium/kafka-druid-pipeline"

# Ir para o diretório do deploy
cd "$DEPLOY_DIR" || { echo "Diretório $DEPLOY_DIR não encontrado!"; exit 1; }

echo "==> Realizando git pull..."
GIT_SSH_COMMAND='ssh -i ~/.ssh/deploy_key -o IdentitiesOnly=yes' git fetch origin minimal-tdp && \
git reset --hard origin/minimal-tdp || { echo "Git pull falhou!"; exit 1; }

echo "==> Derrubando containers antigos..."
docker compose down --remove-orphans || { echo "Falha ao derrubar containers!"; exit 1; }

echo "==> Subindo containers atualizados..."
docker compose up -d || { echo "Falha ao subir containers!"; exit 1; }

echo "==> Containers atualizados com sucesso!"
echo "==> Logs recentes (Ctrl+C para sair):"
docker compose logs -f --tail=50