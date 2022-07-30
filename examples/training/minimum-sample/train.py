import os
import random

import mlflow
from mlflow.tracking import MlflowClient
import pytorch_lightning as pl
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from torchmetrics.functional import accuracy


TRACKING_URI = "http://127.0.0.1:5000"

# mlflow serverのuriを指定
mlflow.set_tracking_uri(TRACKING_URI)

# boto3経由でminioにアクセスするための設定
os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "password"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://127.0.0.1:9000"

# 実験の試行を開始
with mlflow.start_run(run_name="sample training", experiment_id=0) as run:
    mlflow.log_params({
        "version": 1.0,
        "hoge": "huga"
    })

    # start training
    epoch = 100
    for e in range(1, epoch + 1):
        mlflow.log_metric("score", e*random.random(), step=e)
        
    # log artifact
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)
    mlflow.log_artifact("features.txt", artifact_path="features")

