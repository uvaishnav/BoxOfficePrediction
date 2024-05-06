from BoxOfficePrediction.constants import *
from BoxOfficePrediction.utils.common import read_yaml, create_directories
from BoxOfficePrediction.entity.config_entity import DataIngestionConfig

class ConfugarationManager:
    def __init__(self,config_file_path = CONFIG_FILE_PATH, param_file_path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(param_file_path)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestioin_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir= config.root_dir,
            dataset_name= config.dataset_name,
            local_data_file= config.local_data_file,
            unzip_dir= config.unzip_dir
        )

        return data_ingestion_config