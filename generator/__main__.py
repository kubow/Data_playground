from datetime import datetime, timedelta
from faker import Faker
import numpy as np
import pandas as pd
from random import choice, randint
from tui import file_selector
from yaml import safe_load

# Initialize Faker + Random Seed (generally available)
fake = Faker()
np.random.seed(42)

def generate_value(column):
    col_type = column['type']
    possible_values = column['possible_values']

    if possible_values == 'random_numbers':
        return randint(column['min'], column['max'])

    elif possible_values == 'fake_name':
        return fake.name()

    elif possible_values == 'fake_date':
        return fake.date()

    elif isinstance(possible_values, list):
        return choice(possible_values)

    else:
        raise ValueError(f"Unknown possible value type: {possible_values}")

# Function to generate multiple data points
def generate_column_data(column, num_records):
    col_type = column['type']
    possible_values = column['possible_values']

    if isinstance(possible_values, list):
        print(f"variation between {column['possible_values']}")
        return np.random.choice(column['possible_values'], num_records)
    
    elif col_type == 'int':
        return np.random.randint(column['min'], column['max'] + 1, num_records)
    
    elif col_type == 'float':
        return np.random.uniform(column['min'], column['max'], num_records)
    
    elif col_type == 'string':
        return np.random.choice(column['possible_values'], num_records)

    else:
        raise ValueError(f"Unknown type {col_type} for column {column['column_name']}")

def generate_dataset(yaml_file, num_records):
    # Load the YAML file
    with open(yaml_file, 'r') as file:
        config = safe_load(file)
    
    # Generate data
    if config['type'] == 'timeseries':
        # https://llego.dev/posts/pandas-generating-time-series-data-python/
        dti = pd.date_range(datetime.now() - timedelta(days=num_records), datetime.now(), freq='1min')
        #dti = pd.date_range(datetime.now() - timedelta(days=100), datetime.now(), freq='1min')
        data = {}
        for column in config['columns']:
            if column['column_name'] == 'timestamp':  # or column == 'prod_line':
                continue  # timestamp is index of the dataframe
            else:
                data[column['column_name']] = generate_column_data(column, len(dti))
        df = pd.DataFrame(data, index=dti)
    else:
        data = {column['column_name']: [generate_value(column) for _ in range(num_records)]
            for column in config['columns']}

        # Convert to DataFrame
        df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    yaml_file = file_selector()
    num_records = 50
    df = generate_dataset(yaml_file, num_records)

    # Display the generated dataset
    print(df.head())

    # Optionally, save to a CSV file
    df.to_csv(f'./output/{yaml_file.name.replace('.yaml', '')}.csv', index=True)
