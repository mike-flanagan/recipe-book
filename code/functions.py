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
        