import os
import torch   
import cv2 
import xml.etree.ElementTree as ET 
from src.utils.util import read_yaml
CONFIG_FILE_PATH  = os.path.join("config" , "config.yaml")
config = read_yaml(CONFIG_FILE_PATH)
class HelmetDataset(torch.utils.data.Dataset):

    def __init__(self , images_dir , annotation_dir , transform = None , class_map = None):
        self.images_dir = config["dataset"]["images_dir"]
        self.annotations_dir = config["dataset"]["annotations_dir"]
        self.class_map = config["dataset"]["classes"]
        self.transform = transform

        self.annotations_file = [
            f for f in os.listdir(self.annotations_dir) if f.endswith(".xml")
        ]
    
    def __len__(self):
        return len(self.annotations_file)
    
    def __getitem__(self, index):
        xml_file = self.annotations_file[index]
        xml_path = os.path.join(self.annotations_dir , xml_file)

        tree = ET.parse(xml_path)
        root = tree.getroot()

        image_name = root.find("filename").text
        img_path = os.path.join(self.images_dir , image_name)

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)

        boxes = []
        labels = []

        for obj in root.findall('object'):
            label_name = obj.find('name').text
            bbox = obj.find('bndbox')

            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            boxes.append([xmin , ymin , xmax , ymax])
            labels.append(self.class_map[label_name])
        
        boxes = torch.tensor(boxes , dtype=torch.float32)
        labels = torch.tensor(labels , dtype=torch.int64)

        target = {
            "boxes" : boxes,
            "labels" : labels
        }
        if self.transform:
            image , boxes , labels = self.transform(
                image , 
                boxes.tolist(),
                labels.tolist()
            )
            target["boxes"] = torch.tensor(boxes, dtype=torch.float32)
            target["labels"] = torch.tensor(labels, dtype=torch.int64)
        return image , target





        
        