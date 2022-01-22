aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com
docker pull 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com/pytorch-training:1.5.1-cpu-py36-ubuntu16.04
