"""課題2: BigQuery の公開データセットを Python から集計する。

準備:
  gcloud auth application-default login
  pip install -r requirements.txt

実行:
  GCP_PROJECT_ID=abek-gc-lab python query.py

公開データは誰でも無料枠内で読める。ここでは「シカゴ市のタクシー乗車数」を月別に集計する。
"""
import os
from google.cloud import bigquery

PROJECT = os.environ["GCP_PROJECT_ID"]

SQL = """
SELECT
  FORMAT_DATE('%Y-%m', DATE(trip_start_timestamp)) AS month,
  COUNT(*) AS trips,
  ROUND(AVG(fare), 2) AS avg_fare
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE DATE(trip_start_timestamp) BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY month
ORDER BY month
"""

if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT)
    job = client.query(SQL)
    df = job.to_dataframe()
    print(df.to_string(index=False))
    mb = job.total_bytes_processed / 1024 / 1024
    print(f"\nscanned: {mb:.1f} MB  (無料枠 1TB/月)")
