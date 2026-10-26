# 04. Google Cloud でよく使われる言語と BigQuery の操作方法

結論：GC のデータ処理・API 連携では **Python が第一言語**。Node.js も使えるが、BigQuery や Google API のライブラリ・サンプルは Python が最も充実。

## 言語別の位置づけ

| 言語 | 位置づけ | 向いている用途 | 備考 |
| --- | --- | --- | --- |
| Python | 第一言語。公式サンプルの大半 | BQ のデータ操作、ETL、API 連携バッチ、AI/ML | pandas + `google-cloud-bigquery` が定番 |
| SQL | BQ の中核。Python より先に覚える | 集計・変換・レポート | BQ は「SQL で大半が済む」設計 |
| Node.js / TypeScript | Web アプリ・Cloud Run functions・Firebase | Next.js の API、Webhook 受け口 | BQ ライブラリはあるがデータ処理は Python に劣る |
| Go | Google 社内の言語。Cloud Run functions で高速 | 軽量 API、高負荷処理 | 個人開発では少数派 |
| Java | 大企業の Dataflow / Dataproc | 大規模パイプライン | 今から選ぶ理由は薄い |
| GAS | スプレッドシート・Gmail・Drive 連携 | 社内ツール、BQ への簡易クエリ | BQ Connector でスプレッドシートから直接読める |

## BigQuery のデータ操作：4つの方法

| 方法 | 使う場面 | 言語・ツール |
| --- | --- | --- |
| コンソールで SQL | 分析・確認・アドホック集計 | SQL |
| Python クライアント | バッチ処理、取り込み、他 API との組み合わせ | Python + `google-cloud-bigquery` + pandas |
| Connected Sheets | 現場担当がスプレッドシートで見る | コード不要 |
| Dataform / Scheduled Queries | 定期的な変換・集計の自動化 | SQL（Dataform は SQLX） |

### Python 最小例
```python
from google.cloud import bigquery

client = bigquery.Client(project="my-project")
sql = "SELECT date, SUM(cost) AS cost FROM `my-project.ads.daily` GROUP BY date"
df = client.query(sql).to_dataframe()
```

## API 連携でよく使う構成

| 連携先 | 典型パターン | 言語 |
| --- | --- | --- |
| Google Ads / GA4 / Search Console | BigQuery Data Transfer Service で自動取り込み（コード不要）。細かい制御は Python | SQL / Python |
| Meta / Instagram / Shopify など | Cloud Scheduler → Cloud Run jobs（Python）→ BQ | Python |
| Webhook 受け口 | Cloud Run functions で受けて Pub/Sub に流す | Node.js / Python |
| Claude / Gemini | Cloud Run（Python）から Vertex AI または Anthropic API | Python |
| スプレッドシート出力 | BQ → Connected Sheets、または GAS から BQ API | SQL / GAS |

## 認証の基本

GC の API は「サービスアカウント」で認証。Cloud Run 上では自動付与されるのでキーファイル不要。
ローカル開発では `gcloud auth application-default login` を1回実行すれば Python ライブラリが自動で使う。

## 学ぶ順番
1. BigQuery の SQL（コンソールで触る）
2. Python + `google-cloud-bigquery` + pandas
3. Cloud Run jobs + Cloud Scheduler で定期実行
4. 必要になったら Dataform で変換を SQL に寄せる
