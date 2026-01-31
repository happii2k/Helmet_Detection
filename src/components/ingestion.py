import os
import sys
from zipfile import ZipFile

from src.utils.exception import CustomException
from src.cloud.azure_blob import AzureBlob
from src.utils.logger import logging
from src.utils.util import read_yaml
CONFIG_FILE_PATH = os.path.join("config", "config.yaml")

config = read_yaml(CONFIG_FILE_PATH)
from dotenv import load_dotenv
load_dotenv()


class DataIngestion:

    def __init__(self):
        self.container_name = config['data_ingestion']['container_name']
        self.blob_name = config['data_ingestion']['blob_name']
        self.raw_data_dir = config['data_ingestion']['raw_data_dir']   # zip file path
        self.extract_dir = config['data_ingestion']['extract_dir']     # folder path
        self.connection_string = os.getenv("CONNECTION_STRING")

    def download_data_zip(self):
        try:
            logging.info("Starting data download from Azure Blob Storage")

            azure_blob = AzureBlob(self.connection_string)

            azure_blob.download_from_azure(
                local_dir=self.raw_data_dir,
                container_name=self.container_name
                
            )

            logging.info("Download completed successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def extract_data_zip(self):
        try:
            logging.info("Starting zip extraction")

            os.makedirs(self.extract_dir, exist_ok=True)

            with ZipFile(os.path.join(self.raw_data_dir, self.blob_name), 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)

            logging.info("Extraction completed successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def run(self):
        self.download_data_zip()
        self.extract_data_zip()


if __name__ == "__main__":


    ingestion = DataIngestion()
    ingestion.run()
