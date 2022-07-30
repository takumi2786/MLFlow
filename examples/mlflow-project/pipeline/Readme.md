# PIPELINE
## 概要

MLflow Projectを利用したパイプライン。
github上のmlflowプロジェクトをlocal環境もしくは、sagemakerで実行する。

## 環境構築

```bash
# ライブラリを入れる
pip install mlflow
pip install GitPython
pip install sagemaker

# 家から実行する場合は、VPN接続する。

# AWSのmfa認証を行う

# gitのid, tokenを環境変数に登録
export GIT_ID="XXXX"
export GIT_TOKEN="XXXX"
```

## 実行
  
```bash
cd pipeline
MLFLOW_EXPERIMENT_NAME=hello_mlflow \
MLFLOW_TRACKING_URI=https://mlflow.safie-dev.link \
mlflow run . --no-conda
```