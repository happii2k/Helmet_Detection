from PIL import Image
import torch
import numpy as np
from src.utils.util import read_yaml
from src.utils.logger import get_logger
from src.utils.exception import CustomException
import os
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from src.components.transformation import DataTransformation
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
        num_classes = config['model_trainer']['model']['num_classes']
        model = fasterrcnn_resnet50_fpn(
                    weights=None,
                    weights_backbone=None
                )

        in_features = model.roi_heads.box_predictor.cls_score.in_features
        model.roi_heads.box_predictor = FastRCNNPredictor(
            in_features , num_classes
        )

        return model
    
    def _load_model(self):
        model = self._build_model()
        model_path = os.path.join(
            config['model_trainer']['output']['model_dir'] , 
            config['model_trainer']['output']['model_name']
        )
        model.load_state_dict(
            torch.load(model_path , map_location=self.device)
        )
        model.to(self.device)
        model.eval()

        logger.info(f"Model loaded from {model_path}")

        return model
    


    def predict(self, image: Image.Image, conf_threshold=0.3):   # lower first for testing

        try:
            transform = DataTransformation(train=False)

            img_np = np.array(image)

            # fake empty boxes just to pass albumentations safely
            boxes = []
            labels = []

            img_tensor, _, _ = transform(img_np, boxes, labels)

            img_tensor = img_tensor.unsqueeze(0).to(self.device)

            with torch.no_grad():
                output = self.model(img_tensor)[0]

            results = []

            for box, score, label in zip(
                output["boxes"].cpu().numpy(),
                output["scores"].cpu().numpy(),
                output["labels"].cpu().numpy()
            ):
                if score < conf_threshold:
                    continue

                results.append({
                    "class": self.inv_map[label],
                    "confidence": float(score),
                    "box": [float(x) for x in box]
                })

            return results

        except Exception as e:
            raise CustomException(e)
