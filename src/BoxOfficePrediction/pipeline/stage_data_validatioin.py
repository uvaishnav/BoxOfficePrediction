from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.data_validation import DataVerification

from BoxOfficePrediction import logger

STAGE_NAME = "DATA VALIDATION"

class DataValidatioinPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        data_validation_config = config.get_data_validation_config()
        data_validate = DataVerification(config=data_validation_config)
        data_validate.validate_csv()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidatioinPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise e