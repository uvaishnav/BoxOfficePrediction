from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction.components.data_preprocessor import DataPreprocessing


STAGE_NAME = 'GET PREPROCSSING OBJECT'

class DataPreprocessorPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        config = ConfugarationManager()
        data_preprocessor_config = config.get_data_preprocessor_config()
        data_preprocessor = DataPreprocessing(config=data_preprocessor_config)
        preprocessor = data_preprocessor.get_data_preprocessor_object()
        return preprocessor

# if __name__=='__main__':
#     try:
#         logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
#         obj = DataPreprocessorPipeline()
#         obj.main()
#         logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         raise e