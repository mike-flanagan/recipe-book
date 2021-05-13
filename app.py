# cut my imports and pasted temporarily in frontend_development
"""
    Streamlit webserver-based Recommender Engine.
    Author: Mike Flanagan.
    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.
    NB: !! Do not remove/modify the code delimited by dashes !!
    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------
    Description: This file is used to launch a minimal streamlit web
    application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.
    For further help with the Streamlit framework, see:
    https://docs.streamlit.io/en/latest/
"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
# from code.functions import *
# from code.recipe_data_loader import load_recipe_names
from io import BytesIO # for header image
from PIL import Image
from pathlib import Path
import base64
from surprise.similarities import cosine, msd, pearson
from surprise.prediction_algorithms import SVD, BaselineOnly
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset, accuracy, dump

# Data
rdf = pd.read_csv('data/RAW_recipes.csv')
idf = pd.read_csv('data/RAW_interactions.csv')

# Cleaning
rdf.drop(labels=721, inplace = True)
rdf['kcal'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[0])
rdf['fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[1])
rdf['sugar'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[2])
rdf['salt'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[3])
rdf['protein'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[4])
rdf['sat_fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[5])
rdf['carbs'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[6])
rdf['minutes'] = np.where(rdf.minutes == 2147483647, rdf.minutes.median(), rdf.minutes)
idf['date'] = pd.to_datetime(idf.date)

@st.cache
def img_to_bytes(img_path):
    """
    Converts an image in to base64 byte encoding.
    =============
    Parameters:
    - img_path
        path to image file    
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
    
header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes("images/app_assets/sate_logo_aubergine.png"))
st.markdown(header_html, unsafe_allow_html=True)

@st.cache
def recipe_names(df):
    """
    Load recipe names from the source data file's path.
    Returns a list of recipe names.
    Parameters:
    ----------
    file : str
        Relative or absolute path to recipes CSV file. 
    ----------
    """
    recipe_list = df['name'].to_list()
    return recipe_list

recipe_list = recipe_names(rdf)
# page_options = ["Recommend Recipes"]

# User-based preferences
foodmood = st.multiselect('Pick some things that you like.', options=[
        'salads',
        'barbecue',
        'breakfast', 
        'pasta', 
        'pizza',
        'vegan',
        'soup',
        'healthy',
        'seafood',
        'pork',
        'beef',
        'poultry', 
        'side-dishes',
        'sandwiches',
        'pies',
        'crock-pot-slow-cooker',
        'baking',
        'vegetarian', 
        'meat',
        'savory-pies',
        'dessert',
        'chocolate',
        'ice-cream',
        'cocktails',
        'nuts',
        'fruit',
        'vegetables',
        'eggs-dairy',
        'burger',
        'breads',
        'tea',
        'raw',
        'dietary',
    ])

regions = st.multiselect('You may also select to see cuisines of certain regions of origin, if you like.', options=[
                    'japanese',
                    'italian',
                    'french',
                    'mexican', 
                    'greek',
                    'american',
                    'korean',
                    'ethiopian', 
                    'german',
                    'swiss',
                    'spanish',
                    'chinese',
                    'russian',
                    'south-american',
                    'african',
                    'european',
                    'north-american'
     ])

# page_selection = st.sidebar.selectbox("Choose Option", page_options)
#     if page_selection == "Recommend Recipes":
        # Header contents
#         st.write('# Recipe Recommender Engine')
#         st.write('### EXPLORE Recipe Recommendation Predictions')
#         st.image('images/lily-banse--YHSwy6uqvk-unsplash.jpg',use_column_width=True)
        
# Masking to filter the dataframe
@st.cache
def cuisine_mask(cuisine_list, df=rdf, column='tags'):
    """
This function takes in a list of strings used to filter recipes by the 'tags' column of a DataFrame.
Returns a DataFrame filtered by the items in the cuisine_list.
================
Parameters:
    cuisine_list
        A list of strings representing one of the cuisines listed on a recipe's tags.
    df   —   Default: rdf
        The DataFrame to be filtered. 
    column  —  Default: 'tags'
        The name of the column to be filtered.
"""
    masked_food_df = df
    for i in cuisine_list:
        masked_food_df = df[df[column].str.contains(i, case=False) == True]
#     if str(type(masked_food_df)) == 'pandas.core.frame.DataFrame':
    return masked_food_df

df = cuisine_mask(foodmood, rdf)
# if str(type(df)) == 'pandas.core.frame.DataFrame':
filtered_recipe_list = df['name'].to_list()

# App declaration
def main():
        st.write('### Select options that you rate highly.')
        recipe_1 = st.selectbox('Favorite Recipe 1', filtered_recipe_list[930:960])
        recipe_2 = st.selectbox('Favorite Recipe 2', filtered_recipe_list[255:285])
        recipe_3 = st.selectbox('Favorite Recipe 3', filtered_recipe_list[1100:1130])
        recipe_4 = st.selectbox('Favorite Recipe 4', filtered_recipe_list[11000:11085])
        recipe_5 = st.selectbox('Favorite Recipe 5', filtered_recipe_list[13000:13130])
        fav_recipes = [recipe_1, recipe_2, recipe_3, recipe_4, recipe_5]

        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                      ('Baseline Alternating Least Squares',
                       'Baseline Stochastic Gradient Descent',
                       'Funk\'s Singular Value Decomposition'))

        # Perform top-10 recipe recommendation generation
        if sys == 'Baseline Alternating Least Squares':
            if st.button('ALS'):
                try:
                    with st.spinner('Crunching numbers for crunchy panko...'):
                        top_recommendations = get_top_n( #############
                                                als_preds, 
                                                n=10)
                    st.title("Suggestions from our Maître D'. Bon Appétit!")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Hmmm... We seem to be having some difficulties.\
                              We'll whip up a fix and be back in service soon!")


        if sys == 'Baseline Stochastic Gradient Descent':
            if st.button('SGD'):
                try:
                    with st.spinner('Crunching numbers for crunchy panko...'):
                        top_recommendations = get_top_n( #############
                                                sgd_preds, 
                                                n=10)
                    st.title("Suggestions from our Maître D'. Bon Appétit!")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Hmmm... We seem to be having some difficulties.\
                              We'll whip up a fix and be back in service soon!")


        if sys == 'Baseline Stochastic Gradient Descent':
            if st.button('SVD'):
                try:
                    with st.spinner('Crunching numbers for crunchy panko...'):
                        top_recommendations = get_top_n( #############
                                                svd_preds, 
                                                n=10)
                    st.title("Suggestions from our Maître D'. Bon Appétit!")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Hmmm... We seem to be having some difficulties.\
                              We'll whip up a fix and be back in service soon!")
#     else:
#         st.write('## It looks like you\'ve filtered out all recipes!\nTry removing some tags')


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
#     if page_selection == "Solution Overview":
#         st.title("Solution Overview")
#         st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()