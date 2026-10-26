# 課題2: bq-sample

## ゴール
公開データセットに SQL を投げ、pandas の DataFrame として受け取る。

## 手順
```bash
cd apps/bq-sample
pip install -r requirements.txt
GCP_PROJECT_ID=abek-gc-lab python query.py
```

## 学ぶこと
- `google-cloud-bigquery` クライアントの基本
- スキャン量課金の感覚（`total_bytes_processed`）
- WHERE で日付を絞るとスキャン量が減る（パーティション）

## 次のステップ（課題3）
このスクリプトを Cloud Run jobs にして、Cloud Scheduler で毎朝実行する。
