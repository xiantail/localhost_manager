# Python Backend Development Guide

## 仮想環境のセットアップと使用方法

### 1. 仮想環境の作成（初回のみ）
```bash
python3 -m venv .venv
```

### 2. 仮想環境のアクティベート
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
```bash
# .env.exampleから.envをコピー
cp .env.example .env
# .envファイルを編集して実際の設定値を入力
```

### 5. サーバーの起動
```bash
# 手動起動
uvicorn main:app --reload --host localhost --port 9000

# スクリプトを使用（推奨）
./start.sh

# 初回起動時（依存関係も同時インストール）
./start.sh --install
```

### 6. 仮想環境の非アクティベート
```bash
deactivate
```

## 開発のワークフロー

1. `source .venv/bin/activate` で仮想環境をアクティベート
2. 必要に応じて `pip install package_name` で新しいパッケージを追加
3. `pip freeze > requirements.txt` で依存関係を更新
4. `./start.sh` でサーバーを起動
5. 開発作業
6. `deactivate` で仮想環境を終了

## パッケージ管理

### パッケージの追加
```bash
pip install package_name
pip freeze > requirements.txt
```

### パッケージのアップグレード
```bash
pip install --upgrade package_name
pip freeze > requirements.txt
```