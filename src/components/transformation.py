import albumentations as A 
from albumentations.pytorch import ToTensorV2
from src.utils.util import read_yaml
import os
from src.utils.logger import get_logger
logger = get_logger(__name__)
CONFIG_FILE_PATH =  os.path.join("config" , "config.yaml")
config = read_yaml(CONFIG_FILE_PATH)
class DataTransformation:
    def __init__(self , train = True ):
        trans_cfg = config['data_transformation']
        size = trans_cfg['image_size']
        mean = trans_cfg['mean']
        std = trans_cfg['std']

        aug = trans_cfg['augmentation']

        transforms = [A.Resize(size , size)]

        if train:
            if aug["horizontal_flip"]:
                transforms.append(A.HorizontalFlip(p=aug["flip_prob"]))

            if aug["brightness_contrast"]:
                transforms.append(A.RandomBrightnessContrast(p=aug["brightness_prob"]))

            if aug["blur"]:
                transforms.append(A.Blur(p=aug["blur_prob"]))

        transforms.extend([
            A.Normalize(mean=mean, std=std),
            ToTensorV2()
        ])

        self.transform = A.Compose(
            transforms , 
            bbox_params=A.BboxParams(
                format = trans_cfg['bbox_format'] ,
                label_fields=['labels']
            )
        )
        logger.info("Data transformation pipeline created ")
    
    def __call__(self, image , boxes , labels):
        
        transformed = self.transform(
            image = image , 
            bboxes = boxes , 
            labels = labels

        )

        return (
            transformed['image'],
            transformed['bboxes'] , 
            transformed['labels']
        )


  


            
        