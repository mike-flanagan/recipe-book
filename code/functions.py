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
        