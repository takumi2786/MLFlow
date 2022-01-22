"""
入力フォルダ内の message.txt を読み込み、テキストを追記する。
"""


import os
import argparse

import mlflow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--upstream",
        type=str,
        default="",
    )
    parser.add_argument(
        "--num",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--text",
        type=str,
        default="hello",
    )
    args = parser.parse_args()
    upstream = args.upstream
    num = args.num
    text = args.text
    print(args)

    # load downstream
    with open(os.path.join(upstream, "message.txt"), 'a') as f:
        for i in range(0, num):
            f.write(text + "\n")

    # save downstream
    mlflow.log_param("num", num)
    mlflow.log_artifact(os.path.join(upstream, "message.txt"), "downstream")


if __name__ == "__main__":
    main()