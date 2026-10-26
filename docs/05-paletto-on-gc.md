# 05. Paletto を Google Cloud で考えた場合

## Paletto の現在の構成
- Next.js 15 + Supabase + Claude API + Vercel のマルチテナント SaaS（アパレル向けデジタルマーケ）
- Google Ads API 連携（テナント別 OAuth、`integration_tokens` テーブル + RLS）
- Meta / Instagram：フィード・リールは取得済み、ストーリーズは24時間期限のため webhook + ポーリングのハイブリッド設計
- GitHub Actions + Claude Code（@claude で PR 自動生成）

## コンテナ化の考え方

**前提：Vercel はコンテナ不要**。コンテナ化が意味を持つのは「Vercel 以外で動かす」「Vercel に向かない処理を切り出す」とき。

### コンテナ化が効きそうな部分（Next.js 本体ではなく裏側）
- **Instagram ストーリーズの定期取得**：24時間で消えるのでポーリングが要る。Cloud Run jobs にすれば Vercel の実行時間制限を気にせず回せる
- **Google Ads API の集計バッチ**：テナント数が増えると長時間化
- **Claude API を使う重い分析**：複数テナント分をまとめて処理

→ 「Next.js（画面・API）は Vercel、長時間バッチは Cloud Run」の分担が自然。

### 仮に Next.js 本体をコンテナ化するなら
- `next.config.js` に `output: 'standalone'`
- ベースは `node:20-slim` または `node:20-alpine`
- `SUPABASE_URL`、`ANTHROPIC_API_KEY`、Google/Meta のトークンは全部環境変数。`.env` はイメージに焼かない
- `PORT` 環境変数で待ち受け
- RLS 前提は変わらず、コンテナ側は状態を持たない

Paletto はすでに「状態は Supabase・設定は環境変数・RLS でテナント分離」なので、コンテナの作法とほぼ合致。
追加で意識するのは「ログは標準出力」「Web / バッチを分ける」の2点。

## 現実的な使い分け

Next.js + Supabase + Vercel はそのまま残し、GC は「データ基盤と長時間バッチ」だけに使う。

| 層 | いまの担当 | GC を足すならここ | 理由 |
| --- | --- | --- | --- |
| 画面・API | Vercel | 変えない | Vercel の方が楽で速い |
| アプリ DB・認証・RLS | Supabase | 変えない | テナント分離の設計がある |
| 広告・SNS の集計データ | Supabase | BigQuery | Google Ads / GA4 は Data Transfer で自動取り込み。横断集計は BQ が楽 |
| 長時間バッチ | Vercel Cron（時間制限あり） | Cloud Scheduler + Cloud Run jobs（Python） | 24時間まで。テナント増にも対応 |
| レポート出力 | 自前実装 | Connected Sheets / Looker Studio | BQ にあればスプレッドシートに直結 |
| コード管理・CI | GitHub + Actions | 変えない | Actions から `gcloud run deploy` |

### 言語の使い分け
- Next.js 側（Vercel）：TypeScript
- GC 側（Cloud Run jobs、BQ）：Python + SQL

### 最初の一歩
1. GC プロジェクトを1つ作り、BigQuery Data Transfer で Google Ads を取り込む（コード不要）
2. BQ の SQL で集計
3. 必要になったら Python で Instagram ストーリーズ取得を Cloud Run jobs に切り出す

## 費用比較（2026年10月時点の目安）

結論：小規模ならほぼ変わらず、月1,500〜7,000円程度。差が出るのは「DB の最低料金」と「開発者の人数」。

### 現在（Vercel + Supabase）
- Vercel Pro：1開発者あたり月 $20（$20 分の利用クレジット込み）。Hobby は商用不可
- Supabase Pro：月 $25
- 合計：**月 $45 前後（約7,000円）**

### GC に置き換えた場合
- Cloud Run（Next.js）：無料枠が大きく、小規模なら $0〜数ドル
- Cloud SQL（PostgreSQL）：最小構成（共有 CPU・0.6GB・10GB）で月 $9.37（us-central1。東京は2割高）。デフォルト構成なら3か月無料トライアル
- Firebase Auth：月5万ユーザーまで無料
- BigQuery：ストレージ 10GB・クエリ 1TB/月まで無料
- Scheduler / Secret Manager：ほぼ無料
- 合計：**月 $10〜20（約1,500〜3,000円）**

### 見えないコスト
- Cloud SQL 最小構成は本番には心もとない。Supabase Pro 相当（2vCPU・8GB）にすると月 $50〜100 に跳ねて逆転
- Cloud SQL は最低1台分が常時課金
- Vercel の画像最適化・CDN・プレビューデプロイを GC で再現すると LB だけで月 $18〜
- 構築・運用の手間（コンテナ、LB、IAM）は確実に増える

### 判断
- 1〜2人なら **Vercel + Supabase のまま**
- 開発者5人以上なら Vercel の席代（$100〜）が効くので Next.js を Cloud Run に移すと下がる
- 広告・SNS 集計だけ BigQuery に足すのは無料枠内でほぼ追加費用なし。**これが一番コスパが良い**

参考：
- https://vercel.com/docs/plans/pro
- https://cloud.google.com/sql/docs/postgres/pricing-examples?hl=ja
