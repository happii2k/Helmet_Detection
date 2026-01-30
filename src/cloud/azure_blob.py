from azure.storage.blob import BlobServiceClient
from src.utils.exception import CustomException
from src.utils.logger import get_logger
import sys
import os

logger = get_logger(__name__)

class AzureBlob:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

    def download_from_azure(self, local_dir, container_name):
        try:
            logger.info("Initiating download from Azure Blob Storage.")

            container_client = self.blob_service_client.get_container_client(
                container_name
            )

            os.makedirs(local_dir, exist_ok=True)

            for blob in container_client.list_blobs():
                local_file_path = os.path.join(local_dir, blob.name)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                logger.info(f"Downloading {blob.name}")

                data = container_client.download_blob(blob.name).readall()
                with open(local_file_path, "wb") as f:
                    f.write(data)

            logger.info("Download completed successfully.")

        except Exception as e:
            logger.error("Error occurred while downloading from Azure Blob Storage.")
            raise CustomException(e, sys)
