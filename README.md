![Backend CI](https://github.com/Iris408/logsense/actions/workflows/backend-ci.yml/badge.svg)
![Docker CI](https://github.com/Iris408/logsense/actions/workflows/docker-ci.yml/badge.svg)

# LogSense / ログセンス

Python-based log intelligence and analysis tool for importing, storing, analysing, and reporting operational application logs through a modular FastAPI backend.

アプリケーションログの取り込み、保存、分析、レポート生成を行う、FastAPIベースのログインテリジェンス・分析ツールです。

## Current Status / 現在のステータス

LogSense is a FastAPI and PostgreSQL application for importing, storing, analysing, and reporting operational application logs.

### Completed
- FastAPI API layer
- PostgreSQL log storage
- SQLAlchemy database integration
- Log importing and persistence
- Stored log retrieval
- Log severity summaries
- Error analysis and reporting
- Live log preview endpoint
- Docker support
- Docker Compose API + PostgreSQL environment
- Swagger API documentation
- GitHub Actions backend CI

### Known Issue
- Repeated calls to `/logs/import` can create duplicate stored log entries.

### Finalisation Roadmap
- Prevent duplicate log imports
- Add a small read-only LogSense dashboard for log summaries and analysis
- Complete project documentation
- Capture final screenshots and presentation material
- Move LogSense to maintenance

## Features / 機能

| EN | 日本語 |
| --- | --- |
| Log severity categorisation | ログの重要度分類 |
| INFO / WARNING / ERROR detection | INFO / WARNING / ERROR の検出 |
| Repeated error tracking | 重複エラーの追跡 |
| Error frequency analysis | エラー発生頻度の分析 |
| Timestamp and hour-based error analysis | タイムスタンプ・時間帯別のエラー分析 |
| Exportable analysis reports | エクスポート可能な分析レポート |
| Colour-coded CLI output | 色分けされたCLI出力 |
| PostgreSQL log persistence | PostgreSQLへのログ保存 |
| Log import and retrieval API | ログのインポート・取得API |
| Live log preview endpoint | 最新ログのライブプレビュー |
| FastAPI REST API | FastAPI REST API |
| Swagger API documentation | Swagger APIドキュメント |
| Dockerised development environment | Docker開発環境 |
| Modular backend architecture | モジュール化されたバックエンド構成 |

## Tech Stack / 技術スタック

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy

### Database
- PostgreSQL

### Infrastructure
- Docker
- Docker Compose

### Tooling
- Git
- GitHub
- GitHub Actions CI
- Colorama

### Architecture
- Modular service and route structure
- REST API
- PostgreSQL persistence

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
docker build -t logsense .
```

Run the API container:
```bash
docker run -p 8000:8000 logsense-api
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

## Continuous Integration

LogSense uses GitHub Actions for automated backend checks on pushes and pull requests.

The current CI workflow:

- Checks out the repository
- Sets up the Python environment
- Installs project dependencies
- Validates the backend
- Runs available tests
- Builds the Docker image when a Dockerfile is present

Deployment is separate from the current GitHub Actions CI workflow.

## Project Structure / プロジェクト構成

```text
logsense/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── log_model.py
│   ├── routes/
│   │   └── log_routes.py
│   └── services/
│       └── log_service.py
├── sample_logs/
│   └── server.log
├── analytics.py
├── analyzer.py
├── parser.py
├── reporter.py
├── analysis_report.txt
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Documentation

Detailed project documentation is available in the [`docs/`](docs/) directory.

| Document | Description |
| --- | --- |
| [API Examples](docs/api-examples.md) | Example requests for interacting with the LogSense API |
| Architecture | Coming during finalisation |
| Development Notes | Coming during finalisation |

## Finalisation / 最終調整

LogSense is approaching feature completion. Remaining work is intentionally limited to:

| EN | 日本語 |
| --- | --- |
| Prevent duplicate log imports | 重複ログ登録の防止 |
| Add a small read-only analysis dashboard | 読み取り専用の分析ダッシュボードを追加 |
| Complete architecture and development documentation | アーキテクチャ・開発ドキュメントの完成 |
| Capture final screenshots and presentation material | 最終スクリーンショット・紹介資料の作成 |
| Move the project to maintenance | プロジェクトをメンテナンス段階へ移行 |

Once these items are complete, further development will be limited to maintenance, dependency updates, bug fixes, and documentation improvements.