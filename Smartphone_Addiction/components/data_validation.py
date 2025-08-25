from Smartphone_Addiction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Smartphone_Addiction.entity.config_entity import DataValidationConfig
from Smartphone_Addiction.constants.training_pipeline import SCHEMA_FILE_PATH
from Smartphone_Addiction.utils.main_utils.utils import read_yaml_file, write_yaml_file
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os, sys, yaml

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)

    def validate_data(self, df: pd.DataFrame) -> bool:
        try:
            # Check for missing values
            if df.isnull().sum().sum() > 0:
                logging.warning("Missing values found in the dataframe.")
                return False
            
            # Check for duplicate values
            if df.duplicated().sum() > 0:
                logging.warning("Duplicate values found in the dataframe.")
                return False

            # Check for schema validation
            for column in self.schema['schema']['columns'].keys():
                if column not in df.columns:
                    logging.warning(f"Column '{column}' is missing from the dataframe.")
                    return False

            # Validate columns and their data types
            DTYPE_MAPPING = {
                "integer": "int64",
                "float": "float64",
                "string": "object",
                "categorical": "object"
            }
            for column, column_details in self.schema['schema']['columns'].items():
                # Check if the column exists in the DataFrame
                if column not in df.columns:
                    logging.warning(f"Column '{column}' is missing from the dataframe.")
                    return False
                
                # Check for correct data types based on the DTYPE_MAPPING
                schema_dtype = column_details.get('dtype')
                if schema_dtype:
                    expected_pandas_dtype = DTYPE_MAPPING.get(schema_dtype)
                    if expected_pandas_dtype and str(df[column].dtype) != expected_pandas_dtype:
                        logging.warning(f"Column '{column}' has type {df[column].dtype} but expected {expected_pandas_dtype}.")
                        return False

            logging.info("Data validation passed.")
            return True
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)
        
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column: {
                    "drift_status": is_found,
                    "pvalue": float(is_same_dist.pvalue)
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report)
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read the data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validate the data
            is_train_valid = self.validate_data(train_df)
            if not is_train_valid:
                logging.warning("Training data validation failed.")
            is_test_valid = self.validate_data(test_df)
            if not is_test_valid:
                logging.warning("Testing data validation failed.")

            # Check for data drift
            status = self.detect_data_drift(train_df, test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Create and return the DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)
