import os
import zipfile
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
import requests

from BoxOfficePrediction import logger
from BoxOfficePrediction.utils.common import get_size
from BoxOfficePrediction.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config

    def download_file(self)->str:
        # fetch data from kaggle
        try:
            logger.info("Downloading tmdb Dataset from kaggle")
            # Initialize Kaggle API
            api = KaggleApi()
            api.authenticate()

            # Specify the dataset you want to download
            dataset_name = self.config.dataset_name

            # Download dataset
            zip_download_dir = self.config.local_data_file
            api.dataset_download_files(dataset_name, path=zip_download_dir)

            logger.info(f"Downloaded data from {dataset_name} into file {zip_download_dir}")

            logger.info("Downloading ticket price data")

            if not os.path.exists(self.config.ticket_price_file):
                response = requests.get(self.config.ticket_price_dataset_link)
                with open(self.config.ticket_price_file, 'wb') as f:
                    f.write(response.content) 
                logger.info(f"Ticket price data downloaded to {self.config.ticket_price_file}")
            else:
                logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")


        except Exception as e:
            raise(e)
        
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        zip_data = os.listdir(self.config.local_data_file)
        logger.info("we have {} in {}".format(zip_data,self.config.local_data_file))
        zip_data_path = os.path.join(self.config.local_data_file, zip_data[0])

        with zipfile.ZipFile(zip_data_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)