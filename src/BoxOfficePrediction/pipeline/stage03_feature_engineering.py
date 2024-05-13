from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.feature_engineering import FeatureEngineering

from BoxOfficePrediction import logger

STAGE_NAME = 'FEATURE ENGINEERING'

class FeatureEngineeringPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        feature_engineering_config = config.get_feature_engineering_config()
        feature_engineer = FeatureEngineering(config=feature_engineering_config)
        feature_engineer.get_table()
        feature_engineer.handle_missing_values()
        feature_engineer.get_weighted_vote()
        feature_engineer.get_footfall()
        feature_engineer.handle_list_categorical_features()
        feature_engineer.handle_normal_categorical_features()
        feature_engineer.handle_special_categorical_features()
        feature_engineer.save_test_train_data()

if __name__=='__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = FeatureEngineeringPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise e