from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.data_organize import DataOrganize

from BoxOfficePrediction import logger

STAGE_NAME = 'DATA ORGANIZATION'

class DataOrganizePipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        data_organize_config = config.get_data_organize_config()
        data_organize = DataOrganize(config=data_organize_config)
        data_organize.merge_tables()
        data_organize.organise_numerical_features()
        data_organize.organise_temporial_features()
        data_organize.combine_ticket_price_table()
        data_organize.organise_categorical_features()
        data_organize.save_organized_data()


if __name__=='__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataOrganizePipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise e