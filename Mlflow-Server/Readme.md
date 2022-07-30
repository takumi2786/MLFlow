## 概要
MLflow Trackingサーバーの構築例。



## Docker-ComposeでMLflowサーバを構築


```bash
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

# 使ってみる
minio ls 
minio cp hoge.txt s3://mlflow-artifact-strage
```
