from src.components.ingestion import DataIngestion
from src.components.validation import DataValidation
from src.components.model_trainer import ModelTrainer
data_ingestion = DataIngestion()
data_validation = DataValidation()
model_trainer = ModelTrainer()
def run_pipeline():
    data_ingestion.run()
    data_validation.run_validation()
    model_trainer.train()

run_pipeline()


    