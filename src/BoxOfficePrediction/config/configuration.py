from BoxOfficePrediction.constants import *
from BoxOfficePrediction.utils.common import read_yaml, create_directories
from BoxOfficePrediction.entity.config_entity import (DataIngestionConfig,
                                                      DataOrganizeConfig,
                                                      DataValidatioinConfig,
                                                      FeatureEngineeringConfig,
                                                      DataPreprocessorConfig,
                                                      ModelTrainingConfig,
                                                      ModelEvaluationConfig,
                                                      PredictPipelineConfig)
                                                      

class ConfugarationManager:
    def __init__(self,config_file_path = CONFIG_FILE_PATH, param_file_path = PARAMS_FILE_PATH, schema_file_path = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(param_file_path)
        self.schema = read_yaml(schema_file_path)


        create_directories([self.config.artifacts_root])
    
    def get_data_ingestioin_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir= config.root_dir,
            dataset_name= config.dataset_name,
            ticket_price_dataset_link = config.ticket_price_dataset_link,
            ticket_price_file = config.ticket_price_file,
            local_data_file= config.local_data_file,
            unzip_dir= config.unzip_dir
        )

        return data_ingestion_config
    
    def get_data_organize_config(self)->DataOrganizeConfig:
        config = self.config.data_organize

        create_directories([config.org_table_path])

        data_organize_config = DataOrganizeConfig(
            movie_table_path = config.movie_table_path,
            credit_table_path = config.credit_table_path,
            ticket_price_table_path = config.ticket_price_table_path,
            org_table_path = config.org_table_path
        )

        return data_organize_config
    
    def get_data_validation_config(self)->DataValidatioinConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidatioinConfig(
            root_dir = config.root_dir,
            val_data_path = config.val_data_path,
            all_schema = self.schema.COLUMNS,
            status_file = config.status_file
        )

        return data_validation_config
    
    def get_feature_engineering_config(self)->FeatureEngineeringConfig:
        config = self.config.feature_engineering

        create_directories([config.scores_data])

        feature_engineering_config = FeatureEngineeringConfig(
            organized_data = config.organized_data,
            featured_data = config.featured_data,
            scores_data = config.scores_data
        )

        return feature_engineering_config
    
    def get_data_preprocessor_config(self)->DataPreprocessorConfig:
        config = self.config.data_preprocessing

        create_directories([config.root_dir])

        data_preprocessor_config = DataPreprocessorConfig(
            root_dir= config.root_dir
        )

        return data_preprocessor_config
    
    def get_model_training_config(self)->ModelTrainingConfig:
        config = self.config.model_training

        model_training_config = ModelTrainingConfig (
            train_data = config.train_data,
            preprocessor_path = config.preprocessor_path,
            model_path = config.model_path,
            n_iter = self.params.n_iter,
            scoring = self.params.scoring,
            cv = self.params.cv,
            target_column = self.params.target_column
        )

        return model_training_config
    
    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        config = self.config.model_evaluation

        model_evaluation_config = ModelEvaluationConfig(
            test_data = config.test_data,
            target_column = self.params.target_column,
            preprocessor_path = config.preprocessor_path,
            best_params_path = config.best_params_path,
            Adaboost = config.Adaboost,
            CatBoost = config.CatBoost,
            DscisionTree = config.DscisionTree,
            GradientBoosting = config.GradientBoosting,
            LinearRegression = config.LinearRegression,
            RandomForest = config.RandomForest,
            XGBoost = config.XGBoost,
            mlflow_uri = config.mlflow_uri
        )

        return model_evaluation_config
    
    def get_prediction_pipeline_config(self)->PredictPipelineConfig:
        config = self.config.prediction_pipeline

        prediction_pipeline_config = PredictPipelineConfig(
            preprocessor_path = config.preprocessor_path,
            model_path= config.model_path
        )
        return prediction_pipeline_config
    
