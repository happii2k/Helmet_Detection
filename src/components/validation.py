import os
import xml.etree.ElementTree as ET
from PIL import Image
import sys
from pathlib import Path
from src.utils.exception import CustomException
from src.utils.logger import get_logger
from src.utils.util import read_yaml

CONFIG_FILE_PATH = os.path.join("config", "config.yaml")
config = read_yaml(CONFIG_FILE_PATH)

logger = get_logger(__name__)

class DataValidation:

    def __init__(self):
        self.annotation_dir = config['data_validation']['annotations_dir']
        self.images_dir = config['data_validation']['images_dir']
        self.required_classes = config['data_validation']['required_classes']

    def validate(self):
        try:
            logger.info("Starting data validation process")

            # Ensure annotation and image directories exist
            if not os.path.exists(self.annotation_dir):
                logger.error(f"Annotations directory not found: {self.annotation_dir}")
                raise CustomException(f"Annotations directory not found: {self.annotation_dir}. Please run ingestion or fix `config/config.yaml`", sys)

            if not os.path.exists(self.images_dir):
                logger.error(f"Images directory not found: {self.images_dir}")
                raise CustomException(f"Images directory not found: {self.images_dir}. Please run ingestion or fix `config/config.yaml`", sys)

            annotation_files = [
                f for f in os.listdir(self.annotation_dir) if f.endswith(".xml")
            ]

            bad_files = []

            for file in annotation_files:
                xml_path = os.path.join(self.annotation_dir, file)

                tree = ET.parse(xml_path)
                root = tree.getroot()

                img_name = root.find("filename").text
                img_path = os.path.join(self.images_dir, img_name)

                # ✅ Check image exists
                if not os.path.exists(img_path):
                    logger.warning(f"Missing image: {img_name}")
                    bad_files.append(file)
                    continue

                img = Image.open(img_path)
                width, height = img.size

                objects = root.findall("object")

                if len(objects) == 0:
                    logger.warning(f"No objects in {file}")
                    bad_files.append(file)
                    continue

                for obj in objects:
                    class_name = obj.find("name").text

                    if class_name not in self.required_classes:
                        logger.warning(f"Invalid class {class_name} in {file}")
                        bad_files.append(file)
                        continue

                    bbox = obj.find("bndbox")

                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)

                    if xmin < 0 or ymin < 0 or xmax > width or ymax > height:
                        logger.warning(f"Invalid bbox in {file}")
                        bad_files.append(file)
                        break

            logger.info(f"Validation complete. Bad files found: {len(bad_files)}")

            return bad_files

        except Exception as e:
            logger.error("Error during validation")
            raise CustomException(e, sys)
    def remove_bad_files(self, bad_files):
        try:
            logger.info("Starting removal of bad files")

            for file in bad_files:
                xml_path = os.path.join(self.annotation_dir, file)

                tree = ET.parse(xml_path)
                root = tree.getroot()

                img_name = root.find("filename").text
                img_path = os.path.join(self.images_dir, img_name)

                if os.path.exists(img_path):
                    os.remove(img_path)
                    logger.info(f"Removed image: {img_name}")

                os.remove(xml_path)
                logger.info(f"Removed annotation: {file}")

            logger.info("Removal of bad files complete")

        except Exception as e:
            logger.error("Error during removal of bad files")
            raise CustomException(e, sys)
    
    def run_validation(self):
        bad_files = self.validate()
        if bad_files:
            self.remove_bad_files(bad_files)
        else:
            logger.info("No bad files to remove.")


if __name__ == "__main__":
    validator = DataValidation()
    bad = validator.run_validation()
