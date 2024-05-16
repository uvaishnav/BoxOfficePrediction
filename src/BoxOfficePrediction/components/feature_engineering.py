import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import ast

from BoxOfficePrediction import logger
from BoxOfficePrediction.entity.config_entity import FeatureEngineeringConfig
from BoxOfficePrediction.utils.common import remove_columns

class FeatureEngineering:
    def __init__(self,config:FeatureEngineeringConfig) -> None:
        self.config = config
    
    @staticmethod
    def update_countries(list):
        if 'United States of America' in list:
            return 'US'
        else:
            return 'other'
        
    @staticmethod
    def update_language(list):
        if 'English' in list:
            return 'en'
        else:
            return 'other'
    
    @staticmethod
    def assign_score(feature, cinema_db):
        feature_data = cinema_db.groupby(feature)
        columns = [feature, 'score']

        feature_score = pd.DataFrame(columns=columns)
        for group_name, group_data in feature_data:
            popularity_score = group_data['popularity'].mean()
            weighted_rating_score = group_data['weighted_rating'].mean()

            score = 0.7 * popularity_score + 0.3 * weighted_rating_score

            # Append a row to the DataFrame using loc
            feature_score.loc[len(feature_score)] = [group_name, score]
    
        return feature_score
    
    def save_scores(self,score_card,card_name):
        save_path = os.path.join(self.config.scores_data,card_name)
        score_card.to_csv(save_path,index=False)
    
    def get_table(self):
        self.cinema_db = pd.read_csv(self.config.organized_data)
    
    def handle_missing_values(self):

        """
        Remove all entries with zero entries or NaN entries as they have no impact on trget variable.
        """

        nan_features = [feature for feature in self.cinema_db.columns if self.cinema_db[feature].isnull().sum()>=1]
        zero_features = [feature for feature in self.cinema_db if (self.cinema_db[feature]==0).sum()>=1]

        cond1 = (self.cinema_db[nan_features].isnull()).any(axis=1)
        cond2 = (self.cinema_db[zero_features]==0).any(axis=1)

        self.cinema_db = self.cinema_db[~cond1]
        self.cinema_db = self.cinema_db[~cond2]

    def get_weighted_vote(self):
        """
        1)Get a fair voting coomparision with weighted vote average from 'vote_average' and 'vote_count'

        2) remove vote_count and vote_average as their relevence is captured through weighted_rating column
        """

        # Finding overall mean
        overall_mean = self.cinema_db['vote_average'].mean()

        # minimum n.of votes required to be listed in the chart
        m = self.cinema_db['vote_count'].quantile(0.7)

        def weighted_rating(x, m=m, C=overall_mean):
            v = x['vote_count']
            R = x['vote_average']
            # Calculation based on the IMDB formula
            return (v/(v+m) * R) + (m/(m+v) * C)

        # getting 'weighted_rating'
        self.cinema_db['weighted_rating'] = self.cinema_db.apply(weighted_rating, axis=1)

        remove_columns(self.cinema_db,['vote_count','vote_average'])

    def get_footfall(self):
        """
        1) Handle variation in ticket prices over time by considering footfall
        for a fair comparision between movies across time and calculate revenue by predicting footfall

        2) Remove any zero entries within the new feature 

        3) remove 'revenue' and 'avg_ticket_price' as they are not nesessary for training further as their relevence is captured as footfall
        """

        self.cinema_db['footfall'] = self.cinema_db['revenue']//self.cinema_db['avg_ticket_price']
        self.cinema_db = self.cinema_db[self.cinema_db['footfall']!=0]
        remove_columns(self.cinema_db,['revenue','avg_ticket_price'])

    def handle_list_categorical_features(self):
        """
        1) remove production companies
        2) change entries of porduction_countries as US or other
        3) change entries of spoken_languages to english or other
        4) remove original_language as we have the data of spoken_languages similar to it.
        """

        self.cinema_db['production_countries'] = self.cinema_db['production_countries'].apply(self.update_countries)
        self.cinema_db['spoken_languages'] =  self.cinema_db['spoken_languages'].apply(self.update_language)

        remove_columns(self.cinema_db,['production_companies','original_language'])

    def handle_normal_categorical_features(self):
        """
        the impact of movies in post production stage is very minimal so we have to remove such entries
        - Remove entries belong to post production stage
        - then remove the status column as there will be only one category left 
        """

        condition = self.cinema_db['status']!='Released'
        self.cinema_db = self.cinema_db[~condition]

        remove_columns(self.cinema_db,['status'])

    def handle_special_categorical_features(self):
        """
        - crew, hero, heroine
        - Have many unique values so they cannot be handled by using common techniques like one-hot-encoding, label-encoding, frequency-encoding etc..
        - They have to be handled specially

        Scores to each of these feature.
        'score = 0.7*popularity + 0.3*weighted_rating'

        - asign scores to crew, hero, heroine
        - apply log normal transformation to handle skewness.
        - save the scores.

        remove popularity and weighted_rating as their significance is reprsented by scores.
        """

        ## Director Score
        director_score = self.assign_score('crew',self.cinema_db)
        director_score['score'] = np.log(director_score['score'])
        self.save_scores(director_score,'director_score.csv')

        ## Hero scores
        hero_score = self.assign_score('hero',self.cinema_db)
        hero_score['score'] = np.log(hero_score['score'])
        self.save_scores(hero_score,'hero_score.csv')

        ## Heroine scores
        heroine_score = self.assign_score('heroine',self.cinema_db)
        heroine_score['score'] = np.log(heroine_score['score'])
        self.save_scores(heroine_score,'heroine_score.csv')

        remove_columns(self.cinema_db,['popularity','weighted_rating'])

    def save_test_train_data(self):
        root_path = self.config.featured_data

        # split data into train and test subsets in ratio 80:20
        train, test = train_test_split(self.cinema_db,test_size=0.2)

        # save them
        train_path = os.path.join(root_path,"train.csv")
        train.to_csv(train_path,index=False)

        test_path = os.path.join(root_path,"test.csv")
        test.to_csv(test_path,index=False)