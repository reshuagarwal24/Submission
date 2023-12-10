#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_rows = None


# # Question 1: Distance Matrix Calculation

# In[173]:


def calculate_distance_matrix(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, index_col = 'id_start')
    df1 = pd.read_csv(file_path, index_col = 'id_end')
    
    # Create a pivot table with 'id_start', 'id_end', and 'distance'
    pivot_table = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='first', fill_value=0)
    pivot_table.insert(0, '1001400', 0.0)
    pivot_table = pivot_table.fillna(0)
    pivot_table.iloc[1,0] = pivot_table.iloc[0,1]
    
    pivot_table_transpose = df1.pivot_table(index='id_end', columns='id_start', values='distance', aggfunc='first', fill_value=0)
    pivot_table_transpose.loc['1001400'] = 0.0
    pivot_table_transpose.iloc[-1, 1] = pivot_table_transpose.iloc[0, 0]
    last_row = df.iloc[-1]

    # Shift all rows down by one position
    df.iloc[1:] = df.iloc[:-1].values

    # Assign the last row to the first position
    df.iloc[0] = last_row
   

    # Reset index if needed
    print(pivot_table_transpose)

    
#     new_row = pd.Series([, index=pivot_table_transpose.columns)

#     pivot_table_transpose.loc[-1] = '1001400'
#     pivot_table_transpose.index = pivot_table_transpose.index + 1
#     pivot_table_transpose = pivot_table_transpose.sort_index()
#     print(pivot_table)
#     print(pivot_table_transpose)
#     pivot_table_transpose = pivot_table_transpose.sort_index(ascending=True)
    distance_matrix = pivot_table + pivot_table_transpose
    return distance_matrix
file_path = 'dataset-3.csv'
distance_matrix = calculate_distance_matrix(file_path)
print(distance_matrix)


# # Question 2: Unroll Distance Matrix

# In[25]:


# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. 
# The resulting DataFrame should have three columns: columns id_start, id_end, and distance.

# All the combinations except for same id_start to id_end must be present in the rows with their distance values 
# from the input DataFrame.


# In[30]:


import pandas as pd

def unroll_distance_matrix(distance_matrix):
    unrolled_distance_matrix = distance_matrix.copy()

    unrolled_distance_matrix.reset_index(inplace=True)

    melted_distance_matrix = pd.melt(unrolled_distance_matrix, id_vars='index', var_name='id_end', value_name='distance')

    # Filter out rows where 'id_from' is equal to 'id_to'
    unrolled_distance_matrix = melted_distance_matrix[melted_distance_matrix['id_end'] != melted_distance_matrix['index']]

    unrolled_distance_matrix.columns = ['id_start', 'id_end', 'distance']

    return unrolled_distance_matrix

unrolled_distance_matrix = unroll_distance_matrix(distance_matrix)
print(unrolled_distance_matrix)


# # Question 3: Finding IDs within Percentage Threshold

# In[34]:


import pandas as pd

def find_ids_within_ten_percentage_threshold(df, reference_value):
    reference_df = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_df['distance'].mean()

    # Calculate the threshold values for 10% above and below the average
    lower_threshold = reference_average_distance * 0.9
    upper_threshold = reference_average_distance * 1.1

    # Filter the DataFrame for values within the 10% threshold
    result_df = df[(df['id_start'] != reference_value) & 
                   (df['distance'] >= lower_threshold) & 
                   (df['distance'] <= upper_threshold)]

    # Sorting the unique values from the 'id_start' column
    result_ids = sorted(result_df['id_start'].unique())

    return result_ids

reference_value = int(input())
result_ids = find_ids_within_ten_percentage_threshold(unrolled_distance_matrix, reference_value)
print(result_ids)


# # Question 4: Calculate Toll Rate

# In[35]:


import pandas as pd

def calculate_toll_rate(df):
    # Add columns for each vehicle type with their respective rate coefficients
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df

# Example usage (using the unrolled_distance_matrix from the previous question):
toll_rate_df = calculate_toll_rate(unrolled_distance_matrix)
print(toll_rate_df)


# In[ ]:




