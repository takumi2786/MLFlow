# SageMaker PyTorch image
FROM 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com/pytorch-training:1.5.1-cpu-py36-ubuntu16.04

RUN pip install mlflow GitPython

ENV PATH="/opt/ml/code:${PATH}"
# this environment variable is used by the SageMaker PyTorch container to determine our user code directory.
ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/code

# /opt/ml and all subdirectories are utilized by SageMaker, use the /code subdirectory to store your user code.

# Defines cifar10.py as script entrypoint 


