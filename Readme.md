## 概要
MLflow Trackingサーバーのデプロイスクリプト



## Docker-ComposeでMLflowサーバを構築

```bash
cd mlflow-server
docker-compose up -d
```


## mysql
```bash
mysql -u root -p -h 127.0.0.1 -P 3306
```

# minio
```bash
aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3 ls

# コマンドをaliasで登録
alias minio="aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3"
# 一覧
alias

# 利用例
minio ls 
minio cp hoge.txt s3://mlflow-artifact-strage
```

## k8s上にデプロイ
```bash
make mlflow/deploy
```

## 学習スクリプトのサンプルを実行
以下のスクリプトを実行すると、mnistの分類モデルの学習が実行されます。
```bash
cd examples/training/pytorch-model
pip install -r requirement.txt
python train.py
```


<!-- ## モデルをデプロイ
```bash
MLFLOW_CONDA_HOME=PATH_TO_CONDA_COMMAND #~/.pyenv/versions/anaconda3-2021.05/condabin/conda
AWS_ACCESS_KEY_ID=minio
AWS_SECRET_ACCESS_KEY=password
MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9000

mlflow models serve -m models:/mnist-pytorch/latest
``` -->
