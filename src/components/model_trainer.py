import os
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from src.data.data_loader import get_data_loader
from src.utils.util import read_yaml
from src.utils.logger import get_logger

CONFIG_FILE_PATH = os.path.join("config", "config.yaml")
config = read_yaml(CONFIG_FILE_PATH)

logger = get_logger(__name__)


class ModelTrainer:

    def __init__(self):
        trainer_cfg = config["model_trainer"]

        self.epochs = trainer_cfg["training"]["epochs"]
        self.lr = trainer_cfg["training"]["learning_rate"]
        self.batch_size = trainer_cfg["training"]["batch_size"]

        self.num_classes = trainer_cfg["model"]["num_classes"]

        self.model_path = os.path.join(
            trainer_cfg["output"]["model_dir"],
            trainer_cfg["output"]["model_name"]
        )

    def build_model(self):

        model = fasterrcnn_resnet50_fpn(weights="DEFAULT")

        in_features = model.roi_heads.box_predictor.cls_score.in_features

        model.roi_heads.box_predictor = FastRCNNPredictor(
            in_features,
            self.num_classes
        )

        return model

    def train(self):

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")

        model = self.build_model().to(device)

        train_loader = get_data_loader(
            batch_size=self.batch_size,
            train=True,
            shuffle=True
        )

        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=self.lr,
            momentum=0.9,
            weight_decay=0.0005
        )

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        for epoch in range(self.epochs):

            model.train()
            epoch_loss = 0

            for images, targets in train_loader:

                images = [img.to(device) for img in images]
                targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

                loss_dict = model(images, targets)
                loss = sum(loss for loss in loss_dict.values())

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()

            avg_loss = epoch_loss / len(train_loader)

            logger.info(f"Epoch {epoch+1}/{self.epochs} | Loss: {avg_loss:.4f}")

        torch.save(model.state_dict(), self.model_path)

        logger.info(f"Model saved at {self.model_path}")
