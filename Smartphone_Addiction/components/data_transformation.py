import sys, os, numpy as np, pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from Smartphone_Addiction.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from Smartphone_Addiction.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from Smartphone_Addiction.entity.config_entity import DataTransformationConfig
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
from Smartphone_Addiction.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SmartphoneAddictionException(e, sys) 
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Data read successfully from {file_path}")
            return df
        except Exception as e:
            logging.error(f"Error reading data from {file_path}: {e}")
            raise SmartphoneAddictionException(e, sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Remove unnecessary columns
            train_df.drop(columns=['Name'], inplace=True)
            test_df.drop(columns=['Name'], inplace=True)

            # Remove duplicates
            train_df.drop_duplicates(inplace=True)
            test_df.drop_duplicates(inplace=True)

            # Transformation using pipeline
            numerical_features = train_df.drop(columns=[TARGET_COLUMN]).select_dtypes(exclude=['object']).columns.tolist()
            categorical_features = train_df.drop(columns=[TARGET_COLUMN]).select_dtypes(include=['object']).columns.tolist()

            numerical_transformer = Pipeline(steps=[
                ('imputer', KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)),
                ('scaler', StandardScaler())
            ])

            categorical_transformer = Pipeline(steps=[
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            # Use ColumnTransformer to apply the transformers to the correct columns
            preprocessor = ColumnTransformer(
                transformers=[
                    ('numerical', numerical_transformer, numerical_features),
                    ('categorical', categorical_transformer, categorical_features)
            ])

            X_train = preprocessor.fit_transform(train_df.drop(columns=[TARGET_COLUMN]))
            y_train = train_df[TARGET_COLUMN]
            X_test = preprocessor.transform(test_df.drop(columns=[TARGET_COLUMN]))
            y_test = test_df[TARGET_COLUMN]

            # Combine the transformed features and target labels
            X_train = np.c_[X_train, np.array(y_train)]
            X_test = np.c_[X_test, np.array(y_test)]

            logging.info("Data Transformation completed")

            # save transformed data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, X_train)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, X_test)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)

            return DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
        except Exception as e:
            raise SmartphoneAddictionException(e, sys) 