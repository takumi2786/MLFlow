## 概要
MLflow Trackingサーバーの構築手順とシステム構成。

## Pythhon環境
```bash
pip install mlflow
pip install boto3
pip install mysqlclient
```

## MLflowサーバの起動
**mysql**
```bash
## mysql
sudo apt update
sudo apt install mysql-server

# sudoなしでrootログインできるように設定 https://note.com/junf/n/na40fbca9e6ea
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
# rootでログインできることを確認
mysql -u root -p
# ok

# userを追加
CREATE USER 'mlflow' IDENTIFIED BY 'pass';
GRANT ALL ON *.* TO mlflow;
mysql -u mlflow -p

# [mysql]ポート番号を確認
code /etc/mysql/my.cnf 
# port=8898

# [ufw]ポート開放
sudo ufw status

# [mysql]任意の接続先を許可
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf

# local mac から接続確認
LOCAL_IP=192.168.11.108
# LOCAL_IP=127.0.0.1
mysql -u mlflow  -h ${LOCAL_IP} -P 8898 -A
```

**minio**
https://dev.classmethod.jp/articles/s3-compatible-storage-minio/

```bash
docker container run -d --name minio -p 9000:9000 minio/minio:RELEASE.2018-08-25T01-56-38Z server /mnt/data

# AccessKey: QGJ5WQFH8XGQLLXQFM6G
# SecretKey: 4IMg5mF52tv95ByW8l/qF1VmHCOlsjGFKtfzrsIe

# aws cliの設定
aws configure --profile minio
# 確認
aws configure list-profiles
# プロファイルの切り替え
aws_switch

aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3 ls

# コマンドをaliasで登録
alias minio="aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3"

# 一覧
alias

# 使ってみる
minio ls 
minio cp hoge.txt s3://mlflow-artifact-strage
```

**local環境に構築**
```bash
# debug mode
mlflow ui

# mlflow server
mlflow server \
    --backend-store-uri /mnt/persistent-disk \
    --default-artifact-root s3://my-mlflow-bucket/ \
    --host 0.0.0.0

mlflow server \
    --host 0.0.0.0 \
    --backend-store-uri mysql://mlflow:pass@127.0.0.1:8898/mlflow \
    --default-artifact-root ./
```

**kill server**
```bash
lsof -i :5000
pkill -f gunicorn
```

## Docker-ComposeでMLflowサーバを構築


```bash
docker-compose up -d

# mysql
mysql -u root -p -h 127.0.0.1 -P 3306

# minio
aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3 ls
# コマンドをaliasで登録
alias minio="aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3"
# 一覧
alias
# 使ってみる
minio ls 
minio cp hoge.txt s3://mlflow-artifact-strage


mlflow server \
--backend-store-uri 'mysql://mlflow:sufinkusu1@mysql:3306/mlflowdb' \
--default-artifact-root 's3://default/' --host 0.0.0.0 --port 5000


mysql -u root -p -h mysql -P 3306

# https://qiita.com/MasafumiTsuyuki/items/9e03e285d4b9e0c41a7c
```
