# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 19:34:17 2025

@author: Alex
"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

##########################
### Plotting Functions ###
##########################


def race_pie_chart(df, annotate=True, min_pct_label=5, cmap_name="Set2", wedge_fs=14, title_fs=20, legend_fs=10):
    # race columns + labels
    race_cols = ['white_pct', 'black_pct', 'asian_pct', 
                 'indigenous_pct', 'pacific_pct', 
                 'other_race_pct', 'two_or_more_races_pct']

    race_labels = ["White", "Black", "Asian", 
                   "Indigenous", "Pacific", 
                   "Other", "Two+ Races"]

    # generate colors dynamically from colormap
    cmap = plt.colormaps[cmap_name]
    colors = cmap(np.linspace(0, 1, len(race_cols)))

    # GridSpec layout (center + 4 quadrants)
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    positions = {
        'Northwest': (0, 0),
        'Northeast': (0, 2),
        'Central': (1, 1),
        'Southwest': (2, 0),
        'Southeast': (2, 2),
    }

    axes = {}
    for loc, (row, col) in positions.items():
        ax = fig.add_subplot(gs[row, col])
        axes[loc] = ax

        row_data = df[df['location'] == loc][race_cols].iloc[0]

        if not annotate:
            wedges, texts, autotexts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct='%1.0f%%',
                startangle=90
            )
        else:
            wedges, texts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct=None,
                startangle=90
            )
            total = row_data.sum()
            for i, wedge in enumerate(wedges):
                pct = 100 * row_data.iloc[i] / total
                if pct >= min_pct_label:
                    ang = (wedge.theta2 + wedge.theta1) / 2
                    x = wedge.r * 0.7 * np.cos(np.deg2rad(ang))
                    y = wedge.r * 0.7 * np.sin(np.deg2rad(ang))
                    ax.text(x, y, f"{pct:.0f}%", ha="center", va="center", fontsize=wedge_fs)

        ax.set_title(loc, fontsize=title_fs)

    # Add one legend outside of plot
    fig.legend(
        race_labels, loc="center left", bbox_to_anchor=(1, 0.5),
        title="Race", fontsize=legend_fs
    )

    plt.tight_layout()
    #plt.show()
    
    return fig
    
def nativity_pie_chart(df, version="simple", annotate=True, min_pct_label=5, cmap_name="Set3", wedge_fs=14, title_fs=20, legend_fs=10):
    """
    version="simple" → native vs. foreign born
    version="non-citizens" → foreign born broken into regions
    """

    if version == "simple":
        cols = ["native_born_pct", "fb_nat_pct", "fb_non_pct"]
        labels = [
            "People who are Native-Born Citizen",
            "People who are Naturalized Citizens",
            "People who are Non-US Citizens"
        ]
        
        title = 'Citizenship Status'

    elif version == "non-citizens":
        cols = [
            'fb_non_europe_pct_fb_non',
            'fb_non_asia_pct_fb_non',
            'fb_non_africa_pct_fb_non',
            'fb_non_oceania_pct_fb_non',
            'fb_non_latam_pct_fb_non',
            'fb_non_n_america_pct_fb_non'
        ]
        
        labels = [
            "Europe",
            "Asia",
            "Africa",
            "Oceania",
            "Latin America",
            "Northern America"
        ]
        
        title = 'Origin of Non-Citizens'
            
    else:
        raise ValueError("version must be 'simple' or 'non-citizens'")

    # generate colormap
    cmap = plt.colormaps[cmap_name]
    colors = cmap(np.linspace(0, 1, len(cols)))

    # grid structure same as race chart
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    positions = {
        'Northwest': (0, 0),
        'Northeast': (0, 2),
        'Central': (1, 1),
        'Southwest': (2, 0),
        'Southeast': (2, 2),
    }

    axes = {}
    for loc, (row, col) in positions.items():
        ax = fig.add_subplot(gs[row, col])
        axes[loc] = ax

        row_data = df[df['location'] == loc][cols].iloc[0]

        if not annotate:
            wedges, texts, autotexts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct='%1.0f%%',
                startangle=90
            )
        else:
            wedges, texts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct=None,
                startangle=90
            )
            total = row_data.sum()
            for i, wedge in enumerate(wedges):
                pct = 100 * row_data.iloc[i] / total
                if pct >= min_pct_label:
                    ang = (wedge.theta2 + wedge.theta1) / 2
                    x = wedge.r * 0.7 * np.cos(np.deg2rad(ang))
                    y = wedge.r * 0.7 * np.sin(np.deg2rad(ang))
                    ax.text(x, y, f"{pct:.0f}%", ha="center", va="center", fontsize=wedge_fs)

        ax.set_title(loc, fontsize=title_fs)

    # One legend outside
    fig.legend(
        labels, loc="center left", bbox_to_anchor=(1, 0.5),
        title=title, fontsize=legend_fs
    )

    plt.tight_layout()
    
    return fig

    
    
def plot_pie_map(df, title, cols, labels, cmap_name="Set2", annotate=True, min_pct_label=5, wedge_fs=14, title_fs=20, legend_fs=10):
    """
    Plot pie charts for each PUMA in a 3x3 grid layout.
    
    Parameters
    ----------
    df : DataFrame
        Your data, with one row per location and columns matching `cols`.
    title : str
        Title for the legend.
    cols : list of str
        Column names to plot.
    labels : list of str
        Labels for legend entries.
    cmap_name : str
        Name of the Matplotlib colormap to use (default "Set2").
    annotate : bool
        If True, manually annotate slices with percentages (default True).
    min_pct_label : float
        Minimum % value for annotation to avoid clutter.
    """

    # choose colors from colormap
    cmap = plt.colormaps[cmap_name]
    colors = cmap(np.linspace(0, 1, len(cols)))

    # grid structure same as race chart
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    positions = {
        'Northwest': (0, 0),
        'Northeast': (0, 2),
        'Central': (1, 1),
        'Southwest': (2, 0),
        'Southeast': (2, 2),
    }

    axes = {}
    for loc, (row, col) in positions.items():
        ax = fig.add_subplot(gs[row, col])
        axes[loc] = ax

        row_data = df[df['location'] == loc][cols].iloc[0]

        if not annotate:
            wedges, texts, autotexts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct='%1.0f%%',
                startangle=90
            )
        else:
            wedges, texts = ax.pie(
                row_data,
                labels=None,
                colors=colors,
                autopct=None,
                startangle=90
            )
            total = row_data.sum()
            for i, wedge in enumerate(wedges):
                pct = 100 * row_data.iloc[i] / total
                if pct >= min_pct_label:
                    ang = (wedge.theta2 + wedge.theta1) / 2
                    x = wedge.r * 0.7 * np.cos(np.deg2rad(ang))
                    y = wedge.r * 0.7 * np.sin(np.deg2rad(ang))
                    ax.text(x, y, f"{pct:.0f}%", ha="center", va="center", fontsize=wedge_fs)

        ax.set_title(loc, fontsize=title_fs)

    # One legend outside
    fig.legend(
        labels, loc="center left", bbox_to_anchor=(1, 0.5),
        title=title, fontsize=legend_fs
    )

    plt.tight_layout()
    #plt.show()
    
    return fig
    
def plot_hispanic(df, cmap_name='tab10', **kwargs):

    cols = ['hispanic_pct', 'non_hispanic_pct']
    labels = ['Hispanic', 'Non-Hispanic']

    fig = plot_pie_map(df, title='Hispanic/Non-Hispanic', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)

    return fig

    
def plot_hispanic_race(df, cmap_name='Set3', **kwargs):

    cols = ['white_hisp', 'black_hisp', 'indigenous_hisp', 'asian_hisp', 'pacific_hisp', 'other_hisp', 'two_or_more_hisp']
    labels = ['White (Hispanic)', 'Black (Hispanic)', 'Indigenous (Hispanic)', 'Asian (Hispanic)', 'Oceanian (Hispanic)', 'Other (Hispanic)', 'Two+ (Hispanic)']

    fig = plot_pie_map(df, title='Hispanic Race', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)

    return fig

def plot_employment_status(df, cmap_name='Set3', min_cpt_label=2, **kwargs):

    cols = ['employed_total', 'unemployed_total', 'labor_force_mil', 'not_in_labor_force', ]  #['labor_foce_civ', 'unemployed_total', 'labor_force_mil', 'not_in_labor_force']
    labels = ['Employed (In Labor Force)', 'Unemployed (In Labor Force)', 'Military (In Labor Force)', 'Not in Labor Force']    #['Civilian Labor Force', 'Unemployed', 'Military', 'Not in Labor Force']

    fig = plot_pie_map(df, title='Employment Status (Age 16+)', cols=cols, labels=labels, cmap_name=cmap_name, min_pct_label=min_cpt_label, **kwargs)
    
    return fig

def plot_stacked_labor_force(df, title, normalize=False, title_fs=20):
    """
    For each PUMA location, plot a stacked bar chart:
    x-axis = age groups
    y-axis = total number of people
    bars split between 'in labor force' and 'not in labor force'.
    """

    age_groups = ['16_19', '20_21', '22_24', '25_29', '30_34', 
                  '35_44', '45_54', '55_59', '60_61', '62_64', 
                  '65_69', '70_74', '75plus']

    age_labels = ['16–19','20–21','22–24','25–29','30–34',
                  '35–44','45–54','55–59','60–61','62–64',
                  '65–69','70–74','75+']

    colors = ["#4daf4a", "#e41a1c"]  # green = in labor, red = not in labor

    # same grid as pie maps
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    positions = {
        'Northwest': (0, 0),
        'Northeast': (0, 2),
        'Central':   (1, 1),
        'Southwest': (2, 0),
        'Southeast': (2, 2),
    }

    axes = {}
    for loc, (row, col) in positions.items():
        ax = fig.add_subplot(gs[row, col])
        axes[loc] = ax

        # subset the row for this location
        row_data = df[df['location'] == loc].iloc[0]

        in_labor  = [row_data[f"{age}_in_labor"] for age in age_groups]
        not_labor = [row_data[f"{age}_not_labor"] for age in age_groups]
        
        if normalize:
            totals = [i + j for i, j in zip(in_labor, not_labor)]
            in_labor  = [i / t * 100 if t > 0 else 0 for i, t in zip(in_labor, totals)]
            not_labor = [j / t * 100 if t > 0 else 0 for j, t in zip(not_labor, totals)]
            ylabel = "Percent"
        else:
            ylabel = "Population"

        x = np.arange(len(age_groups))

        ax.bar(x, in_labor, color=colors[0], label="In Labor Force")
        ax.bar(x, not_labor, bottom=in_labor, color=colors[1], label="Not in Labor Force")

        ax.set_title(loc, fontsize=20)
        ax.set_xticks(x)
        ax.set_xticklabels(age_labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)

    # one legend for all
    fig.legend(["In Labor Force", "Not in Labor Force"], 
               loc="center left", bbox_to_anchor=(1, 0.5), title="Status")

    fig.suptitle(title, fontsize=title_fs)
    plt.tight_layout()
    
    return fig
    
def plot_industry(df, cmap_name='tab20', **kwargs):

    cols = ["ind_agriculture",     
            "ind_construction",    
            "ind_manufacturing",    
            "ind_wholesale" ,   
            "ind_retail"           ,
            "ind_transport_ware"   ,
            "ind_info"          ,
            "ind_finance"        , 
            "ind_professional"    ,
            "in_edu_health"       ,
            "ind_arts_food"      ,
            "ind_other_services"  ,
            "ind_public_admin" ]

    labels = ["Agriculture"        ,
            "Construction"       ,
            "Manufacturing"      ,
            "Wholesale"          ,
            "Retail"             ,
            "Transportion/Warehousing"    ,
            "Information"               ,
            "Finance"            ,
            "Administrative/Support/Waste Management"    ,
            "Education/Health"         ,
            "Arts/Entertainment/Food"        ,
            "Other Services"    ,
            "Public Administration" ]

    fig = plot_pie_map(df, title='Industry', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)

    return fig

def plot_occupation(df, cmap_name='Set3', **kwargs):

    cols = ["occ_mgmt_business_sci", 
            "occ_services",
            "occ_sales_office",
            "occ_nat_resources",
            "occ_production_transport"]



    labels = ["Management/Business/Science/Arts",
            "Services",
            "Sales and other Office Work",
            "Natural Resources/Construction/Maintenance",
            "Production/Transportation" ]

    fig = plot_pie_map(df, title='Occupation', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)    

    return fig

def plot_insurance(df, cmap_name='Paired', **kwargs):

    cols = ['health_ins_on_pct', 'health_ins_off_pct']
    labels = ['On Health Insurance', 'Off Health Insurance']

    fig = plot_pie_map(df, title='Health Insurance', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)

    return fig

def plot_no_insurance(df, cmap_name='tab20c', **kwargs):

    cols = ['health_ins_0-18_off_pct_off', 'health_ins_19-34_off_pct_off', 'health_ins_35-64_off_pct_off', 'health_ins_65+_off_pct_off']
    labels = ['0-18', 
              '19-34',
             '35-64',
             '65+']

    fig = plot_pie_map(df, title='Those with no Health Insurance', cols=cols, labels=labels, cmap_name=cmap_name, **kwargs)
    
    return fig

def plot_stacked_health_insurance(df, title, normalize=True, title_fs=20):
    """
    For each PUMA location, plot a stacked bar chart:
    x-axis = age groups
    y-axis = total number of people (or % if normalize=True)
    bars split between 'on health insurance' and 'off health insurance'.
    """

    age_groups = ['0-18', '19-34', '35-64', '65+']
    age_labels = age_groups

    colors = ["#4daf4a", "#e41a1c"]  # green = insured, red = uninsured

    # same grid as pie maps
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    positions = {
        'Northwest': (0, 0),
        'Northeast': (0, 2),
        'Central':   (1, 1),
        'Southwest': (2, 0),
        'Southeast': (2, 2),
    }

    axes = {}
    for loc, (row, col) in positions.items():
        ax = fig.add_subplot(gs[row, col])
        axes[loc] = ax

        # subset the row for this location
        row_data = df[df['location'] == loc].iloc[0]

        insured  = [row_data[f'health_ins_{age}_on']  for age in age_groups]
        uninsured = [row_data[f'health_ins_{age}_off'] for age in age_groups]

        if normalize:
            totals = [i + j for i, j in zip(insured, uninsured)]
            insured  = [i / t * 100 if t > 0 else 0 for i, t in zip(insured, totals)]
            uninsured = [j / t * 100 if t > 0 else 0 for j, t in zip(uninsured, totals)]
            ylabel = "Percent"
        else:
            ylabel = "Population"

        x = np.arange(len(age_groups))

        ax.bar(x, insured, color=colors[0], label="Insured")
        ax.bar(x, uninsured, bottom=insured, color=colors[1], label="Uninsured")

        ax.set_title(loc, fontsize=20)
        ax.set_xticks(x)
        ax.set_xticklabels(age_labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel(ylabel)

        if normalize:
            ax.set_ylim(0, 100)

    # one legend for all
    fig.legend(["Insured", "Uninsured"], 
               loc="center left", bbox_to_anchor=(1, 0.5), title="Status")

    fig.suptitle(title, fontsize=title_fs)
    plt.tight_layout()
    
    return fig

def plot_transportation(df, cmap_name='tab10', **kwargs):

    transport_list = ['car_alone', 'carpool', 'public_transit', 'taxi', 'motorcyle', 'bicycle', 'walked', 'other', 'work_home']           
    cols = []
    for transport in transport_list:
        colname = f'commute_{transport}_pct'
        cols.append(colname)
    labels = ['Drive Alone', 'Carpool', 'Public Transit', 'Taxi', 'Motorcyle', 'Bicycle', 'Walk', 'Other', 'Work from Home']   

    fig = plot_pie_map(df, title='How do People Get to Work?', cols=cols, labels=labels, cmap_name=cmap_name, annotate=True, min_pct_label=3, **kwargs)

    return fig