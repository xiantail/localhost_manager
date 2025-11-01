#!/bin/bash

# 仮想環境をアクティベート
source .venv/bin/activate

# 環境変数ファイルが存在するか確認
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env file created. Please edit it with your actual configuration."
    fi
fi

# 依存関係をインストール（必要な場合）
if [ "$1" = "--install" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# サーバーを起動
echo "Starting FastAPI server..."
uvicorn main:app --reload --host ${HOST:-localhost} --port ${PORT:-9000}