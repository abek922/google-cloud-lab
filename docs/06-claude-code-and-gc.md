# 06. Claude Code から Google Cloud を操作する

Vercel / Supabase と同じことが GC でもできる。やり方は2系統。

## 1. Claude Code + gcloud CLI（一番確実）

Claude Code はターミナルを叩けるので、`gcloud` が入っていれば GC の操作はほぼ全部できる。

```bash
gcloud run deploy --source .                 # Cloud Run にデプロイ
bq query --use_legacy_sql=false 'SELECT ...' # BigQuery の SQL 実行
gcloud scheduler jobs create http ...        # 定期実行の設定
gcloud secrets create ...                    # シークレット登録
gcloud run jobs create ...                   # バッチジョブ作成
```

最初に `gcloud auth login` を1回通せば OK。

## 2. MCP サーバーで接続（会話型）

Google 公式の MCP サーバー：
- **Cloud Run MCP**：会話で Cloud Run へデプロイ・ログ確認
- **MCP Toolbox for Databases**：Cloud SQL / AlloyDB / BigQuery に SQL
- **BigQuery MCP**：データセット閲覧・クエリ実行

claude.ai の BigQuery コネクタをつなげば、ブラウザからも BQ の SQL を直接実行できる。

## GitHub → Vercel の流れを GC に置き換える

1. GitHub Actions に「push されたら `gcloud run deploy`」のワークフローを1本足す（`.github/workflows/deploy-cloud-run.yml` が雛形）
2. Claude Code がコードを編集して push すれば自動で Cloud Run に反映
3. Vercel の「つなぐだけ」より一手間あるが、Claude Code にワークフローを書かせれば数分

認証は **Workload Identity Federation** を使い、サービスアカウントのキーファイルを GitHub に置かない。

## 向き不向き
- デプロイ・SQL・インフラ設定 → CLI が確実で速い
- データを見ながら相談・分析 → MCP（BigQuery）が便利
- Cloud Run jobs 作成から Scheduler 登録まで一気通貫 → Claude Code に任せる

## Paletto で試すなら
「BQ Data Transfer で Google Ads を取り込む → Claude Code で SQL 集計を書く」が、コードもインフラも最小で始められる入口。
