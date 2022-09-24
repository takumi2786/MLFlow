IMAGE_MYSQL=takumi2786/mysql
IMAGE_MLFLOW=takumi2786/mlflow

mysql/build:
	docker build -f docker/mysql/Dockerfile ./docker/mysql -t ${IMAGE_MYSQL}

mysql/push: mysql/build
	docker push ${IMAGE_MYSQL}

mlflow/build:
	docker build -f docker/mlflow/Dockerfile ./docker/mlflow -t ${IMAGE_MLFLOW}

mlflow/push: mlflow/build
	docker push ${IMAGE_MLFLOW}

mlflow/deploy: mlflow/push
	kubectl apply -f ./manifest/mlflow