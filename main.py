import os
from src.pipeline.download_file import run_kaggle_download

base_dir = os.path.dirname(os.path.abspath(__file__))

dataset_name = "jacopoferretti/expedia-travel-dataset"
expected_file = "travel.csv"

def main():
    run_kaggle_download(base_dir, dataset_name, expected_file)


if __name__ == "__main__":
    main()