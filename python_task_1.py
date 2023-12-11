#!/usr/bin/env python
# coding: utf-8

# In[69]:


import pandas as pd


# In[75]:


df = pd.read_csv('dataset-1.csv', index_col='id_1')


# # Question 1: Car Matrix Generation

# In[76]:


def generate_car_matrix(file_path):
    df = pd.read_csv(file_path, index_col='id_1')

    car_matrix = pd.pivot_table(df, values='car', index='id_1', columns='id_2', aggfunc='first', fill_value=0)

    return car_matrix

file_path = 'dataset-1.csv'

matrix_result = generate_car_matrix(file_path).round(1)

print(matrix_result)


# # Question 2: Car Type Count Calculation

# In[72]:


import pandas as pd

def get_type_count(file_path):
    df = pd.read_csv(file_path)

    df['car_type'] = 'low'
    df.loc[df['car'] > 15, 'car_type'] = 'medium'
    df.loc[df['car'] > 25, 'car_type'] = 'high'

    type_count = df['car_type'].value_counts().sort_index()
    type_count = type_count.to_dict()
    return type_count

file_path = 'dataset-1.csv'
result = get_type_count(file_path)

print(result)


# # Question 3: Bus Count Index Retrieval

# In[73]:


import pandas as pd

def get_bus_indexes(file_path):
    df = pd.read_csv(file_path)

    # Calculate the mean value of the 'bus' column
    mean_bus = df['bus'].mean()
            
    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

file_path = 'dataset-1.csv'

result = get_bus_indexes(file_path)

print(result)


# # Question 4: Route Filtering

# In[107]:


# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function
# should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

def filter_routes(file_path):
    df = pd.read_csv(file_path)
    
    grouped_df = df.groupby('route')['truck'].mean()
    
    routes_above_average = grouped_df[grouped_df > 7].index.to_list()
    return routes_above_average
    
file_path = 'dataset-1.csv'
result = filter_routes(file_path)
result


# # Question 5: Matrix Value Modification

# In[114]:


def multiply_matrix(matrix_result):
    modified_matrix = matrix_result.copy()
    modified_matrix = modified_matrix.applymap(lambda x : x*0.75 if x>20 else x*1.25)
    modified_matrix = modified_matrix.fillna(0)
    
    return modified_matrix.round(1)
multiply_matrix(matrix_result)


# # Question 6: Time Check

# In[115]:


# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). 
# The goal is to verify the completeness of the time data by checking whether the timestamps 
# for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) 
# and span all 7 days of the week (from Monday to Sunday).
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair
# has incorrect timestamps. The boolean series must have multi-index (id, id_2).


# In[128]:


pd.options.display.max_columns = None
pd.options.display.max_rows = None
data = pd.read_csv('dataset-2.csv', index_col = 'id')
data = data.sort_values(by='id_2').fillna(1)
data


# In[138]:


import pandas as pd

def verify_timestamps_completeness(df):
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')

    df = df[df['id_2'] != -1]

    # Grouped by (id, id_2) and checked completeness
    completeness_series = df.groupby(['id', 'id_2']).apply(check_completeness)

    return completeness_series

def check_completeness(group):
    # Check 24-hour period
    time_diff = group['end_datetime'].max() - group['start_datetime'].min()
    full_day_coverage = time_diff >= pd.Timedelta(days=1)

    # Check 7 days of the week
    span_check = len(group['start_datetime'].dt.dayofweek.unique())== 7

    # Return True if both conditions are met, checking completeness
    return full_day_coverage and span_check

df = pd.read_csv('dataset-2.csv')

span_check = verify_timestamps_completeness(df)

print(completeness_series)


# In[ ]:


def calculate_distance_matrix(file_path):
    
file_path = 'dataset-3.csv'
calculate_distance_matrix(file_path)

