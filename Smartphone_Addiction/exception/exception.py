import sys
from Smartphone_Addiction.logging import logger
class SmartphoneAddictionException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in file: {self.filename} at line: {self.lineno} with message: {str(self.error_message)}"
    
if __name__ == "__main__":
    try:
        logger.logging.info("Logging has started")
    except Exception as e:
        raise SmartphoneAddictionException(e,sys)