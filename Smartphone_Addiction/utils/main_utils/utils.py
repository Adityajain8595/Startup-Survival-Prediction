import yaml
from Smartphone_Addiction.exception.exception import SmartphoneAddictionException
from Smartphone_Addiction.logging.logger import logging
import os, sys, dill, pickle
import numpy as np

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            yaml_file = yaml.safe_load(file)
        return yaml_file
    except Exception as e:
        raise SmartphoneAddictionException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SmartphoneAddictionException(e, sys)
