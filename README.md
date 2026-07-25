![Backend CI](https://github.com/Iris408/log-intelligence-analyzer/actions/workflows/backend-ci.yml/badge.svg)
![Docker CI](https://github.com/Iris408/inventory-management-system/actions/workflows/docker-ci.yml/badge.svg)

# Log Intelligence Analyzer / ログインテリジェンスアナライザー

Python-based log analysis and monitoring tool designed to parse, analyse, and report operational server logs through a modular backend architecture.

Pythonベースのログ解析・監視ツール。サーバーログの分析、エラー追跡、レポート生成を行うバックエンドプロジェクト。

## Current Status / 現在のステータス

Log Intelligence Analyzer is a FastAPI backend project for importing, storing, analysing, and reporting application logs.

### Completed
- FastAPI backend routes
- PostgreSQL log storage
- Docker support
- Docker Compose setup
- Log import route
- Stored logs route
- Error summary/report routes

### Known Issue
Running `/logs/import` multiple times can create duplicate stored log entries.

### Next Roadmap
- Add duplicate prevention for imported logs
- Add log hash/checksum field
- Add severity filtering
- Add Slack/email alerts for critical logs
- Expand FastAPI dashboard
- Move detailed documentation into the `docs/` directory

## Features / 機能
| EN | 日本語 |
| --- | --- |
| Log severity categorisation | ログの重要度分類 |
| INFO / WARNING / ERROR | INFO / WARNING / ERROR の検出 |
| Repeated error tracking | 重複エラーの追跡 |
| Error frequency analysis | エラー発生頻度の分析 |
| Timestamp/hour-based error analysis | タイムスタンプ・時間帯別のエラー分析 |
| Exportable analysis reports | エクスポート可能な分析レポート |
| Color-coded CLI output | 色分けされたCLI出力 |
| Modular backend structure | モジュール化されたバックエンド構成 |
| FastAPI dashboard/API layer | FastAPIダッシュボード・APIレイヤー |
| Swagger API documentation | Swagger APIドキュメント |
| PostgreSQL log storage | PostgreSQLへのログ保存 |
| Docker containerization | Dockerコンテナ |
| Docker Compose API + PostgreSQL setup | Docker Compose APIとPostgreSQL構成 |
| Live log preview route | 最新ログを確認するライブプレビュールート |

## Tech Stack / 技術スタック

- Python
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Docker | Docker Compose
- Colorama
- Git | GitHub
- Linux/macOS terminal
- Modular Backend Architecture

## Docker Usage / Dockerでの起動
### Docker Compose

Start the FastAPI backend and Postgresql database:
```bash
docker compose up --build
```
Run in the background:
```bash
docker compose up -d
```
View container logs:
```bash
docker compose logs
```
Stop the container:
```bash
docker compose down
```

## Manual Docker Usage / 手動Docker起動
Build the API container:
```bash
docker build -t log-intelligence-api .
```

Run the API container:
```bash
docker run -p 8000:8000 log-intelligence-api
```

Open FastAPI Swagger docs:
```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | API health/status route |
| GET | /logs/summary | Returns log severity summary |
| GET | /logs/errors | Returns error log entries |
| GET | /logs/report | Returns generated analysis report |
| POST | /logs/import | Imports log entries into PostgreSQL |
| GET | /logs/stored | Returns stored log entries from PostgreSQL |
| GET | /logs/live | Returns the latest log entries from the log file |
| DELETE | /logs/stored | Clears stored log entries from PostgreSQL |

## API Examples / API使用例

Import logs:
```bash
curl -X POST http://127.0.0.1:8000/logs/import
```

View stored logs:
```bash
curl http://127.0.0.1:8000/logs/stored
```

View severity summary

## CI/CD

This project uses GitHub Actions to run automated checks on every push and pull request.

Current pipeline:

- Install dependencies
- Validate Python syntax
- Run tests when available
- Build project or Docker image where applicable

## Project Structure / プロジェクト構成
```markdown
log-intelligence-analyzer/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── log_model.py
│   ├── routes/
│   │   └── log_routes.py
│   └── services/
│       └── log_service.py
├── analysis_report.txt
├── analytics.py
├── analyzer.py
├── Dockerfile
├── docker-compose.yml
├── parser.py
├── README.md
├── reporter.py
├── requirements.txt
└── sample_logs/
    └── server.log
```

## Documentation

Detailed project documentation is available in the [`docs/`](docs/) directory.

| Document | Description |
|----------|-------------|
| [API Examples](docs/api-examples.md) | Example requests and responses for each API endpoint. |
| Architecture | *(Coming soon)* |
| Development Notes | *(Coming soon)* |

## Future Improvements / 今後の改善点

| EN | 日本語 |
| --- | --- | 
| Background live log monitioring | バックグラウンドでのライブログ監視 |
| Slack/email alert integration | Slack・メール通知連携 |
| Duplicate log prevention | 重複ログ登録の防止 |
| Log search and filtering | ログ検索・フィルタリング |
| Dashboard UI improvements | ダッシュボードUIの改善 |
| Historical log charts | 過去ログのグラフ表示 |
| CI/CD pipeline | CI/CDパイプライン |
| Deployment documentation | デプロイ手順のドキュメント化 |
