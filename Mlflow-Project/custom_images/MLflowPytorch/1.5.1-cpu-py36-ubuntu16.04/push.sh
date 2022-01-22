
echo "tag:"
read tag
IMAGE=mlflow-pytorch
aws ecr-public get-login-password --profile default | docker login --username AWS --password-stdin public.ecr.aws/z4r5y2l4
docker tag $IMAGE\:latest public.ecr.aws/z4r5y2l4//$IMAGE\:$tag
docker push 229006280112.dkr.ecr.ap-northeast-1.amazonaws.com/$IMAGE\:$tag