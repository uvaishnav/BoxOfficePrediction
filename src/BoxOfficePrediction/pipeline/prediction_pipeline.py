import pandas as pd
import joblib

from BoxOfficePrediction.config.configuration import ConfugarationManager
from BoxOfficePrediction import logger

class PredictPipeline:
    def __init__(self) -> None:
        config = ConfugarationManager()
        self.prediction_config = config.get_prediction_pipeline_config()


    def predict(self,features):
        try:
            preprocessor_path = self.prediction_config.preprocessor_path
            preprocessor_obj = joblib.load(preprocessor_path)

            logger.info("Preprocessor loaded for prediction")

            model_path = self.prediction_config.model_path
            model = joblib.load(model_path)

            logger.info("model loaded for prediction")

            data_scaled = preprocessor_obj.transform(features)
            prediction = model.predict(data_scaled)

            return prediction




        except Exception as e:
            raise(e)


class CustomData:
    def __init__(
            self,
            budget:int,
            runtime : int,
            crew : str,
            hero : str,
            heroine : str,
            release_month : str,
            production_countries : str,
            spoken_languages : str,
            genres : list
    ):
        self.budget = budget
        self.runtime = runtime
        self.crew = crew
        self.hero = hero
        self.heroine = heroine
        self.release_month = release_month
        self.production_countries = production_countries
        self.spoken_languages = spoken_languages
        self.genres = genres

    def get_data_as_dataframe(self):
        try:
            custom_input_df = {
                'budget' : [self.budget],
                'runtime' : [self.runtime],
                'crew' : [self.crew],
                'hero' : [self.hero],
                'heroine' : [self.heroine],
                'release_month' : [self.release_month],
                'production_countries' : [self.production_countries],
                'spoken_languages' : [self.spoken_languages],
                'genres' : [self.genres]
            }

            return pd.DataFrame(custom_input_df)
        
        except Exception as e:
            raise(e)