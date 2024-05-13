from BoxOfficePrediction import logger
from BoxOfficePrediction.pipeline.stage01_data_ingestion import DataIngestionPipeline
from BoxOfficePrediction.pipeline.stage02_data_organize import DataOrganizePipeline
from BoxOfficePrediction.pipeline.stage_data_validatioin import DataValidatioinPipeline
from BoxOfficePrediction.pipeline.stage03_feature_engineering import FeatureEngineeringPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = 'DATA ORGANIZATION'
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_organize = DataOrganizePipeline()
    data_organize.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e


STAGE_NAME = "DATA VALIDATION"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    data_validation = DataValidatioinPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e

STAGE_NAME = "FEATURE ENGINEERING"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    feature_engineer = FeatureEngineeringPipeline()
    feature_engineer.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    raise e