from Smartphone_Addiction.components.data_ingestion import DataIngestion
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
from Smartphone_Addiction.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion initiated")
        print(data_ingestion_artifact)
    except Exception as e:
        raise SmartphoneAddictionException(e, sys)
