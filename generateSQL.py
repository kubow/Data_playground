from pathlib import Path

def generate_single_SQL(file_name, file_location):
    return f"CREATE OR REPLACE TABLE main.{file_name} AS \nFROM read_csv('{file_location}');"

with open('./SQL.sql', 'w') as sql:
    for fle in Path('.').glob('*.csv'):
        print(generate_single_SQL(str(fle).split('.')[0], f"{l}{fle}"))
        #sql.write(generate_single_SQL(fle, f"{l}{fle}"))
        
        
