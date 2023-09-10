import requests
import pandas as pd

# The API endpoint for the CA LMID LAUS dataset
endpoint = "https://data.edd.ca.gov/resource/e6gw-gvii.json"

# Initialize an empty list to store all the data
all_data = []

# Set the initial parameters for pagination (if applicable)
params = {"$limit": 1000, "$offset": 0}

while True:
    # Make the HTTP request with the current parameters
    response = requests.get(endpoint, params=params)

    # Check the response status code
    if response.status_code != 200:
        # The request failed, so print an error message
        print(f"Error fetching data from {endpoint}: {response.status_code}")
        break
    
    # The request was successful, so get the JSON data
    data = response.json()
    
    # Add the current batch of data to the all_data list
    all_data.extend(data)
    
    # Check if there is more data to retrieve
    if len(data) < 1000:
        break
    
    # Update the offset for the next request
    params["$offset"] += 1000

# Create the dataframe and filter records
df = pd.DataFrame(all_data)
df = df.query('area_name == "San Diego-Carlsbad MSA" and year >= "2018" and seasonally_adjusted_y_n == "N"')

# define data type dicionary and update data frame
dtypes = {
    'area_name' : 'str',
    'date': 'datetime64[ns]',
    'year': 'int',
    'month': 'str',
    'labor_force': 'str',
    'employment': 'str',
    'unemployment': 'int',
    'unemployment_rate': 'float'}

df = df.astype(dtypes)

# sort data frame and select columns
df = df.sort_values(by='date')
cols = list(dtypes.keys())
df = df[cols]