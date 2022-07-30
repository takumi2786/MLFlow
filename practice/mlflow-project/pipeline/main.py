import os
import argparse
import json

import git
import mlflow
from mlflow.tracking import MlflowClient
from sagemaker.pytorch import PyTorch


TRACKING_URI_AWS_GLOBAL = "http://localhost:5000/"
TRACKING_URI_AWS_LOCAL  = "http://localhost:5000/"
DEFAULT_IMAGE_URI       = "229006280112.dkr.ecr.ap-northeast-1.amazonaws.com/pytorch-safie:latest"# Sagemakerが利用するイメージのデフォルト
AWS_ROLE                = 'arn:aws:iam::945686603449:role/sagemaker-execution-role'# Sagemakerの実行RoleのID

def make_git_uri(git_id, git_token, git_url):
    git_url = git_url.replace("https://", "")
    return "https://{}:{}@{}".format(git_id, git_token, git_url)

def execute_git_repo(git_id, git_token, git_url, branch, git_project_dir, run_id, parameters=None, aws_flg=False, **kwargs):
    """
        指定したレポジトリをクローンし、mlflow projectとして実行する。

        git_id:          githubのID
        git_token:       githubのパーソナルアクセストークン
        git_url:         レポジトリのURL
        git_project_dir: レポジトリ内のmlflow projectのパス
        branch:          利用するブランチ
        run_id:          mlflowにおけるrun_id
        aws_flg:         sagemakerを利用するかどうか
        (option)
        instance_type:   sagemakerのインスタンスタイプ
        instance_count:  sagemakerのインスタンス数
        image_uri:       sagemakerで利用するdocker imageのURI
    """
    git_uri = make_git_uri(git_id, git_token, git_url)

    if aws_flg is True: # use sagemaker
        instance_type  = kwargs["instance_type"]  if "instance_type"  in kwargs else "local"
        instance_count = kwargs["instance_count"] if "instance_count" in kwargs else 1
        image_uri      = kwargs["image_uri"]      if "image_uri"      in kwargs else DEFAULT_IMAGE_URI
        tracking_uri   = TRACKING_URI_AWS_GLOBAL  if instance_type is "local"   else TRACKING_URI_AWS_LOCAL
        
        pytorch_processor = PyTorch(
            entry_point="run_git_repo.py",  # Pick your train script
            source_dir="./entry_points/",
            role=AWS_ROLE,
            instance_type=instance_type,
            instance_count=instance_count,
            hyperparameters={
                "git_uri": git_uri,
                "branch": branch,
                "git_project_dir": git_project_dir,
                "tracking_uri" : tracking_uri,
                "run_id": run_id,
                "parameters": json.dumps(parameters),
            },
            image_uri=image_uri,
            subnets=["subnet-039b4c3b8bb0e07cc"],
            security_group_ids=["sg-0c88ac15866099e54"],
            enable_network_isolation=False,
        )
        pytorch_processor.fit()

    else: # run in local enviroment
        ## git clone
        name_repo = os.path.basename(git_url).replace(".git", "")
        
        if not os.path.exists("./repos/" + name_repo):
            git.Repo.clone_from( url=git_uri, to_path="./repos/" + name_repo, branch=branch)

        ## execute project
        mlflow.set_tracking_uri(TRACKING_URI_AWS_GLOBAL)

        ## write text
        run = mlflow.run(
            uri=os.path.join("./repos/", git_project_dir),
            entry_point="main",
            backend="local",
            use_conda=False,
            run_id=run_id,
            parameters=parameters,
        )

def main():
    ###################################
    # 実行するmlflow projectのレポジトリを指定
    GIT_URL = "github.com/t-ibayashi-safie/takumi_project.git"
    # レポジトリ内のパスを指定
    BRANCH = "add_mlflow"
    ###################################

    # tracking_uri    = os.getenv(mlflow.tracking._TRACKING_URI_ENV_VAR, os.getenv("HOME") + "/mlruns/")
    experiment_name = os.getenv(mlflow.tracking._EXPERIMENT_NAME_ENV_VAR, "Default")
    git_id    = os.getenv("GIT_ID", "")
    git_token = os.getenv("GIT_TOKEN", "")
    if(git_id == "" or git_token == ""):
        print("error: git id or token is not defined")
        exit()

    mlflow.set_tracking_uri(TRACKING_URI_AWS_GLOBAL)
    mlflow.set_experiment(experiment_name)

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    artifact_location = experiment.artifact_location
    print("artifact_location: " + artifact_location)

    with mlflow.start_run(run_name="pipeline") as r_pipeline:
        with mlflow.start_run(run_name="step1", nested=True) as r1:
            git_project_dir = "takumi_project/MLflow/Mlflow-Project/sample_projects/01_write_file/echo"
            parameters = {
                "num": 2,
                "text": "Step1",
            }
            execute_git_repo(git_id, git_token, GIT_URL, BRANCH,  git_project_dir, r1.info.run_id, parameters=parameters, 
                             aws_flg=False, instance_type="local")
            downstream = os.path.join( artifact_location, r1.info.run_id, "artifacts/downstream/" )
        
        with mlflow.start_run(run_name="step2", nested=True) as r2:
            git_project_dir = "takumi_project/MLflow/Mlflow-Project/sample_projects/01_write_file/zip"
            parameters = {
                "upstream":downstream,
            }
            execute_git_repo( git_id, git_token, GIT_URL, BRANCH,  git_project_dir, r2.info.run_id, parameters=parameters, 
                              aws_flg=False, instance_type="local")

if __name__ == "__main__":
    main()