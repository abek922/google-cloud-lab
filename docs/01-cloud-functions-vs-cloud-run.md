# 01. Cloud Functions と Cloud Run の違い、Dockerイメージの基礎

## Cloud Functions vs Cloud Run

一言でいうと：**Cloud Functions は「関数を1つ置くだけ」、Cloud Run は「コンテナを丸ごと動かす」**。

現在は統合が進み、Cloud Functions（第2世代）は「Cloud Run functions」という名前になり、実態は Cloud Run 上で動く。
違いは「別サービス」ではなく「どこまで自分で面倒を見るか」。

### Cloud Run functions（旧 Cloud Functions）
- 書くのは関数（コード）だけ。Dockerfile もサーバー設定も不要
- 「HTTPが来たら」「Storage にファイルが置かれたら」などイベント駆動向き
- 対応言語は Node.js / Python / Go / Java など決まったもの
- 例：Shopify の webhook を受けてスプレッドシートに書く、画像がアップされたらリサイズ

### Cloud Run
- コンテナ（Docker イメージ）を渡して動かす。言語・ライブラリ・OSレベルの設定は自由
- Web アプリや API サーバーなど「常時リクエストを受けるもの」向き
- 1インスタンスで複数リクエストを同時処理でき、メモリ・CPU の上限も大きい
- 例：Next.js や FastAPI のアプリ、Puppeteer 入りのクローラー

### 使い分け
- ちょっとした処理・イベント連携 → Cloud Run functions
- アプリ本体・特殊な依存あり → Cloud Run

どちらもリクエストがなければゼロまで縮むので、小規模なら無料枠内。

## Docker イメージとは

**アプリを動かすのに必要なものを全部まとめた1つのパッケージ**。スマホアプリの APK に近い。

層構造：
- ベース：最小限の OS（Debian、Alpine など）
- ランタイム：Node.js、Python などの実行環境
- ライブラリ：npm install / pip install した依存
- 自分のコード
- 起動コマンド

### なぜ便利か
「自分のPCでは動くのにサーバーで動かない」が消える。環境ごと固めてあるので、どこでも同じように動く。

### 作り方（Python の例）
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### 用語
- イメージ：設計図・パッケージ（動いていない）
- コンテナ：イメージを起動したもの（動いている）
- レジストリ：イメージの置き場。GC では Artifact Registry

### 補足
Cloud Run は Dockerfile がなくてもソースから自動でイメージを作る（Buildpacks）。
最初は `gcloud run deploy --source .` で十分。

## 「コンテナにOSが入っている」の意味

コンテナに入っているのは **OS全体ではなく「OSの道具箱の中身」だけ**。

### 例え：ビルの中のテナント店舗
- ビル本体（カーネル）：電気・水道・構造。サーバー側の Linux が1つだけ提供
- テナント店舗（コンテナ）：内装・什器・商品は店ごとに違う。これがイメージの中身

だからイメージは数十〜数百MBと軽く、起動も数秒。仮想マシンはビルごと建てるので数GB・数分。

### `python:3.12-slim` の中身
- `/bin/ls`、`/bin/sh` などの基本コマンド
- `/usr/lib` の共有ライブラリ（SSL、文字コード処理）
- `apt` パッケージ管理ツール
- Python 本体
- **入っていないもの**：カーネル、ドライバ、GUI、デスクトップ

## コンテナ前提の作法と OS の選択

### OS について
メジャーなのは **Debian（slim）と Ubuntu**。Alpine は小さいがクセがある。

- Alpine は標準Cライブラリが特殊（musl）で、numpy / pandas などがビルド失敗・遅くなることがある
- 日本語フォントや文字コードで追加設定が要ることがある
- 公式 Python イメージも「迷ったら slim」

目安：Python でデータ系なら slim、Node.js や単純な API なら Alpine でも可。

### コンテナ前提の作法（The Twelve-Factor App）
- **1コンテナ1プロセス**：Web サーバーとバッチを同居させない
- **設定は環境変数で渡す**：API キーや DB 接続先をコードに埋めない
- **状態を持たない**：ファイルをローカルに保存しない。DB や Cloud Storage へ。コンテナは再起動で中身が消える
- **ログは標準出力**：`print` / `console.log` で出す。Cloud Run が自動収集
- **PORT 環境変数で待ち受ける**：Cloud Run が `PORT` を渡してくる
- **依存は固定**：`requirements.txt` / `package-lock.json` でバージョン確定

GAS / VBA からの移行なら「設定は環境変数・保存先はクラウド・ログは標準出力」の3つを守れば OK。
