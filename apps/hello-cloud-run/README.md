# 課題1: hello-cloud-run

## ゴール
`gcloud run deploy` だけで Python アプリを公開し、URL で JSON が返るのを確認する。

## 手順
```bash
cd apps/hello-cloud-run
gcloud run deploy hello-cloud-run --source . --region asia-northeast1 --allow-unauthenticated \
  --set-env-vars GCP_REGION=asia-northeast1
```
出力される URL をブラウザで開く。

## 学ぶこと
- Buildpacks によるソースデプロイ（Dockerfile 不要）
- PORT 環境変数（Cloud Run が自動で渡す）と、自分で渡す環境変数（`--set-env-vars`。付けないと region が `unknown` になる）
- Cloud Logging でのログ確認：`gcloud run services logs read hello-cloud-run --region asia-northeast1`

## 片付け
```bash
gcloud run services delete hello-cloud-run --region asia-northeast1
```
