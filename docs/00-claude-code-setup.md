# 00. Claude Code 初期設定（クラウドで進める）

ローカル PC にインストールせず、ブラウザだけで進める構成。2つの選択肢がある。
設定の仕様は変わることがあるので、迷ったら公式ドキュメント（https://docs.claude.com/en/docs/claude-code/overview）を確認。

| | A. Cloud Shell + Claude Code（推奨） | B. Claude Code on the web（claude.ai/code） |
| --- | --- | --- |
| 動く場所 | Google Cloud 内の無料 VM（ブラウザ端末） | Anthropic のクラウド環境 |
| GC 認証 | 最初からログイン済み。鍵ファイル不要 | サービスアカウントの鍵を環境変数で渡す必要あり |
| ネットワーク | GC API に素通し | 既定では googleapis.com に出られない。環境設定で許可が必要 |
| スマホから | ブラウザで可（画面は狭い） | claude.ai アプリから可。使いやすい |
| 向き | gcloud を叩く課題全般 | コード編集・ドキュメント整備・設計相談 |

**使い分け**：gcloud / bq を実行する課題は A、ドキュメント整備や設計の相談は B。
両方とも同じ GitHub リポジトリ（abek922/google-cloud-lab）を見るので、併用して問題ない。

## A. Cloud Shell + Claude Code（推奨）

### 1. Cloud Shell を開く
Google Cloud コンソール右上の「Cloud Shell をアクティブにする」（ターミナルのアイコン）。
無料、5GB のホームディレクトリが永続、gcloud は自分のアカウントで認証済み。

### 2. Claude Code をインストール（初回のみ）
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```
Cloud Shell には Node.js が入っている。ホームに残るので2回目以降は不要。

### 3. リポジトリを取得
```bash
git clone https://github.com/abek922/google-cloud-lab.git
cd google-cloud-lab
```
push するなら GitHub の認証が要る：`gh auth login` を1回実行。

### 4. GC 側の準備（初回のみ）
```bash
gcloud config set project abek-gc-lab
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com bigquery.googleapis.com \
  cloudscheduler.googleapis.com secretmanager.googleapis.com
```

### 5. 起動
```bash
claude
```
初回はブラウザでログイン（Claude.ai のアカウント）。
その後「README のロードマップの課題1から始めて」と言えば CLAUDE.md を読んで進める。

### 注意
- Cloud Shell は一定時間操作がないと切断される。長いビルドは `gcloud builds submit` などサーバー側で動くものに任せる
- エディタが欲しければ Cloud Shell エディタ（VS Code ベース）がボタン1つで開く

## B. Claude Code on the web（claude.ai/code）

claude.ai の「Code」から GitHub リポジトリを選んで起動する方式。コード編集や docs の更新はこれで十分。
gcloud も動かすなら、環境（Environment）を1つ作る。公式ドキュメント：https://code.claude.com/docs/ja/cloud-environments

### 環境の作り方
claude.ai/code のメッセージ欄の上にある雲アイコン → 「クラウド環境を追加」。設定項目は4つ。

| 項目 | 推奨値 | 理由 |
| --- | --- | --- |
| Name | `gc-lab` | |
| Network access | **Custom**、「Also include default list」にチェック、追加ドメインに `dl.google.com` と `packages.cloud.google.com` | Trusted（既定）には `*.googleapis.com` が含まれるので API 呼び出しは通る。gcloud CLI のインストール元だけ追加が要る |
| Environment variables | `GCP_PROJECT_ID=abek-gc-lab`<br>`GCP_REGION=asia-northeast1`<br>`GCP_SA_KEY_B64=<鍵の base64>` | 環境変数は環境を使える人全員に見える。個人環境なら自分だけだが、鍵は学習用・最小権限に限定する |
| Setup script | 下記 | gcloud / gh は VM に入っていないので入れる。初回だけ実行され、スナップショットがキャッシュされる |

Setup script：
```bash
#!/bin/bash
set -e
# gcloud CLI
curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts --install-dir=/opt >/dev/null
ln -sf /opt/google-cloud-sdk/bin/gcloud /usr/local/bin/gcloud
ln -sf /opt/google-cloud-sdk/bin/bq /usr/local/bin/bq
# gh CLI（PR 操作などで使う。無くても GitHub の組み込みツールで足りる）
apt-get update -qq && apt-get install -y -qq gh || true
# Python ライブラリ
pip install -q google-cloud-bigquery[pandas] flask gunicorn || true
```
5分以内に終わること、終了コードが0であることが条件。

### サービスアカウント鍵の作り方（Cloud Shell で1回）
ブラウザログインができないので、学習用の限定的なサービスアカウント鍵を使う。
```bash
gcloud iam service-accounts create claude-code-lab --project abek-gc-lab
for role in roles/run.admin roles/bigquery.user roles/cloudscheduler.admin \
            roles/secretmanager.admin roles/artifactregistry.admin \
            roles/cloudbuild.builds.editor roles/iam.serviceAccountUser; do
  gcloud projects add-iam-policy-binding abek-gc-lab \
    --member serviceAccount:claude-code-lab@abek-gc-lab.iam.gserviceaccount.com \
    --role $role --quiet
done
gcloud iam service-accounts keys create key.json \
  --iam-account claude-code-lab@abek-gc-lab.iam.gserviceaccount.com
base64 -w0 key.json   # 出力を GCP_SA_KEY_B64 に貼る
rm key.json
```

### セッション開始時
CLAUDE.md に書いてあるので Claude Code が自分で実行する：
```bash
echo "$GCP_SA_KEY_B64" | base64 -d > /tmp/sa.json
gcloud auth activate-service-account --key-file /tmp/sa.json
gcloud config set project "$GCP_PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS=/tmp/sa.json
```

### 注意
- 鍵は **abek-gc-lab 専用・学習用** に限定。Paletto や他プロジェクトの権限は付けない
- 鍵をリポジトリにコミットしない（`.gitignore` で `*.json` を除外済み）
- 使わなくなったら `gcloud iam service-accounts keys delete` で失効させる
- 鍵を環境変数に置きたくなければ、gcloud を使う課題だけ Cloud Shell（A）でやればよい。web 側は環境変数なしで docs とコード編集に使う
- `~/.claude/` のユーザー設定・MCP はクラウドに引き継がれない。リポジトリの `.claude/settings.json` と `.mcp.json` に書く

## 共通：設定ファイルと CLAUDE.md

- `CLAUDE.md`（リポジトリ直下）：起動時に必ず読まれる。背景・方針・プロジェクト ID を記載済み
- `.claude/settings.json`：許可 / 拒否ルール。`gcloud run` / `bq` などは確認なし、`gcloud sql` / `compute` / `container` は拒否
- `.claude/settings.local.json`：自分だけの一時設定（gitignore 済み）
- 全プロジェクト共通の好みは `~/.claude/settings.json` と `~/.claude/CLAUDE.md`

## よく使うコマンド

| コマンド | 用途 |
| --- | --- |
| `/permissions` | 許可ルールの確認・編集 |
| `/mcp` | MCP サーバーの状態 |
| `/compact` | 会話を要約して続行 |
| `/cost` | 利用量 |
| `Shift+Tab` | 許可モード切替（都度確認 ⇔ 自動承認） |

自動承認モード（`--dangerously-skip-permissions`）は学習中は使わない。課金操作を勝手に実行される。
