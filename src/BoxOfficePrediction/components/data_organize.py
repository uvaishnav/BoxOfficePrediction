import os
from pathlib import Path

import numpy as np
import pandas as pd

import calendar
import ast

from BoxOfficePrediction import logger
from BoxOfficePrediction.utils.common import remove_columns
from BoxOfficePrediction.entity.config_entity import DataOrganizeConfig


class DataOrganize:
    def __init__(self, config:DataOrganizeConfig) -> None:
        self.config = config

    def get_names_from_att(self,obj):
        x=[]
        for i in ast.literal_eval(obj):
            x.append(i['name'])
        return x
    
    def get_director(self,obj):
        x=[]
        for i in ast.literal_eval(obj):
            if i['job']=='Director':
                x.append(i['name'])
                break
        return x
            

    def merge_tables(self):
        movie_table = pd.read_csv(self.config.movie_table_path)
        credit_table = pd.read_csv(self.config.credit_table_path)

        self.cinema_db = movie_table.merge(credit_table, on='title')

        logger.info("Merged movie and creditas tables")

    def organise_numerical_features(self):

        remove_columns(self.cinema_db,['id','movie_id'])

        logger.info("Removed id and movie_id columns")

    def organise_temporial_features(self):

        # Convert 'release_date' to datetime format
        self.cinema_db['release_date'] = pd.to_datetime(self.cinema_db['release_date'])

        # Extract month from 'release_date'
        self.cinema_db['release_month'] = self.cinema_db['release_date'].dt.month

        # Map month numbers to month names
        self.cinema_db['release_month'] = self.cinema_db['release_month'].apply(lambda x: calendar.month_abbr[int(x)] if not np.isnan(x) else np.nan)

        # Extract Year from 'release_date'
        self.cinema_db['release_year'] = self.cinema_db['release_date'].dt.year

        # Convert non-null values in release_year column to integers
        self.cinema_db['release_year'] = pd.to_numeric(self.cinema_db['release_year'], errors='coerce').astype('Int64')

        logger.info("Year and month are extracted.")

        #remove 'release_date'
        remove_columns(self.cinema_db,['release_date'])

        logger.info("Removed Release date")

    def combine_ticket_price_table(self):

        #read Data
        ticket_price_db = pd.read_csv(self.config.ticket_price_table_path)

        # handle avg_price_type
        ticket_price_db['avg_ticket_price'] = ticket_price_db['avg_ticket_price'].str.replace('$','').astype(float)

        # rename year column to release_year to merge
        ticket_price_db = ticket_price_db.rename(columns={'year':'release_year'})

        # Convert year to Int64 type
        ticket_price_db['release_year'] = pd.to_numeric(ticket_price_db['release_year'],errors='coerce').astype('Int64')

        # Join the cinema_db with ticket_price_db based on year
        cinema_data = self.cinema_db.merge(ticket_price_db,on='release_year',how="left")
        self.cinema_db = cinema_data

        # Remove the year attribute as it not significant after we got prices 
        remove_columns(self.cinema_db,['release_year'])

        logger.info("Cinema db combined with ticket prices")

    def organise_categorical_features(self):

        # remove all the unwanted Categorical columns
        remove_columns(self.cinema_db,['homepage','original_title','title','tagline','overview','keywords'])

        # Formating genres,production_companies,production_countries,spoken_languages
        self.cinema_db['genres'] = self.cinema_db['genres'].apply(self.get_names_from_att)
        self.cinema_db['production_companies'] = self.cinema_db['production_companies'].apply(self.get_names_from_att)
        self.cinema_db['production_countries'] = self.cinema_db['production_countries'].apply(self.get_names_from_att)
        self.cinema_db['spoken_languages'] = self.cinema_db['spoken_languages'].apply(self.get_names_from_att)

        # modify Cast to get hero and heroine names
        self.cinema_db['cast'] = self.cinema_db['cast'].apply(self.get_names_from_att)
        self.cinema_db['hero'] = [cast[0] if len(cast)>1 else np.nan for cast in self.cinema_db['cast']]
        self.cinema_db['heroine'] = [cast[1] if len(cast)>1 else np.nan for cast in self.cinema_db['cast']]

        # Remove Cast
        remove_columns(self.cinema_db,['cast'])

        # Modify crew to get director name
        self.cinema_db['crew'] = self.cinema_db['crew'].apply(self.get_director)
        self.cinema_db['crew'] = [crew[0] if len(crew)>0 else np.nan for crew in self.cinema_db['crew']]

        logger.info("Categorical features organised Successfully")

    def save_organized_data(self):
        save_path = os.path.join(self.config.org_table_path,'organized_cinema.csv')
        self.cinema_db.to_csv(save_path,index=False)


