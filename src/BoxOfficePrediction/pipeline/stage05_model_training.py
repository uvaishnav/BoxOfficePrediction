from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.model_training import ModelTraining

from BoxOfficePrediction import logger

STAGE_NAME = 'MODEL TRAINING'

class ModelTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        model_trainer_config = config.get_model_training_config()
        model_trainer = ModelTraining(config=model_trainer_config)
        model_trainer.initiate_training()

if __name__=='__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise e