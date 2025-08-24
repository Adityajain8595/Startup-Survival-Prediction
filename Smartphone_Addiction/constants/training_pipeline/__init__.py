import os
import sys
import numpy as np
import pandas as pd

TARGET_COLUMN="Addiction_Level"
PIPELINE_NAME: str = "Smartphone_Addiction"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "data.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

DATA_INGESTION_COLLECTION_NAME: str = "Smartphone_Addiction"
DATA_INGESTION_DATABASE_NAME: str = "Aditya"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.3

