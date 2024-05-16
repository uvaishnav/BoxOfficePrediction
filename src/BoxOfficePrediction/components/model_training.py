import os
from pathlib import Path
import joblib
import pickle
import yaml

import pandas as pd
import numpy as np

from BoxOfficePrediction.constants import *
from BoxOfficePrediction.entity.config_entity import ModelTrainingConfig
from BoxOfficePrediction.pipeline.stage04_data_preprocessing import DataPreprocessorPipeline
from BoxOfficePrediction import logger

## Importing nesessary models
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.model_selection import RandomizedSearchCV


class ModelTraining:
    def __init__(self,config:ModelTrainingConfig) -> None:
        self.config = config
        self.estimators =[
            ("RandomForest", RandomForestRegressor()),
            ("DecisionTree", DecisionTreeRegressor()),
            ("GradientBoosting", GradientBoostingRegressor()),
            ("LinearRegression", LinearRegression()),
            ("XGBoost", XGBRegressor()),
            ("CatBoost", CatBoostRegressor()),
            ("AdaBoost", AdaBoostRegressor())
        ]
        self.params_dict = {
            'RandomForest' : {
                "n_estimators": range(100, 1000),
                "max_depth": range(3, 10),
                "min_samples_split": range(2, 20),
                "min_samples_leaf": range(1, 10)
            },
            'DecisionTree' : {
                "max_depth": range(3, 10),
                "min_samples_split": range(2, 20),
                "min_samples_leaf": range(1, 10)
            },
            'GradientBoosting' : {
                "n_estimators": range(100, 1000),
                "learning_rate": np.arange(0.01, 1.0, 0.1),
                "max_depth": range(3, 10)
            },
            'LinearRegression' : {
                "fit_intercept": [True, False]
            },
            'XGBoost' : {
                "n_estimators": range(100, 1000),
                "learning_rate": np.arange(0.01, 1.0, 0.1),
                "max_depth": range(3, 10),
                "colsample_bytree": np.arange(0.1, 1.0, 0.1)
            },
            'CatBoost' : {
                "iterations": range(100, 1000),
                "learning_rate": np.arange(0.01, 1.0, 0.1),
                "depth": range(3, 10)
            },
            'AdaBoost' : {
                "n_estimators": range(100, 1000),
                "learning_rate": np.arange(0.01, 1.0, 0.1)
            }

        }
    
    @staticmethod
    def get_preprocessor_object():
        get_preprocessor = DataPreprocessorPipeline()
        preprocessor_obj = get_preprocessor.main()
        return preprocessor_obj
    
    def write_params_to_yaml(self, model_name, best_params):
        # Define the method to write best parameters to a YAML file here
        params_file_path = os.path.join(self.config.model_path, 'best_params.yaml')
        # Load existing parameters if the file exists
        if os.path.exists(params_file_path):
            with open(params_file_path, 'r') as f:
                existing_params = yaml.safe_load(f)
        else:
            existing_params = {}

        # Convert numpy objects to native Python objects
        best_params_converted = {}
        for key, value in best_params.items():
            if isinstance(value, np.generic):
                # Convert numpy scalar to Python scalar
                best_params_converted[key] = value.item()
            elif isinstance(value, np.ndarray):
                # Convert numpy array to Python list
                best_params_converted[key] = value.tolist()
            else:
                best_params_converted[key] = value

        # Update the existing parameters with the new best parameters
        existing_params[model_name] = best_params_converted

        # Write the updated parameters to the YAML file
        with open(params_file_path, 'w') as f:
            yaml.dump(existing_params, f, default_flow_style=False)



    def get_train_data(self):
        train_data = pd.read_csv(self.config.train_data)

        logger.info("loaded test and train data")

        # Seperating Target Column from INput Features
        input_feature_train_df = train_data.drop([self.config.target_column],axis=1)
        target_feature_train_df = np.log(train_data[self.config.target_column])     

        """
        Applied log normal transformation for target column as there are outlier in it and the data is skewed.
        preprocessor object is for input columns only not for target column.
        So we apply log normal transformation explicitly.
        """

        logger.info("Split target column complete")

        logger.info("Obtaining Preprocessor Object")

        preprocessor_obj = ModelTraining.get_preprocessor_object()

        logger.info("Preprocessing the Training and testing dataframes")

        input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)

        logger.info(input_feature_train_arr.shape)

        logger.info("Saving Preprocessor Object as pkl file")
        joblib.dump(preprocessor_obj,self.config.preprocessor_path)

        return (
            input_feature_train_arr,
            np.array(target_feature_train_df),
        )
    
    def initiate_training(self):

        x_train,y_train = self.get_train_data()

        x_train_nan = np.isnan(x_train).any()
        y_train_nan = np.isnan(y_train).any()

        logger.info("Train data has NaN values : {}".format(x_train_nan))
        logger.info("Trauin target has NaN value : {} ".format(y_train_nan))

        x_train_inf = np.isinf(x_train).any()
        y_train_inf = np.isinf(y_train).any()

        logger.info("Train data has inf values : {}".format(x_train_inf))
        logger.info("Trauin target has inf value : {} ".format(y_train_inf))

        # Perform Randomized SearchCV for each estimator and save the best model
        logger.info("Initiated randomized SearchCV for each model")

        for name, estimator in self.estimators:
            random_search = RandomizedSearchCV(estimator=estimator,param_distributions=self.params_dict[name],n_iter=self.config.n_iter,scoring=self.config.scoring,cv=self.config.cv)
            logger.info("Initiated randomized SearchCV for {} model".format(name))
            random_search.fit(x_train,y_train)

            # Get the best model score
            best_score = random_search.best_score_

            logger.info(f"Found best model for {name} model with a negMSE of {best_score:.4f}")

            # Save the best model for each algorithm
            model_path = os.path.join(self.config.model_path,f"{name}_model.pkl")
            with open(model_path, "wb") as f:
                pickle.dump(random_search.best_estimator_, f)

            logger.info("Saved best model of {}".format(name))

            # Extract best parameters and convert to a dictionary
            best_params = {key: value for key, value in random_search.best_params_.items()}

            self.write_params_to_yaml(name,best_params)

            logger.info(f"{name} best parameters: {best_params}")





