![image](https://github.com/mike-flanagan/recipe-book/blob/main/images/lily-banse--YHSwy6uqvk-unsplash.jpg)  
  
<div align="center";>Photo by <a href="https://unsplash.com/@lvnatikk?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Lily Banse</a> on <a href="https://unsplash.com/@lvnatikk?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a></div>  
  
## Overview  
This repository contains all work involved in the development of a recipe recommendation system with the ultimate goal of launching a front-end web application.  
  
## Business Problem & Motivation  
Some of the most successful and well known companies in the world use recommender systems to deliver products, services & content. *Google* uses recommender systems to target advertising, while *Amazon* uses them to connect customers on the platform to items that are more relevant and likely to be purchased, given the customer's profile. *Netflix*, *YouTube*, and many others do the same for content so that we may spend more time on their platform, and yet, when it comes to particular categories of items which play a larger role in a person's every-day life, such systems appear to be less utilized.  
  
While food delivery services (*Seamless*, *Postmates*, & *GrubHub*) and applications for grocery delivery (*Instacart*, *Fresh Direct*, etc.) most certainly utilize user data to connect their customers with content that is curated to be more relevant for them, there has yet to be a service for food *recipes* that has become ubiquitous — that is, while there are many resources for a person to find recipes, no single resource has dominated the field.  
  
In developing a food recipe recommender system, I hope to empower individuals with a tool that will allow them to better curate their life. With this system, a user will be able to discover a vast world of recipes personalized to them.
  
## Data  
This dataset consists of 180K+ recipes and 700K+ recipe reviews covering 18 years of user interactions and uploads on [Food.com](https://www.food.com/). It includes a pickle file that contains the identities of tokenized recipe ingredients, and includes versions of several CSV files for recipes & interactions, as well as versions that have been pre-processed for natural language processing.  
  
The dataset is sourced from [Kaggle](https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions/), where it was provided by researchers [Shuyang Li](https://www.kaggle.com/shuyangli94), Jianmo Ni, Julian McAuley, & [Bodhisattwa Prasad Majumder](https://www.kaggle.com/bodhisattwamajumder) of the University of California, San Diego. These researchers collected the data using Python Requests and BeautifulSoup to webscrape [Food.com](https://www.food.com/) (formerly GeniusKitchen) for their research, which is formally presented in [*Generating Personalized Recipes from Historical User Preferences*](https://www.aclweb.org/anthology/D19-1613.pdf).  
  
## Methodology  
My methodology implements the CRISP-DM model for exploratory data analysis, cleaning, modeling, and evaluation. I use descriptive and inferrential statistics to evaluate both the recipes and user interactions dataset, enact appropriate steps for data cleaning & preparation for modeling, attempt memory-based collaborative filtering using matrix factorization, and develop several models for a explicit ratings-based collaborative filtering recommender system. The algorithms used in my iterative modeling process include `scikit-surprise`'s `Baseline` recommender algorithms that use `Alternating Least Squares` (ALS) and `Stochastic Gradient Descent` (SGD), `Singular Value Decomposition` (SVD), `CoClustering`, and attempts with `k-Nearest Neighbors`(KNN). I implement the library's `cross_validate` in training the models, as well as `GridSearchCV()` to find optimum hyperparameter tuning where possible, and evaluate the resulting model performance on the Root Mean Square Error (RMSE), as well as training time and memory consumption.  
  
Tools used include Python, Surprise, PySpark, SciKit Learn, NumPy, Pandas, as well as boto3 to utilize AWS S3. Jupyter Notebooks were developed using AWS Sagemaker, and model training was made possible by AWS EC2. Visualizations were created with MatPlotLib and Seaborn.  
  
## Current Status  
This project is a work in progress. After running and evaluating different models, I evaluate the models which perform with the lowest average RMSE on user rating predictions across validation splits. At the moment, the best performing collaborative filtering model is a Baseline recommender system model that uses ALS, and allows for little-to-no further hyperparameter tuning.  
  
## Further Actions  
As a good recommender system can be only as good as the user interprets it to be, the predicted recommendations must be evaluated beyond the RMSE, with human intuition. This will be achievable (beyond testing personally) with the use of a public front-end web application. Getting a functional recipe recommendation website or app up is my next priority.  
  
Once I have a recommender system that functions for public users, I will implement AB testing to see which of my two best performing models (Baseline ALS and SGD) result in more user interaction with the site. Over the course of the next several months, I will also AB test marketing and the design of the front-end application.  
  
There are other algorithms and implementations of recommender systems that I would like to explore — such as systems that use nueral networks, and implementations developed specifically for the AWS platform. Additionally, I would like to implement a content-based recommendation systems for item-to-item and user-to-user similarity, and possibly integrate them with my best model to create a hybrid-collaborative filtering model. I will also return to attempting to memory-based recommender system development with the use of distributed computing to further evaluate the results that I have seen so far.  
  
## Index
- [**CRISP-DM-Drafts**](https://github.com/mike-flanagan/recipe-book/tree/main/CRISP-DM-Drafts) — contains initial project development/data exploration file, initial EDA notebook file, and initial modeling notebook file.  
- [**code**](https://github.com/mike-flanagan/recipe-book/tree/main/code) — contains .py files of code used in notebooks.
- [**data**](https://github.com/mike-flanagan/recipe-book/tree/main/data) — contains CSVs included with the dataset 
  - **Note:** the primary datasets used in the project are not included in this directory due to file size, and are available via my S3 cloud storage at the below links:  
    - [RAW_interactions.csv](https://s3.console.aws.amazon.com/s3/object/sagemaker-studio-t1ems8mtnoj?region=us-east-2&prefix=RAW_interactions.csv) — user interactions with recipes, including the date of the interaction, as well as the user's rating and review of the recipe.  
    - [RAW_recipes.csv](https://s3.console.aws.amazon.com/s3/object/sagemaker-studio-t1ems8mtnoj?region=us-east-2&prefix=RAW_recipes.csv)  
    - [ui_ratings.csv](https://s3.console.aws.amazon.com/s3/object/sagemaker-studio-t1ems8mtnoj?region=us-east-2&prefix=ui_ratings.csv) — user-item ratings utility matrix generated from the RAW interactions.
- [**images**](https://github.com/mike-flanagan/recipe-book/tree/main/images) — contains a PDF presentation of my findings, images files used for notebook and readme header, and output visualizations which were used in the presentation slides.  
- [**models**](https://github.com/mike-flanagan/recipe-book/tree/main/models) — contains output/pickle files of models.  
- .gitignore
- [Presentation_Slides_RecipeBook.pdf](https://github.com/mike-flanagan/recipe-book/blob/main/Presentation_Slides_RecipeBook.pdf) — PDF of project presentation
- [MF_Recipe_RecSystem_Notebook.ipynb](https://github.com/mike-flanagan/recipe-book/blob/main/MF_Recipe_RecSystem_Notebook.ipynb) — primary, summative project notebook file.  
- README.md  
  
  
  
<div align="center";>Author  
  <div align="center";>Mike Flanagan  
    <div align="center";><a href="https://flanalysis.com/">flanalysis.com</a>  
  
[GitHub](https://github.com/mike-flanagan/) | [LinkedIn](https://www.linkedin.com/in/mike-flanagan-data/) | [Medium](https://mike-flanagan.medium.com/)
  
  
