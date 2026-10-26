# google-cloud-lab — Google Cloud 学習リポジトリ

Google Cloud（GC）を Claude Code と一緒に学ぶためのリポジトリ。
Vercel / Supabase / GitHub / Cloudflare 構成の経験を土台に、GC の主要サービスを実際に動かしながら理解することが目的。

## 構成

```
google-cloud-lab/
├── CLAUDE.md                 # Claude Code への指示（最初に読まれる）
├── .claude/settings.json     # Claude Code の許可/拒否ルール
├── README.md                 # このファイル
├── docs/
│   ├── 00-claude-code-setup.md              # Claude Code の初期設定
│   ├── 01-cloud-functions-vs-cloud-run.md   # 関数 vs コンテナ、Dockerイメージの基礎
│   ├── 02-service-mapping.md                # Vercel/Supabase/GitHub/Cloudflare/AWS → GC 対応表
│   ├── 03-roles-explained.md                # 各役割（ホスティング・DB・CDN等）の解説
│   ├── 04-languages-and-bigquery.md         # GCで使う言語、BigQueryの操作方法
│   ├── 05-paletto-on-gc.md                  # Paletto構成をGCで考えた場合（費用含む）
│   └── 06-claude-code-and-gc.md             # Claude Code から GC を操作する方法
├── apps/
│   ├── hello-cloud-run/      # 課題1: Cloud Run に最小のPythonアプリをデプロイ
│   └── bq-sample/            # 課題2: BigQuery に公開データをクエリして集計
└── .github/workflows/
    └── deploy-cloud-run.yml  # push で Cloud Run に自動デプロイ（雛形）
```

## 学習ロードマップ

| # | テーマ | ゴール | 使うサービス |
| --- | --- | --- | --- |
| 1 | Cloud Run 入門 | `apps/hello-cloud-run` をデプロイしてURLで応答を見る | Cloud Run, Artifact Registry |
| 2 | BigQuery 入門 | 公開データセットをSQLで集計し、Pythonで読み出す | BigQuery |
| 3 | 定期実行 | 課題2のスクリプトを Cloud Run jobs + Scheduler で毎朝回す | Cloud Run jobs, Cloud Scheduler |
| 4 | 自動デプロイ | GitHub Actions から `gcloud run deploy` を叩く | GitHub Actions, Workload Identity |
| 5 | 外部API連携 | Shopify や Meta のAPIから取得して BigQuery に書く | Cloud Run jobs, Secret Manager |
| 6 | Paletto への応用 | Instagram ストーリーズ取得を Cloud Run jobs に切り出す設計 | 上記すべて |

## 前提セットアップ

```bash
# gcloud CLI（未導入なら）
brew install google-cloud-sdk      # macOS
gcloud init                        # ログイン
gcloud config set project abek-gc-lab
gcloud auth application-default login   # Python ライブラリ用の認証
```

請求先アカウントの紐付けと、次のAPI有効化が必要：

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com bigquery.googleapis.com \
  cloudscheduler.googleapis.com secretmanager.googleapis.com
```

## 費用の目安

小規模な学習用途なら、Cloud Run / BigQuery / Scheduler / Secret Manager はすべて無料枠内。
Cloud SQL だけは最小構成でも月 $9〜 かかるので、学習中は使わない（DBが必要なら Supabase のまま）。
