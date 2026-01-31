from src.utils.exception import CustomException
from src.utils.logger import logging
import os
import sys
import yaml
from pathlib import Path

def read_yaml(file_path: Path) -> dict:
    try:
        logging.info(f"Reading YAML file from: {file_path}")
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        logging.info(f"Successfully read YAML file from: {file_path}")
        
        return content
    
    
    except Exception as e:
        logging.error(f"Error reading YAML file from: {file_path} - {e}")
        raise CustomException(e, sys)