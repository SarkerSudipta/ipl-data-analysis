'''
Analytics:
1. How many times has batting first team won?
2. How many times has toss winner won?
'''

import pandas as pd

df = pd.read_csv("../data/processed/matches_table.csv")

print(df.dtypes)