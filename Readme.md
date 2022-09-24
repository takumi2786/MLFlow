## Abstruct
This is the example to deploy mlflow tracking server.



## Deploy with docker-compose

```bash
cd mlflow-server
docker-compose up -d
```


**access to mysql**
```bash
mysql -u root -p -h 127.0.0.1 -P 3306
```

**access to minio**
```bash
aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3 ls
```

**register alias**
```
alias minio="aws --profile minio --endpoint-url http://127.0.0.1:9000/ s3"
```

## Deploy to k8s cluster
```bash
make mlflow/deploy
```

## Execute training example
mnist classification
```bash
cd examples/training/pytorch-model
pip install -r requirement.txt
python train.py
```
