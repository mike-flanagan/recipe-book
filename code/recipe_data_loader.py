"""
    Helper functions for data loading and manipulation.
"""
# Data handling dependencies
import numpy as np
import pandas as pd

def load_recipe_names(csv_filename):
    """
        Load recipe names from the source data file's path.
    
    Returns a list of recipe names.
    
    Parameters:
    ----------
    file : str
        Relative or absolute path to recipes CSV file. 
    -------
    """
    # Data: read CSV file in as pandas DataFrame
    rdf = pd.read_csv(csv_filename)
    
        # Data: alternatively, data may be loaded from the cloud (AWS S3)
    # recipes_url = ('https://sagemaker-studio-t1ems8mtnoj.s3.us-east-2.amazonaws.com/RAW_recipes.csv')
    # rdf = pd.read_csv(recipes_url) 

    # Cleaning: Dropping row that contains a NaN value for recipe name
    rdf.drop(labels=721, inplace = True)
    # Cleaning/FE: Creating columns for recipe's respective nutrients
    rdf['kcal'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[0])
    rdf['fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[1])
    rdf['sugar'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[2])
    rdf['salt'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[3])
    rdf['protein'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[4])
    rdf['sat_fat'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[5])
    rdf['carbs'] = rdf.nutrition.apply(lambda x: x[1:-1].split(sep=', ')[6])
    # Cleaning: Imputing outlier value to median
    rdf['minutes'] = np.where(rdf.minutes == 2147483647,
                             rdf.minutes.median(),
                             rdf.minutes)
    recipe_list = rdf['name'].to_list()
    return recipe_list