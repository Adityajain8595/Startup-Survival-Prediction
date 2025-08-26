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

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SmartphoneAddictionException(e, sys)
    
def save_object(file_path: str, obj: object):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise SmartphoneAddictionException(e,sys)
