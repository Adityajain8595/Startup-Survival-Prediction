import os
import sys
import json
from pymongo import MongoClient
import certifi
import pandas as pd
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class AddictionDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)

    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise SmartphoneAddictionException(e, sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            
            self.mongo_client=MongoClient(uri)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise SmartphoneAddictionException(e,sys)
            
if __name__ == "__main__":
    FILE_PATH="data/smartphone_addiction_data.csv"
    DATABASE="Aditya"
    COLLECTION="Smartphone_Addiction"

    startup_obj=AddictionDataExtract()
    records=startup_obj.csv_to_json_converter(FILE_PATH)
    num_records = startup_obj.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(f"Number of records inserted: {num_records}")

            

