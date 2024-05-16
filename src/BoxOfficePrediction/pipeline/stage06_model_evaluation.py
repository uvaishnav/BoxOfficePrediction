from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.model_evaluation import ModelEvaluation

from BoxOfficePrediction import logger

class ModelEvaluationPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluator = ModelEvaluation(config=model_evaluation_config)
        model_evaluator.initiate_evaluation()

STAGE_NAME = 'MODEL EVALUATION'

if __name__=='__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        raise e