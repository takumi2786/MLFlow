"""
入力フォルダ内の ファイル を読み込み、zip化する.
"""


import os
import argparse
import zipfile
import glob


import mlflow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--upstream",
        type=str,
        default="",
    )

    args = parser.parse_args()
    upstream = args.upstream
    print(args)

    # tempフォルダを作成
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")

    # zip化する
    with zipfile.ZipFile("./tmp/data.zip", 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        file_paths = glob.glob(os.path.join(upstream, "*"))
        for file_path in file_paths:
            arcname = file_path.replace(upstream, "")
            zip_file.write(file_path, arcname=arcname)

    # save result
    mlflow.log_artifact("./tmp/data.zip", "downstream")

if __name__ == "__main__":
    main()