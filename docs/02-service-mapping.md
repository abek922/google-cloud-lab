# 02. Vercel / Supabase / GitHub / Cloudflare / AWS → Google Cloud 対応表

完全一致ではなく「役割が一番近いもの」を並べている。
GC は「1社で全部揃う」型、Vercel / Supabase / Cloudflare は「得意分野だけ」型。

略称：GC = Google Cloud、BQ = BigQuery、GAS = Google Apps Script。

## Vercel → Google Cloud

| 役割 | Vercel | Google Cloud | 補足 |
| --- | --- | --- | --- |
| Next.js のホスティング | Vercel 本体 | Cloud Run | GC は Docker イメージかソースをデプロイ。Vercel ほど自動最適化されない |
| サーバーレス関数 | Vercel Functions / API Routes | Cloud Run functions | GC はイベント駆動（Storage・Pub/Sub）が得意 |
| エッジ実行 | Edge Functions / Middleware | なし（Cloud CDN + Cloud Run で代替） | GC にエッジで動く関数はほぼない。Cloudflare Workers の方が近い |
| 定期実行 | Vercel Cron | Cloud Scheduler + Cloud Run jobs | GC はジョブを最大24時間動かせる |
| 環境変数・シークレット | Project Settings | Secret Manager | Cloud Run から参照 |
| ビルド・デプロイ | Git push で自動 | Cloud Build（または GitHub Actions） | トリガー設定が必要 |
| ログ・監視 | Vercel Logs / Analytics | Cloud Logging / Monitoring | 標準出力に書けば自動収集 |
| 画像最適化 | next/image | なし | GC に Vercel 相当の画像最適化はない |

## Supabase → Google Cloud

| 役割 | Supabase | Google Cloud | 補足 |
| --- | --- | --- | --- |
| PostgreSQL | Supabase Database | Cloud SQL for PostgreSQL / AlloyDB | Cloud SQL が標準。AlloyDB は高性能版 |
| 認証 | Supabase Auth | Firebase Authentication / Identity Platform | GC では認証は Firebase 側 |
| ストレージ | Supabase Storage | Cloud Storage | S3 互換ではなく GCS 独自 API |
| サーバーレス関数 | Edge Functions（Deno） | Cloud Run functions | Node.js / Python / Go など |
| リアルタイム | Realtime | Firestore（リアルタイムリスナー） | Postgres のリアルタイム購読に直接相当なし |
| ベクトル検索 | pgvector | Vertex AI Vector Search / AlloyDB（pgvector 対応） | 小規模なら Cloud SQL + pgvector |
| 行レベルセキュリティ | RLS | Cloud SQL の Postgres RLS（自前設定） | Postgres 標準なので移植可能 |
| 管理画面 | Supabase Dashboard | Cloud Console | 機能ごとに画面が分かれる |

## GitHub → Google Cloud

| 役割 | GitHub | Google Cloud | 補足 |
| --- | --- | --- | --- |
| Git リポジトリ | GitHub | Cloud Source Repositories（新規受付終了） | GitHub 連携前提。移す必要なし |
| CI/CD | GitHub Actions | Cloud Build | Actions から `gcloud run deploy` を叩く構成が一般的 |
| コンテナイメージ置き場 | GitHub Container Registry | Artifact Registry | Cloud Run はここから取る |
| パッケージ配布 | GitHub Packages | Artifact Registry | npm / pip / Maven も置ける |
| Issue・PR | GitHub | なし | |

## Cloudflare → Google Cloud

| 役割 | Cloudflare | Google Cloud | 補足 |
| --- | --- | --- | --- |
| DNS | Cloudflare DNS | Cloud DNS | 同等。Cloudflare の方が簡単 |
| CDN | Cloudflare CDN | Cloud CDN | Cloud CDN はロードバランサーとセット |
| エッジ関数 | Workers | なし | Cloudflare の強み |
| WAF・DDoS | Cloudflare WAF | Cloud Armor | 設定が重い |
| オブジェクトストレージ | R2 | Cloud Storage | R2 は S3 互換、GCS は独自 |
| KV ストア | Workers KV | Memorystore / Firestore | 用途次第 |
| 静的サイト | Pages | Firebase Hosting / Cloud Storage | Firebase Hosting が近い |
| ロードバランサー | Load Balancing | Cloud Load Balancing | 機能が多いぶん設定も多い |

## AWS → Google Cloud

AWS と GC は同じ「フルスタック型」なのでほぼ1対1。AWS の記事を読むときはこの表で読み替える。

| 分類 | AWS | Google Cloud | 補足 |
| --- | --- | --- | --- |
| 仮想マシン | EC2 | Compute Engine | ほぼ同じ |
| コンテナ（サーバーレス） | Fargate / App Runner | Cloud Run | App Runner が一番近い |
| コンテナ（Kubernetes） | EKS | GKE | GKE の方が歴史が長い |
| 関数 | Lambda | Cloud Run functions | Lambda の方がトリガーが多い |
| オブジェクトストレージ | S3 | Cloud Storage | |
| リレーショナル DB | RDS / Aurora | Cloud SQL / AlloyDB | Aurora ≒ AlloyDB |
| NoSQL | DynamoDB | Firestore / Bigtable | 小規模は Firestore、大規模ログは Bigtable |
| データウェアハウス | Redshift | BigQuery | GC の看板。サーバー管理不要でスキャン量課金 |
| キャッシュ | ElastiCache | Memorystore | |
| メッセージング | SQS / SNS | Pub/Sub | GC は Pub/Sub 一本 |
| ワークフロー | Step Functions | Workflows | |
| 定期実行 | EventBridge Scheduler | Cloud Scheduler | |
| ETL | Glue | Dataflow / Dataform | |
| 認証（利用者） | Cognito | Firebase Authentication / Identity Platform | |
| 権限管理 | IAM | IAM | GC はプロジェクト単位が基本 |
| シークレット | Secrets Manager | Secret Manager | |
| CDN | CloudFront | Cloud CDN | LB と一体 |
| DNS | Route 53 | Cloud DNS | |
| WAF | WAF / Shield | Cloud Armor | |
| CI/CD | CodeBuild / CodePipeline | Cloud Build | どちらも GitHub Actions で代替されがち |
| コンテナレジストリ | ECR | Artifact Registry | |
| 監視・ログ | CloudWatch | Cloud Monitoring / Logging | GC の方がログ検索が速い |
| 生成AI | Bedrock | Vertex AI | Gemini のほか Claude もある |
| 機械学習 | SageMaker | Vertex AI | |
| 低コードアプリ | Amplify | Firebase | |

### 構造上の違い
- **課金・権限の単位**：AWS は「アカウント」、GC は「プロジェクト」。GC は1請求先の下にプロジェクトを何個でも作れ、クライアントごとに分けやすい
- **データ基盤**：AWS は Redshift + Glue + Athena に分かれるが、GC は BigQuery 中心。Google アナリティクス・Google 広告と直結する点も GC 特有
- **ネットワーク**：AWS の VPC はリージョン単位、GC の VPC は全リージョンをまたぐ
