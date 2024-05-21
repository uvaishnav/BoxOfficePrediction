import os
import pandas as pd
import numpy as np
import ast

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, FunctionTransformer
from sklearn.base import BaseEstimator, TransformerMixin

from BoxOfficePrediction.entity.config_entity import DataPreprocessorConfig
from BoxOfficePrediction import logger


# Custom transformer for getting scores from CSV files

class ScoresFromCsvTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, category):
        self.category = category
        self.director_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQvkS0pEG7bYLkROOqa_5fBRtU92kBjUqcsOpGmSNHb_Hh7Q9b6Haf2pO0CnDDcPi8IbzmlMvJjYhc4/pub?gid=1457223827&single=true&output=csv'
        self.hero_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSn0EY0v8Oqg-uLvLrxbGMV0-Wfkt5oHdNdOetZIz2ykeJMfMDCiiWxyEHD5PuvGtBV3r5cJj4nN8lO/pub?gid=2115785350&single=true&output=csv'
        self.heroine_scores = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vThFs2Qwa2_ueOmhhVeWCU2ly6xUQG07UAQfs5jceiHj0IH70ebtmy8clpx64kR4sM-CwJsOmJQFhhO/pub?gid=597603140&single=true&output=csv'
    
    @staticmethod
    def get_scores_from_csv(x, category_link, category_name):
        logger.info("Shape of data given to get_scores_function : {}".format(x.shape))
        logger.info("Started extracting {} scores".format(category_name))
        data = pd.read_csv(category_link)
        scores = []
        for index, row in x.iterrows():
            name = row[0]  # Assuming the name is in the first column of the DataFrame
            if name in data[category_name].values:
                score = data.loc[data[category_name] == name, 'score'].iloc[0]
                scores.append(score)
            else:
                # If the name doesn't exist, return the median score
                median_score = data['score'].median()
                scores.append(median_score)
        
        logger.info("Extracted {} scores".format(category_name))
        logger.info("no.of entries in scores : {}".format(len(scores)))
        return scores
    
    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        if self.category == 'crew':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x, self.director_scores, 'crew')
            scores_series = pd.Series(scores)
            return scores_series.values.reshape(-1, 1)
        
        elif self.category == 'hero':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x, self.hero_scores, 'hero')
            scores_series = pd.Series(scores)
            return scores_series.values.reshape(-1, 1)
        
        elif self.category == 'heroine':
            scores = ScoresFromCsvTransformer.get_scores_from_csv(x, self.heroine_scores, 'heroine')
            scores_series = pd.Series(scores)
            return scores_series.values.reshape(-1, 1)
        else:
            return None
        

class MyLabelEncoder(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.encoder = LabelEncoder(*args, **kwargs)
    
    def fit(self, x, y=None):
        self.encoder.fit(x)
        return self
    
    def transform(self, x, y=None):
        transformed = self.encoder.transform(x)
        return transformed.reshape(-1, 1)
        

class DataPreprocessing:
    def __init__(self, config: DataPreprocessorConfig) -> None:
        self.config = config

        self.continous_num_col = ['budget', 'runtime']
        self.list_category_col = ['genres']
        self.normal_category_col = ['production_countries', 'spoken_languages']
        self.label_category_col = ['release_month']
        self.crew_col = ['crew']
        self.hero_col = ['hero']
        self.heroine_col = ['heroine']

        # Define all possible genres here
        self.all_possible_genres = [
            'Action', 'Animation', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music',
            'Mystery', 'Romance', 'Science Fiction', 'Foreign', 'Thriller',
            'War', 'Western', 'Adventure'
        ]

    @staticmethod
    def log_normal_transform(x):
        return np.log1p(x)
    
    @staticmethod
    def convert_to_list(gener):
        logger.info("Shape of genre sent to convert_list : {}".format(gener.shape))
        return gener.apply(ast.literal_eval)

    def custom_genre_on_hot_encode(self, x):
        # Convert string representations of lists to actual lists
        x = x.apply(DataPreprocessing.convert_to_list)
        logger.info("Shape of genre returned by convert_to_list {}".format(x.shape))
        # Explode the lists into separate rows
        x_exploded = x.explode('genres')

        # Create a DataFrame with all possible genres initialized to 0
        df_all_genres = pd.DataFrame(columns=self.all_possible_genres)
        df_all_genres = pd.concat([df_all_genres, pd.DataFrame(0, index=x.index, columns=self.all_possible_genres)], ignore_index=False)

        # Apply one-hot encoding on the actual data
        df_encoded = pd.get_dummies(x_exploded, prefix='', prefix_sep='')

        # Ensure only the predefined genres are considered
        df_encoded = df_encoded.reindex(columns=self.all_possible_genres, fill_value=0)

        # Aggregate the one-hot encoded values back to the original structure
        df_aggregated = df_encoded.groupby(level=0).max()
        
        return df_aggregated

    @staticmethod
    def get_shape_begin(x):
        logger.info("Shape of column before preprocessing : {} ".format(x.shape))
        return x

    @staticmethod
    def get_shape_end(x):
        logger.info("Shape of column after preprocessing : {} ".format(x.shape))
        return x

    def get_data_preprocessor_object(self):
        continous_num_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('log_normal', FunctionTransformer(DataPreprocessing.log_normal_transform)),
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        list_category_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('stack_encoder', FunctionTransformer(self.custom_genre_on_hot_encode)),
                ('scaler', StandardScaler(with_mean=False)),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        normal_category_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False)),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        label_category_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('label_encoder', MyLabelEncoder()),
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        hero_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('get_scores', ScoresFromCsvTransformer(category='hero')),
                ('scaler', StandardScaler()),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        crew_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('get_scores', ScoresFromCsvTransformer(category='crew')),
                ('scaler', StandardScaler()),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        heroine_pipeline = Pipeline(
            steps=[
                ('start_shape', FunctionTransformer(DataPreprocessing.get_shape_begin, validate=False, accept_sparse=True)),
                ('get_scores', ScoresFromCsvTransformer(category='heroine')),
                ('scaler', StandardScaler()),
                ('end_shape', FunctionTransformer(DataPreprocessing.get_shape_end, validate=False, accept_sparse=True))
            ]
        )

        preprocessor = ColumnTransformer(
            [
                ('Continous_num_pipeline', continous_num_pipeline, self.continous_num_col),
                ('List_category_pipeline', list_category_pipeline, self.list_category_col),
                ('Normal_category_pipeline', normal_category_pipeline, self.normal_category_col),
                ('Label_category_pipeline', label_category_pipeline, self.label_category_col),
                ('Hero_pipeline', hero_pipeline, self.hero_col),
                ('Crew_pipeline', crew_pipeline, self.crew_col),
                ('Heroine_pipeline', heroine_pipeline, self.heroine_col)
            ]
        )

        return preprocessor
