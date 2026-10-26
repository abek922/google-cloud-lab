"""課題1: Cloud Run に最小の Python アプリをデプロイする。

デプロイ:
  cd apps/hello-cloud-run
  gcloud run deploy hello-cloud-run --source . --region asia-northeast1 --allow-unauthenticated

ポイント:
- PORT 環境変数で待ち受ける（Cloud Run が渡してくる）
- ログは標準出力に print するだけで Cloud Logging に集まる
- Dockerfile なし。Buildpacks が requirements.txt を見て自動でイメージを作る
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    print("request received")  # これが Cloud Logging に出る
    return jsonify(message="Hello from Cloud Run", region=os.environ.get("GCP_REGION", "unknown"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
