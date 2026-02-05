import os
from torch.utils.data import DataLoader

from src.components.dataset import HelmetDataset
from src.components.transformation import DataTransformation


def collate_fn(batch):
    return tuple(zip(*batch))


def get_dataloader(train=True, batch_size=4):

    transform = DataTransformation(train=train)

    dataset = HelmetDataset(transform=transform)

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=train,
        num_workers=2,   # or start with 4
        pin_memory=True,              # faster GPU transfer
        persistent_workers=True, 
        collate_fn=collate_fn
    )

    return loader
