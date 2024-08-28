# filename: verify_csv.py

import pandas as pd

# Read the CSV file
df = pd.read_csv('table_data.csv')

# Display the full contents of the DataFrame
with pd.option_context('display.max_colwidth', None):
    print(df.to_string(index=False))