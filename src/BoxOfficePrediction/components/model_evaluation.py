import os
import joblib
from pathlib import Path

import pandas as pd
import numpy as np

import mlflow
import mlflow.sklearn
from urllib.parse import urlparse

from sklearn.metrics import mean_squared_error

from BoxOfficePrediction.entity.config_entity import ModelEvaluationConfig
from BoxOfficePrediction.utils.common import read_yaml
from BoxOfficePrediction import logger


class ModelEvaluation:
    def __init__(self,config:ModelEvaluationConfig) -> None:
        self.config = config

        self.models = [
            ('RandomForest', joblib.load(self.config.RandomForest)),
            ('AdaBoost',joblib.load(self.config.Adaboost)),
            ('CatBoost',joblib.load(self.config.CatBoost)),
            ('DecisionTree',joblib.load(self.config.DscisionTree)),
            ('GradientBoosting',joblib.load(self.config.GradientBoosting)),
            ('LinearRegression',joblib.load(self.config.LinearRegression)),
            ('XGBoost',joblib.load(self.config.XGBoost))
        ]

        self.best_params = read_yaml(Path(self.config.best_params_path))

    def get_test_data(self):
        test_data = pd.read_csv(self.config.test_data)

        logger.info("loaded test Data")

        # Seperating Target Column from INput Features
        input_feature_test_df = test_data.drop([self.config.target_column],axis=1)
        target_feature_test_df = np.log(test_data[self.config.target_column])

        """
        Applied log normal transformation for target column as there are outlier in it and the data is skewed.
        preprocessor object is for input columns only not for target column.
        So we apply log normal transformation explicitly.
        """

        logger.info("Split target column complete")

        logger.info("Obtaining Preprocessor Object")

        preprocessor_obj = joblib.load(self.config.preprocessor_path)

        logger.info("preprocessing the test dataframe")

        input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

        logger.info("Test input is preprocessed")

        return (
            input_feature_test_arr,
            np.array(target_feature_test_df)
        )
    
    def log_model_into_ml_flow(self,model,model_name,metrics):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            rmse, neg_mse = metrics

            mlflow.log_params(self.best_params[model_name])

            mlflow.log_metric("rmse",rmse)
            mlflow.log_metric("neg_mse",neg_mse)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                logger.info("Regestiring {} to mlflow".format(model_name))
                mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)
            else:
                mlflow.sklearn.log_model(model, "model")
                logger.info("Unable to regestitor model to mlflow")

    
    def initiate_evaluation(self):
        x_test, y_test = self.get_test_data()

        for model_name, model in self.models:
            y_pred = model.predict(x_test)

            mse = mean_squared_error(y_true=y_test,y_pred=y_pred)
            rmse = np.sqrt(mse)
            neg_mse = -mean_squared_error(y_true=y_test, y_pred=y_pred)

            logger.info("RMSE of {} is {}".format(model_name,rmse))
            logger.info("neg_mse of {} is {}".format(model_name,neg_mse))

            self.log_model_into_ml_flow(model=model,model_name=model_name,metrics=(rmse,neg_mse))






