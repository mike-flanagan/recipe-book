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
from code.functions import *
from code.recipe_data_loader import load_recipe_names
# from recommenders.collaborative_based import collab_model
# from recommenders.content_based import content_model

st.title('Sate')
st.write('the recipe book with your taste in mind')

# Data
recipe_list = load_recipe_names('data/RAW_recipes.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommend Recipes","Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommend Recipes":
        # Header contents
        st.write('# Recipe Recommender Engine')
        st.write('### EXPLORE Recipe Recommendation Predictions')
        st.image('images/lily-banse--YHSwy6uqvk-unsplash.jpg',use_column_width=True)
        
        # User-based preferences
        st.write('### Enter Your Three Favorite Recipes')
        recipe_1 = st.selectbox('First Option', recipe_list[14930:15200])
        recipe_2 = st.selectbox('Second Option', recipe_list[25055:25255])
        recipe_3 = st.selectbox('Third Option', recipe_list[21100:21200])
        fav_recipes = [recipe_1, recipe_2, recipe_3]
        
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


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()