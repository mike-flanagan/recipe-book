# import libraries
import boto3, re, sys, os, time, math, csv, json, pickle, urllib.request
from sys import getsizeof
from os import system
from time import gmtime, strftime                 
from math import floor
from copy import deepcopy
from collections import defaultdict
import numpy as np                                
import pandas as pd                               
import matplotlib.pyplot as plt  
import seaborn as sns
import requests
from wordcloud import WordCloud, STOPWORDS 
from surprise.similarities import cosine, msd, pearson
from surprise.prediction_algorithms import SVD, KNNWithMeans, KNNBaseline, CoClustering, BaselineOnly
from surprise.model_selection import GridSearchCV, cross_validate, train_test_split
from surprise import Reader, Dataset, accuracy, dump
from IPython.display import Image                 
from IPython.display import display               
# from surprise.prediction_algorithms import SVD, knns, KNNWithMeans, KNNBasic, KNNBaseline, KNNWithZScore, CoClustering, BaselineOnly, NormalPredictor, NMF, SVDpp, SlopeOne # these were all packages I originally played with, cut out to improve memory utilization

# Setting display options for DataFrames and plots
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
sns.set_theme(font_scale=1.5)

def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def tags_to_csv(tags_list):
    """
    Write CSVs of recipes based on one of its tags.

    Parameters: 
        
        tags_list 
        - a list containing strings that correspond to recipe tags (rdf['tags']).

    Returns:
        
        Writes CSV files to path: data/cuisines/tag_string.csv
    """
    for i in tags_list:
        tag_recipes = rdf[rdf.tags.str.contains(i, case=False) == True]
        tag_recipes.to_csv(f'data/cuisine/{i}.csv')

def read_img_url(url):
    """
    Read and resize image directly from a url
    ============
    Parameters:
        url
        - Image source URL.
    
    Attribution:
        
        This (partially modified) function was borrowed from Justin Tennenbaum's ColorGan Streamlit application.
        https://github.com/jmt0221/
        https://github.com/jmt0221/ColorGan/blob/master/streamlit/app.py
        
    """
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# def choices_to_df(choices_list=fav_recipes)
#             """
#             Take in a list of the user's 5 selections and convert them in to 
#             a dataframe that the models may be run on.
#             ===========
#             Parameters: choices_list (Default: fav_recipes)
#             """
#             user = [1]*5
#             rating = [5]*5
#             ids = []
#             for i in choices_list:
#                 ids.append(rdf[rdf.name == i].id.values[0])
#             user_ratings = {'user_id':user, 'recipe_id':ids, 'rating':rating}
#             udf = pd.DataFrame.from_dict(user_ratings)
#             return udf

# def cuisine_mask(cuisine_list, df=rdf, column='tags'):
#         """
#     This function takes in a list of strings used to filter recipes by the 'tags' column of a DataFrame.
#     Returns a DataFrame filtered by the items in the cuisine_list.
#     ================
#     Parameters:
        
#         cuisine_list
        
#             a list of strings representing one of the cuisines listed on a recipe's tags.
        
#         df
            
#             Default: rdf
            
#             The DataFrame to be filtered. 
            
#         column
            
#             Default: 'tags'
            
#             The name of the column to be filtered.
#     ================
#     """
#     masked_food_df = None
#     for i in cuisine_list:
#         masked_food_df = df[df[column].str.contains(i, case=False) == True]
# #     if str(type(masked_food_df)) == 'pandas.core.frame.DataFrame':
#     return masked_food_df

# # Data for cuisine_filter() function
# rdf = pd.read_csv('data/RAW_recipes.csv')
# # idf = pd.read_csv('data/RAW_interactions.csv')

# # Cleaning
# rdf.drop(labels=721, inplace = True)
# rdf['kcal'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[0])
# rdf['fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[1])
# rdf['sugar'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[2])
# rdf['salt'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[3])
# rdf['protein'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[4])
# rdf['sat_fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[5])
# rdf['carbs'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[6])
# rdf['minutes'] = np.where(rdf.minutes == 2147483647,
#                          rdf.minutes.median(),
#                          rdf.minutes)

# # idf['date'] = pd.to_datetime(idf.date)

# def cuisine_filter(cuisine_list, df=rdf, column='tags', verbose=0):
#     """
#     THIS UNFORTUNATELY WILL NOT WORK WITH STREAMLIT. REQUIRES DEBUGGING
    
#     This function takes in a list of strings used to filter recipes by the 'tags' column of a DataFrame.
#     Returns a DataFrame filtered by the items in the cuisine_list.
#     ================
#     Parameters:
        
#         cuisine_list
        
#             a list of strings representing one of the cuisines listed on a recipe's tags.
        
#         df
            
#             Default: rdf
            
#             The DataFrame to be filtered. 
            
#         column
            
#             Default: 'tags'
            
#             The name of the column to be filtered.
        
#         verbose
            
#             Default: 0
            
#             If 0: returns the filtered DataFrame.
            
#             If 1: 
#             - returns the number of items remaining in the DataFrame after all filters.
#             - returns the filtered DataFrame
            
#             If 2:
#             - returns the number of items remaining in the DataFrame after each filter.
#             - returns the filtered DataFrame
            
#             If -1: 
#             - returns *only* the number of items that would remain in the DataFrame after all filters.
            
#             If 21: 
#             - returns *only* the number of items that would remain in the DataFrame after each filters.

#     ================
#     """
#     masked_food_df = df
#     filtered_lengths = ["Length of original df: 231,636"]
#     for i in cuisine_list:
#         masked_food_df = df[df[column].str.contains(i, case=False) == True]
#         filtered_lengths.append(f"Length after filter \'{i}\': {len(masked_food_df)}")
#     if str(type(masked_food_df)) == 'pandas.core.frame.DataFrame' and len(masked_food_df) != 0:
#         if verbose == 2:
#             print(filtered_lengths)
#             return masked_food_df
#         elif verbose == 1:
#             print(len(masked_food_df))
#             return masked_food_df
#         elif verbose == -1:
#             print(f'Length after all filters: {len(masked_food_df)}')
#         elif verbose == -2:
#             return filtered_lengths
#         elif verbose == 0:
#             return masked_food_df
#     else:
#         print('It looks like you\'ve filtered out all recipes!\nTry removing some tags')

# def head(data='interactions', disp_head=3):
#     """
#     ### Dev. note: THIS WOULD BE BETTER WITHIN A DEFINED CLASS SO THAT I COULD SWITCH IT UP MORE EASILY ###
    
#     Takes in a dataframe and sets display.max_colwidth before returning the dataframe.head().
    
#         Default for int_df: display.max_colwidth = 200
        
#         Default for all other dataframes: display.max_colwidth = 50
    
#     Parameters = (data: DataFrame, disp_head: int):
    
#         data: 'interactions' or 'recipes'. 
        
#             Default: data = interactions

#         disp_head: Non-negative integer number of first rows to display. 

#             Default for interactions: 11
#             Default for all other dataframes: 3
    
#     """
#     num_rows = 3
#     if disp_head > 0:
#         num_rows = disp_head
#     if data == 'interactions':
#         pd.set_option('display.max_colwidth', 400)
#         num_rows = 11
#         return int_df.head(num_rows)
#     elif data == 'recipes':
#         pd.set_option('display.max_colwidth', 50)
#         return df.head(num_rows)
        