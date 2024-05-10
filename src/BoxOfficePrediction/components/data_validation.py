import os
from pathlib import Path
import pandas as pd

from BoxOfficePrediction.entity.config_entity import DataValidatioinConfig

class DataVerification:
    def __init__(self,config:DataValidatioinConfig) -> None:
        self.config = config
    
    def validate_csv(self):
        try:
            cinema_db = pd.read_csv(self.config.val_data_path)

            schema = self.config.all_schema

            # Open the status.txt file for writing
            with open(self.config.status_file,'w') as status_file:

                # Check for unexpected columns
                unexpected_columns = [col for col in cinema_db.columns if col not in schema.keys()]
                if unexpected_columns:
                    status_file.write(f"Unexpected columns found: {unexpected_columns}\n")
                    return False
                
                # Verify expected columns and data types
                for column_name, expected_datatype in schema.items():
                    if column_name not in cinema_db.columns:
                        status_file.write(f"Column '{column_name}' is missing.\n")
                        return False
                    if cinema_db[column_name].dtype != expected_datatype:
                        status_file.write(f"Data type mismatch for column '{column_name}'. "f"Expected: {expected_datatype}, Actual: {cinema_db[column_name].dtype}\n")
                        return False
                
                status_file.write("Verification successful. All columns and data types match the schema.\n")
                return True

        except Exception as e:
            raise e