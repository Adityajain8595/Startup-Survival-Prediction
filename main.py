from Smartphone_Addiction.components.data_ingestion import DataIngestion
from Smartphone_Addiction.components.data_validation import DataValidation
from Smartphone_Addiction.components.data_transformation import DataTransformation
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
from Smartphone_Addiction.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
import sys

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion completed")
        print(data_ingestion_artifact)
        
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise SmartphoneAddictionException(e, sys)
