import os
from src.utils.exception import CustomException
from src.cloud_blob.azure_blob import AzureBlob
import sys
from src.utils.logger import logging
from zipfile import ZipFile


class DataIngestion:

    def __init__(self , config):
        self.container_name = config['data_ingestion']['container_name']
        self.blob_name = config['data_ingestion']['blob_name']
        self.raw_data_dir = config['data_ingestion']['raw_data_dir']
        self.extract_dir = "data/raw_data"
        self.connection_string = os.getenv("CONNECTION_STRING") 
    
    def download_data_zip(self , azure_blob):
        try:
            logging.info("Starting data download from Azure Blob Storage.")
            azure_blob = AzureBlob(self.connection_string)
            azure_blob.download_from_azure(local_dir=self.extract_dir , container_name=self.container_name)
            logging.info("Data downloaded successfully from Azure Blob Storage.")
        except Exception as e:
            raise CustomException(e, sys)
    
    def extract_data_zip(self):
        try:
           
            logging.info("Starting data extraction.")
            with ZipFile(self.raw_data_dir, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
            logging.info("Data extracted successfully.")
        except Exception as e:
            logging.info("Data extracted Failed !!")
            raise CustomException(e, sys)
    
    def run(self):
        
        self.download_zip()
        self.extract_zip()



    

        