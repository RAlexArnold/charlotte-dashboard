# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 19:31:46 2025

@author: Alex
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import sys

base_path = Path("../")

sys.path.append(os.path.join(base_path, 'src'))

import plot_utils as plots

import streamlit as st

output_file = base_path / "data" / "raw" / "charlotte-puma.csv"

map_file = base_path / "data" / "raw" / "charlotte_puma_reference.png"

# --- Load Data ---

@st.cache_data
def load_data():

    df = pd.read_csv(output_file)
    return df



# --- Demographic Plots ---
def st_population(df):
    st.write('**Population** - Each PUMA has roughly equal population between 120,000 and 160,000.')
    f, ax = plt.subplots()
    sns.barplot(df, x='location', y='total_population')
    #ax.tick_params(axis='x', labelrotation=90)
    ax.set_xlabel('Location')
    ax.set_ylabel('Population')
    ax.set_title('Population by PUMA Location')
    st.pyplot(f)

def st_race_plot(df):
    st.write('**Race Makeup of Charlotte** - We can see a *polarization* between North and South Charlotte.')
    fig = plots.race_pie_chart(df)#, title_fs=20, wedge_fs=14)
    st.pyplot(fig)
    
def st_hispanic_plot(df):
    st.write('**Hispanic vs. Non-Hispanic**')
    fig = plots.plot_hispanic(df)
    st.pyplot(fig)
    
def st_hispanic_race(df):
    st.write('**Race Makeup of People Identifying as Hispanic** - The pie chart for each region sums to the number of Hispanic people. Hispanic people in North Charlotte often identify as *Other* more often than Hispanic people in South Charlotte who are more likely to identify as *Two or More* races or as *White*.')
    fig = plots.plot_hispanic_race(df)
    st.pyplot(fig)
    
def st_citizenship(df):
    st.write('**Citizenship of People** - The Northeast and Southwest have the highest number of non-US citizens.')
    fig = plots.nativity_pie_chart(df, version='simple')
    st.pyplot(fig)
    
def st_origin(df):
    st.write('**Origin of Non-US Citizens** - Pie chart of each region sums to the number of non-US citizens. We can see that most non-US citizens are of *Latin American* origin, except in the Southeast region where most originate from *Asia*. But recall that the Southeast has the least number of non-US citizens (7%).')
    fig = plots.nativity_pie_chart(df, version='non-citizens')
    st.pyplot(fig)

# --- Health Plots ---    
def st_insurance(df):
    st.write('**What Percent of People Have Health Insurance** - Roughly equal percentage in each region (15-17%) except for the Southeast where only 6% of people do not have insurance.')
    fig = plots.plot_insurance(df, cmap_name='Paired')
    st.pyplot(fig)
    
def st_no_insurance(df):
    st.write('**The Ages of Those with No Insurance** - We can see that most people off insurance are between the ages of **35 and 64**, with the **19 to 34** age group a close second. Around 17% of children are not covered by insurance. The pie chart for each region sums to the number of people *without* insurance.')
    fig= plots.plot_no_insurance(df, cmap_name='tab20c')
    st.pyplot(fig)
    
def st_stacked_insurance(df):
    st.write('**Age Breakdown of Health Insurance Status** - This shows the number of people on insruanced (green) and off insurance (red) for each age bracket.')
    fig = plots.plot_stacked_health_insurance(df, 'Health Insurance Status', normalize=False)
    st.pyplot(fig)
    
def st_stacked_insurance_norm(df):
    st.write('**Age Breakdown of Health Insurance Status** - This is the same data as above, but here each age group is normalized, i.e. sums to 100% so you can see what *percentage* in each age group is on vs. off insurance.')
    fig = plots.plot_stacked_health_insurance(df, 'Health Insurance Status', normalize=True)
    st.pyplot(fig)
    
# --- Economy Plots ---
def st_industry(df):
    st.write('**Industry Composition** - *Education/Health*, *Administration*, and *Retail* are common in the North. While *Finance*, *Administration*, and *Education* is common in the South.')
    fig = plots.plot_industry(df)
    st.pyplot(fig)

def st_occupation(df):    
    st.write('**Occupation Composition** - This is an alternative way of classifying workers based off the *nature of the occupation* instead of the industry. We can see that *Production/Transportation* is more common in the North than in the South. *Management*, *Sales*, and *Services* are common in all regions, but *Magagement* dominates in the Southeast.')
    fig = plots.plot_occupation(df)
    st.pyplot(fig)
    
def st_employment_status(df):
    st.write('**Employment Status** - Shows the number of people *in the labor force* (split into **employed** and **military**) vs. *not in the labor force*. The next plots will investigate those not in the labor force further.')
    fig = plots.plot_employment_status(df)
    st.pyplot(fig)
    
def st_stacked_labor_force(df):
    st.write('**Employment Status by Age Group** - Shows the number of people *in the labor force* in green vs those *not in the labor force* in red for each age bracket.')
    fig = plots.plot_stacked_labor_force(df, "Employment Status by Age Group", normalize=False)
    st.pyplot(fig)
    
def st_stacked_labor_force_norm(df):
    st.write('**Employment Status by Age Group** - This is the same data as above, but here each age group is normalized, i.e. sums to 100% so the percentages in eage age group are easier to read. We can see that the percent of each age bracket not in the labor force starts to drop for ages over 50.')
    fig = plots.plot_stacked_labor_force(df, "Employment Status by Age Group (Normalized)", normalize=True)
    st.pyplot(fig)
    
def st_income(df):
    st.write('**The Median Income of Each Region** - The Northwest has the lowest median income at less than \$50,000 while the Souteast has the highest with more than \$120,000!')
    fig, ax = plt.subplots()
    sns.barplot(df, x='location', y='median_income')
    ax.set_xlabel('Location')
    ax.set_ylabel('Median Income ($)')
    ax.set_title('Median Income by Location')
    st.pyplot(fig)
    
def st_unemployment(df):
    st.write('**The Unemployment Rate of Each Region**')
    fig, ax = plt.subplots()
    sns.barplot(df, x='location', y='unemployment_rate_pct')
    ax.set_xlabel('Location')
    ax.set_ylabel('Unemployment Rate (%)')
    ax.set_title('Unemployment Rate by Location')
    st.pyplot(fig)
    
def st_poverty(df):
    st.write('**The Poverty Rate of Each Region**')
    fig,ax = plt.subplots()
    sns.barplot(df, x='location', y='median_rent')
    ax.set_xlabel('Location')
    ax.set_ylabel('Median Rent ($)')
    ax.set_title('Rent by Location')
    st.pyplot(fig)
    
def st_rent(df):
    st.write('**The Rent as a Percent of Income for Each Region**')
    fig,ax = plt.subplots()
    sns.barplot(df, x='location', y='median_rent_pct_income')
    ax.set_xlabel('Location')
    ax.set_ylabel('Median Rent as % Income')
    ax.set_title('Rent as Percent of Income by Location')
    st.pyplot(fig)
    
def st_transport(df):
    st.write("**How do People Get to Work in Each Region** - We can see that most *drive alone* to work, and about a quarter *work from home*. About 10% *carpool*. Most don't use *Public Transportation* in the city. Less than 3% of people in most regions use a *bus*, *tram*, or *train*.")
    fig = plots.plot_transportation(df, cmap_name='tab10')
    st.pyplot(fig)
    
    
    

    

df = load_data()

# --- Page Layout ---
st.title('Charlotte PUMA Data Dashboard')
st.write('Overview of Demographics, Healthcare, Economy for the Five Regions of Charlotte')

tab1, tab2, tab3, tab4 = st.tabs(["Demographics", "Health", "Economy", "Reference Map"])

with tab1:
    st.header('Demographics')
    
    st_population(df)
    st_race_plot(df)
    st_hispanic_plot(df)
    st_hispanic_race(df)
    st_citizenship(df)
    st_origin(df)
    
    
with tab2:
    st.header('Health')
   
    st_insurance(df)   
    st_no_insurance(df)
    st_stacked_insurance(df)
    st_stacked_insurance_norm(df)

with tab3:
    st.header('Economy')
    
    st_income(df)
    st_unemployment(df)
    st_employment_status(df)
    st_stacked_labor_force(df)
    st_stacked_labor_force_norm(df)
    st_poverty(df)
    st_rent(df)
    st_industry(df)
    st_occupation(df)
    st_transport(df)
    
with tab4:
    st.header('Reference PUMA Map')
    
    st.write('This dashboard assigns *PUMA 3703102* as **Northwest**, *PUMA 3703103* as **Northeast**, *PUMA 3703101* as **Central**, *PUMA 3703104* as **Southeast**, and *PUMA 3703105* as **Southwest**.')
    st.image(map_file, caption='Charlotte PUMAs', use_container_width=True)
    
    





