# customize_chat_server

## 使用技術

- Python 3.9
- FastAPI 0.68.0
- Uvicorn 0.15.0

## セットアップ方法

プロジェクトのセットアップには、以下の手順を実行してください。

1. リポジトリをクローンします。

   ```bash
   git clone git@github.com:task-0112/customize_chat_server.git
   ```

1. dockerを立ち上げます。

   ```bash
   docker compose up --build
   ```

1. 必要な Python パッケージをインストールします。

   ```bash
   poetry install
   ```


これらの手順に従ってセットアップを完了させると、サーバーが起動し、 <http://localhost:8001> でアクセスできます。

