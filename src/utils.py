# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 18:32:55 2025

@author: Alex
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns

from census import Census
from us import states

import sys
import os
from pathlib import Path
#sys.path.append("..")
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "config"))

import config



# Initialize the census class
c = Census(config.API_KEY)

# These are the PUMA codes specifically for Charlotte
pumas = config.pumas # ['03101', '03102', '03103', '03104', '03105']

varnames = config.varnames

locations = {'03101': 'Central',
 '03102': 'Northwest',
 '03103': 'Northeast',
 '03104': 'Southeast',
 '03105': 'Southwest'}

    
##########################
#### Query Functions #####
##########################

def query_category(cat):

    out_df = _query_pumas(varnames=varnames[cat])

    out_df['location'] = out_df['public use microdata area'].map(locations)
    
    return out_df

def _query_pumas(*, varnames, pumas=pumas):
    
    vars = ('NAME',) + tuple(varnames.values()) 

    data = []
    for puma in pumas:
        result = c.acs5.get(
            vars,
            {'for' : f'public use microdata area:{puma}', 'in': f'state:{states.NC.fips}'}
        )
        data.extend(result)
        
    df = pd.DataFrame(data)
    
    # To rename the dataframe fields using the names specified in the varnames dictionary, let's first make a reverse dictionary
    reverse_varnames = {v: k for k, v in varnames.items()}
    
    # Now use this dictionary to rename the dataframe fields if they appear
    df.rename(columns=reverse_varnames, inplace=True)
    df.columns = df.columns.str.lower() # make all lowercase
    
    return df

def query_population():

    cat = 'population'

    pop_df = query_category(cat)

    race_fields = ['white', 'black', 'indigenous', 'asian', 'pacific', 'other_race', 'two_or_more_races']
    for field in race_fields:

        pop_df[f'{field}_pct'] = pop_df[field]/pop_df['total_race']

    pop_df['hispanic_pct'] = pop_df['hispanic_yes']/pop_df['hispanic_total']
    pop_df['non_hispanic_pct'] = pop_df['hispanic_no']/pop_df['hispanic_total']

    return pop_df
    
def query_citizenship():

    cat = 'nativity'

    nat_df = query_category(cat)

    # Define which subcategories you want percentages for
    fb_nat_areas = ["europe", "asia", "africa", "oceania", "latam", "n_america"]

    # Loop through and create both total % and internal %
    for area in fb_nat_areas:
        col_nat = f"fb_nat_{area}"
        col_non = f"fb_non_{area}"

        # percentages of total
        nat_df[f"{col_nat}_pct"] = nat_df[col_nat] / nat_df["nativity_total"]
        nat_df[f"{col_non}_pct"] = nat_df[col_non] / nat_df["nativity_total"]

        # percentages within foreign born total
        nat_df[f"{col_nat}_pct_fb"] = nat_df[col_nat] / nat_df["foreign_born_total"]
        nat_df[f"{col_non}_pct_fb"] = nat_df[col_non] / nat_df["foreign_born_total"]

        nat_df[f"{col_nat}_pct_fb_nat"] = nat_df[col_nat] / nat_df["foreign_born_naturalized"]
        nat_df[f"{col_non}_pct_fb_non"] = nat_df[col_non] / nat_df["fb_non_citizen_total"]

    nat_df['native_born_pct'] = nat_df['native_born']/nat_df['nativity_total']
    nat_df['foreign_born_pct'] = nat_df['foreign_born_total']/nat_df['nativity_total']

    nat_df['fb_nat_pct'] = nat_df['foreign_born_naturalized']/nat_df['nativity_total']
    nat_df['fb_nat_pct_fb'] = nat_df['foreign_born_naturalized']/nat_df['foreign_born_total']

    nat_df['fb_non_pct'] = nat_df['fb_non_citizen_total']/nat_df['nativity_total']
    nat_df['fb_non_pct_fb'] = nat_df['fb_non_citizen_total']/nat_df['foreign_born_total']
    
    return nat_df

def query_health():

    cat = 'health'

    hth_df = query_category(cat)

    # The total people off health insurance
    hth_df['health_ins_off'] = hth_df['health_ins_0-18_off'] + hth_df['health_ins_19-34_off'] + hth_df['health_ins_35-64_off'] + hth_df['health_ins_65+_off']
    
    # The total people on health insurance
    hth_df['health_ins_on'] = hth_df['health_ins_total'] - hth_df['health_ins_off']

    # The percentage of people on vs off health insurance
    hth_df['health_ins_on_pct'] = hth_df['health_ins_on']/hth_df['health_ins_total']*100
    hth_df['health_ins_off_pct'] = hth_df['health_ins_off']/hth_df['health_ins_total']*100

    # The total people in age brackets with insurance
    for age in ['0-18', '19-34', '35-64', '65+']:

        age_total = f'health_ins_{age}_total'
        age_off  = f'health_ins_{age}_off'

        # How many of each age-bracket are ON insurance
        hth_df[f'health_ins_{age}_on'] = hth_df[age_total] - hth_df[age_off]

        # How many of each age-bracket are on or off insurance relative to the age-bracket
        hth_df[f'health_ins_{age}_off_pct_{age}'] = hth_df[age_off]/hth_df[age_total]*100
        hth_df[f'health_ins_{age}_on_pct_{age}'] = 100 - hth_df[f'health_ins_{age}_off_pct_{age}']
        
        # How many of each age bracket are off insurance relative to all people off insurance
        hth_df[f'health_ins_{age}_off_pct_off'] = hth_df[age_off]/hth_df['health_ins_off']*100
        
    return hth_df

def query_economic():
    cat = 'economic'

    df = query_category(cat)

    df['poverty_rate'] = df['poverty_below']/df['poverty_total']
    df['poverty_rate_pct'] = df['poverty_rate']*100.

    df['unemployment_rate_pct'] = df['unemployed_total']/df['labor_force_total']*100
    
    # map age groups → male/female column names
    age_groups = {
        "16_19":  ("male_16_19_in_labor",  "female_16_19_in_labor",
                   "male_16_19_not_labor", "female_16_19_not_labor"),
        "20_21":  ("male_20_21_in_labor",  "female_20_21_in_labor",
                   "male_20_21_not_labor", "female_20_21_not_labor"),
        "22_24":  ("male_22_24_in_labor",  "female_22_24_in_labor",
                   "male_22_24_not_labor", "female_22_24_not_labor"),
        "25_29":  ("male_25_29_in_labor",  "female_25_29_in_labor",
                   "male_25_29_not_labor", "female_25_29_not_labor"),
        "30_34":  ("male_30_34_in_labor",  "female_30_34_in_labor",
                   "male_30_34_not_labor", "female_30_34_not_labor"),
        "35_44":  ("male_35_44_in_labor",  "female_35_44_in_labor",
                   "male_35_44_not_labor", "female_35_44_not_labor"),
        "45_54":  ("male_45_54_in_labor",  "female_45_54_in_labor",
                   "male_45_54_not_labor", "female_45_54_not_labor"),
        "55_59":  ("male_55_59_in_labor",  "female_55_59_in_labor",
                   "male_55_59_not_labor", "female_55_59_not_labor"),
        "60_61":  ("male_60_61_in_labor",  "female_60_61_in_labor",
                   "male_60_61_not_labor", "female_60_61_not_labor"),
        "62_64":  ("male_62_64_in_labor",  "female_62_64_in_labor",
                   "male_62_64_not_labor", "female_62_64_not_labor"),
        "65_69":  ("male_65_69_in_labor",  "female_65_69_in_labor",
                   "male_65_69_not_labor", "female_65_69_not_labor"),
        "70_74":  ("male_70_74_in_labor",  "female_70_74_in_labor",
                   "male_70_74_not_labor", "female_70_74_not_labor"),
        "75plus": ("male_75plus_in_labor", "female_75plus_in_labor",
                   "male_75plus_not_labor","female_75plus_not_labor"),
    }

    for age, (m_in, f_in, m_out, f_out) in age_groups.items():
        df[f"{age}_in_labor"]  = df[m_in] + df[f_in]
        df[f"{age}_not_labor"] = df[m_out] + df[f_out]
        
        
    #####
    
    cat = 'labor_sectoral'
    df2 = query_category(cat)
    
    cat = 'transportation'
    df3 = query_category(cat)
    
    df = df.merge(
    df2, on=['name', 'location', 'public use microdata area', 'state'], how='left').merge(
    df3, on=['name', 'location', 'public use microdata area', 'state'], how='left')
    
    transport_list = ['car_alone', 'carpool', 'public_transit', 'taxi', 'motorcyle', 'bicycle', 'walked', 'other', 'work_home']
                          
    for transport_type in transport_list:
        df[f'commute_{transport_type}_pct'] = df[f'commute_{transport_type}']/df['commute_total']

    
    return df


#######################
### Misc Functions ####
#######################

'''
def _save_data(df):
    output_file = Path("raw/charlotte-puma.csv")
    output_file.parent.mkdir(exist_ok=True, parents=True)  # make sure the folder exists
    df.to_csv(output_file, index=False)
    

def run():
    
    df = _query_pumas(pumas=pumas)
    _save_data(df)
    print("Charlotte PUMA data saved! Here’s a preview:")
    print(df.head())
    
    

if __name__ == "__main__":
    run()
'''