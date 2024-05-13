import os
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,LabelEncoder,StandardScaler,FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin


from BoxOfficePrediction.entity.config_entity import DataPreprocessorConfig
from BoxOfficePrediction import logger

import joblib


# Custom transformer for getting scores from CSV files

class ScoresFromCsvTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, category) -> None:
        self.category = category
        self.director_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQvkS0pEG7bYLkROOqa_5fBRtU92kBjUqcsOpGmSNHb_Hh7Q9b6Haf2pO0CnDDcPi8IbzmlMvJjYhc4/pub?gid=1457223827&single=true&output=csv'
        self.hero_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSn0EY0v8Oqg-uLvLrxbGMV0-Wfkt5oHdNdOetZIz2ykeJMfMDCiiWxyEHD5PuvGtBV3r5cJj4nN8lO/pub?gid=2115785350&single=true&output=csv'
        self.heroine_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS2qQq80RVgVIg5KH4THgA5Qz2ahcyhlnJ0UTGOmMC6cPqY1hUDa1cEVnPCYkbIeTLiLVMT5sBz9sSn/pub?gid=826200949&single=true&output=csv'

    @staticmethod
    def get_scores_from_csv(x,category_link,category_name):
        data = pd.read_csv(category_link)
        scores = []
        for name in x:
            if name in data[category_name].values:
                score = data.loc[data[category_name] == name, 'score'].iloc[0]
                scores.append(score)
            else:
                # If the name doesn't exist, return the median score
                median_score = data['score'].median()
                scores.append(median_score)
        
        return scores
    
    def fit(self,x,y=None):
        return self
    
    def transform(self,x):

        if self.category == 'crew':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x,self.director_scores,'crew')
            return np.array(scores).reshape(-1, 1)
        
        elif self.category == 'hero':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x,self.hero_scores,'hero')
            return np.array(scores).reshape(-1, 1)
        
        elif self.category == 'heroine':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x,self.heroine_scores,'heroine')
            return np.array(scores).reshape(-1, 1)
        else:
            return None


class DataPreprocessing:
    def __init__(self, config:DataPreprocessorConfig) -> None:
        self.config = config

        self.continous_num_col = ['budget','runtime']
        self.list_category_col = ['genres']
        self.normal_category_col = ['production_countries','spoken_languages']
        self.label_category_col = ['release_month']
        self.crew_col = ['crew']
        self.hero_col = ['hero']
        self.heroine_col = ['heroine']


    @staticmethod
    def log_normal_transform(x):
        return np.log1p(x)
    
    @staticmethod
    def custom_genre_on_hot_encode(x):
        df_encoded = pd.get_dummies(x.apply(pd.Series).stack()).sum(level=0)
        return df_encoded
    

    def get_data_preprocessor_object(self):
        """
        This function is responsible for all the preprocessing of the data  to make it suitable for training.
        """

        continous_num_pipeline = Pipeline(
            steps=[
                ('log_normal',FunctionTransformer(DataPreprocessing.log_normal_transform)),
                ('imputer',SimpleImputer(strategy='median')),
                ('sacler',StandardScaler())
            ]
        )

        list_category_pipeline = Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('stack_encoder',FunctionTransformer(DataPreprocessing.custom_genre_on_hot_encode)),
                ('scaler',StandardScaler(with_mean=False))
            ]
        )

        normal_category_pipeline = Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ]
        )

        label_category_pipeline = Pipeline(
            steps=[
                ('label_encoder',LabelEncoder()),
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ]
        )

        hero_pipeline = Pipeline(
            steps=[
                ('get_scores',ScoresFromCsvTransformer(category='hero')),
                ('scaler',StandardScaler())
            ]
        )

        crew_pipeline = Pipeline(
            steps=[
                ('get_scores',ScoresFromCsvTransformer(category='crew')),
                ('scaler',StandardScaler())
            ]
        )

        heroine_pipeline  = Pipeline(
            steps=[
                ('get_scores',ScoresFromCsvTransformer(category='heroine')),
                ('scaler',StandardScaler())
            ]
        )


        preprocessor = ColumnTransformer(
            [
                ('Continous_num_pipeline',continous_num_pipeline,self.continous_num_col),
                ('list_category_pipeline',list_category_pipeline,self.list_category_col),
                ('normal_category_pipeline',normal_category_pipeline,self.normal_category_col),
                ('label_category_pipeline',label_category_pipeline,self.label_category_col),
                ('hero_pipeline',hero_pipeline,self.hero_col),
                ('crew_pipeline',crew_pipeline,self.crew_col),
                ('heroine_pipeline',heroine_pipeline,self.heroine_col)
            ]
        )

        ## Save the Preprocessor 
        preprocessor_path = os.path.join(self.config.root_dir,'preprocessor.pkl')
        joblib.dump(preprocessor,preprocessor_path)

       
    
    










