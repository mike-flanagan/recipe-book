import streamlit as st
import boto3, re, sys, os, time, math, csv, json, pickle
from os import system
from math import floor
from copy import deepcopy
from collections import defaultdict # used in get_top_n() function from Surprise documentation
from sagemaker import get_execution_role
import numpy as np                                
import pandas as pd                               
import matplotlib.pyplot as plt  
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS 
# sys.path.insert(0, '/home/ec2-user/SageMaker/recipe-book/code/')
from code.functions import get_top_n # despite importing defaultdict above, this function doesn't seem to be able to recognize it in this notebook
from surprise.prediction_algorithms import SVD, CoClustering, BaselineOnly
from surprise.model_selection import GridSearchCV, cross_validate, train_test_split
from surprise import Reader, Dataset, accuracy, dump

from IPython.display import Image                 
from IPython.display import display               
from time import gmtime, strftime                 

# Setting display options for DataFrames and plots
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', 200)
sns.set_theme(font_scale=1.5)
%matplotlib inline

print('hello, world!')
print('welcome to Sate, the recipe book with your taste in mind.')