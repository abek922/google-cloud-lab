# CLAUDE.md — google-cloud-lab

このリポジトリは **Google Cloud を学ぶための練習場** です。本番サービスではありません。

## 利用者について

- 普段の開発スタック：Next.js + Supabase + Vercel、GitHub Actions、GAS、VBA
- Google Cloud は初学者。AWS も未経験
- Vercel / Supabase の概念に置き換えて説明すると理解しやすい（`docs/02-service-mapping.md` 参照）
- 本業はアパレル向けのデジタルマーケ支援。Shopify / Meta / Google Ads のAPI連携に関心がある
- 既存プロジェクト「Paletto」（Next.js + Supabase + Vercel のマルチテナントSaaS）への応用が最終目標

## Claude Code への指示

### 基本方針
- **説明しながら進める**。コマンドを実行する前に、何をするのか・なぜ必要かを1〜2行で添える
- **無料枠を超える操作は実行前に確認する**。特に Cloud SQL / GKE / Compute Engine / ロードバランサーの作成
- **Python + SQL を優先**。GC側の処理は Python、Next.js側は TypeScript という役割分担（docs/04 参照）
- `gcloud` / `bq` コマンドは直接実行してよい。MCP があれば BigQuery はそちらを使ってもよい
- GC プロジェクト：`abek-gc-lab`（表示名 abek-google-cloud-lab）
- リージョンは `asia-northeast1`（東京）を既定とする

### やらないこと
- `.env` や鍵ファイルをコミットしない。シークレットは Secret Manager か環境変数
- Dockerfile は必要になるまで書かない。まず `gcloud run deploy --source .` で動かす
- 本番の Paletto リポジトリ（abek922/paletto.cloud）には触れない。ここでは設計の検討まで

### 環境変数
以下を `.env.local`（git管理外）に置く想定：
```
GCP_PROJECT_ID=abek-gc-lab
GCP_REGION=asia-northeast1
```

### 進め方
`README.md` の学習ロードマップに沿って進める。各課題は `apps/` 配下にディレクトリを作り、
完了したら `docs/` に学んだことを追記する。

## 参考ドキュメント
- `docs/00-claude-code-setup.md` — Claude Code の初期設定手順
- `docs/01-cloud-functions-vs-cloud-run.md` — 関数とコンテナの違い、Dockerイメージとは
- `docs/02-service-mapping.md` — Vercel/Supabase/GitHub/Cloudflare/AWS と GC の対応表
- `docs/03-roles-explained.md` — ホスティング・DB・CDN など各役割の解説
- `docs/04-languages-and-bigquery.md` — GCで使う言語、BigQuery の4つの操作方法
- `docs/05-paletto-on-gc.md` — Paletto をGCで考えた場合の構成と費用比較
- `docs/06-claude-code-and-gc.md` — Claude Code から GC を操作する方法
