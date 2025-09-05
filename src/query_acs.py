# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 17:58:32 2025

@author: Alex
"""

'''
Query Each Type of Data. Then Save as DataFrame for later
'''

from pathlib import Path
from utils import *

# Add the config folder to sys.path
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))

#import config


def run_query():

    # Population Data
    pop_df = query_population()
    
    # Citizenship Data
    nat_df = query_citizenship()
    
    # Health Data
    hth_df = query_health()
    
    # Economic Data
    eco_df = query_economic()
    
    # Merge All
    df = pop_df.merge(
        nat_df, on=['name', 'location', 'public use microdata area', 'state'], how='left').merge(
        hth_df, on=['name', 'location', 'public use microdata area', 'state'], how='left').merge(
        eco_df, on=['name', 'location', 'public use microdata area', 'state'], how='left')
            
        
    return df
            
def save_file(df):
    
    output_file = Path("data/raw/charlotte-puma.csv")
    output_file.parent.mkdir(exist_ok=True, parents=True)  # make sure the folder exists
    df.to_csv(output_file, index=False)
    
df = run_query()
save_file(df)

