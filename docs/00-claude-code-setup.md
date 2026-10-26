# 00. Claude Code 初期設定（このリポジトリ向け）

Claude Code を初めて使う / 新しい PC で使うときの手順。所要 15 分程度。
設定の仕様は変わることがあるので、迷ったら公式ドキュメント（https://docs.claude.com/en/docs/claude-code/overview）を確認。

## 1. インストールとログイン

```bash
# Node.js 18 以上が必要
npm install -g @anthropic-ai/claude-code
claude --version

# リポジトリで起動 → 初回はブラウザでログイン
cd google-cloud-lab
claude
```

ログインは Claude.ai のアカウント（Pro / Max / Team）か API キーのどちらか。個人の学習用なら Claude.ai アカウントで十分。

## 2. 設定ファイルの3階層

| ファイル | 場所 | 用途 | git 管理 |
| --- | --- | --- | --- |
| ユーザー設定 | `~/.claude/settings.json` | 全プロジェクト共通（自分の好み） | 対象外 |
| プロジェクト設定 | `.claude/settings.json` | このリポジトリのルール。チームで共有 | する |
| ローカル上書き | `.claude/settings.local.json` | 自分だけの一時的な許可など | しない |

優先度は ローカル > プロジェクト > ユーザー。

## 3. 推奨設定（このリポジトリ用）

`.claude/settings.json` をリポジトリに置いてある。中身の意図：

- **許可（allow）**：`gcloud` / `bq` / `git` / `pip` / `python` など学習に必要なコマンドは確認なしで実行
- **拒否（deny）**：`.env*` の読み書き、`rm -rf`、Cloud SQL / GKE / Compute Engine の作成（課金が大きいもの）
- **それ以外**は都度確認（既定の動作）

課金が心配なら allow を減らし、都度確認に戻せばよい。

### 自分の好みをユーザー設定に置く例（`~/.claude/settings.json`）
```json
{
  "permissions": {
    "allow": ["Bash(git status)", "Bash(git diff *)", "Bash(git log *)"]
  }
}
```

## 4. CLAUDE.md（最重要）

リポジトリ直下の `CLAUDE.md` は起動時に必ず読まれる。このリポジトリでは既に用意済み：
- あなたの背景（Vercel / Supabase 経験、GC 初学者）
- 説明しながら進める、課金の大きい操作は確認する、Python + SQL 優先
- GC プロジェクト `abek-gc-lab`、リージョン `asia-northeast1`

`/init` コマンドで自動生成もできるが、このリポジトリでは不要。
全プロジェクト共通の指示は `~/.claude/CLAUDE.md` に書く。

## 5. MCP サーバー（任意）

BigQuery を会話で触りたければ追加。CLI（`bq` コマンド）で十分なら不要。

```bash
# 例：Google 公式 MCP Toolbox for Databases（BigQuery）
claude mcp add --transport stdio bigquery -- npx -y @google-cloud/mcp-toolbox ...
```
設定は `~/.claude.json`（ユーザー）か `.mcp.json`（プロジェクト共有）に入る。
`claude mcp list` で確認。追加前に公式ドキュメント（https://docs.claude.com/en/docs/claude-code/mcp）で最新のコマンドを確認すること。

## 6. gcloud 側の準備（Claude Code を動かす前に）

```bash
gcloud auth login
gcloud config set project abek-gc-lab
gcloud auth application-default login   # Python ライブラリ用
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com bigquery.googleapis.com \
  cloudscheduler.googleapis.com secretmanager.googleapis.com
```

## 7. 最初の対話

```
claude
> README のロードマップの課題1から始めて。コマンドを実行する前に何をするか説明して。
```

## よく使うコマンド

| コマンド | 用途 |
| --- | --- |
| `/init` | CLAUDE.md の雛形生成 |
| `/permissions` | 許可ルールの確認・編集 |
| `/mcp` | MCP サーバーの状態 |
| `/clear` | 会話をリセット |
| `/compact` | 会話を要約して続行（長くなったとき） |
| `/cost` | このセッションの利用量 |
| `Shift+Tab` | 許可モードの切替（都度確認 ⇔ 自動承認） |

## 注意
- `.claude/settings.local.json` と `.env*` は `.gitignore` 済み
- 自動承認モード（`--dangerously-skip-permissions`）は学習中は使わない。課金操作を勝手に実行される
