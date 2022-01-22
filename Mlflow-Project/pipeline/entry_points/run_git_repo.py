## execute project in git repository
import argparse
import json
import os

import git
import mlflow

# execute
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--git_uri',  type=str, default="https://user:pass@path/to/repository")
    parser.add_argument('--branch', type=str, default="")
    parser.add_argument('--git_project_dir', type=str, default="")
    parser.add_argument('--tracking_uri',  type=str, default="")
    parser.add_argument('--run_id',  type=str, default="")
    parser.add_argument('--parameters',  type=str, default="")

    args = parser.parse_args()
    git_uri = args.git_uri
    branch  = args.branch
    git_project_dir = args.git_project_dir
    tracking_uri = args.tracking_uri
    run_id = args.run_id
    parameters = json.loads(args.parameters)
    print(args)

    ## git clone
    name_branch = os.path.basename(git_uri).replace(".git", "")
    git.Repo.clone_from( url=git_uri, to_path="./repos/" + name_branch, branch=branch)


    ## execute project
    mlflow.set_tracking_uri(tracking_uri)
    ## write text
    writeText_run = mlflow.run(
        uri=os.path.join("./repos/", git_project_dir),
        entry_point="main",
        backend="local",
        use_conda=False,
        run_id=run_id,
        parameters=parameters
    )

if __name__ == "__main__":
    main()