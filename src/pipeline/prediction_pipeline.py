from PIL import Image
import torch
from src.utils.util import read_yaml
from src.utils.logger import get_logger
from src.utils.exception import CustomException
import os
CONFIG_FILE_PATH = os.path.join('config' , 'config.yaml')
config = read_yaml(CONFIG_FILE_PATH)
logger=get_logger(__name__)

class PredictionPipeline:
    def __init__(self):
        try : 
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self._load_model()
            self.class_map = config['dataset']['classes']
            self.inv_map = {v:k for k , v in self.class_map.items()}
            logger.info(f"Prediction pipeline initialized on {self.device}")
        except Exception as e :
            raise(CustomException(e))
    
    def _build_model(self):
        
        













        

