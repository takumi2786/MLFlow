FROM python:3.8

RUN apt update && apt upgrade -y \
&&  apt install -y default-libmysqlclient-dev \
# clean up image
&&  apt clean \
&&  rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN pip install mlflow mysqlclient sqlalchemy boto3
RUN mkdir -p /mlflow
WORKDIR /mlflow