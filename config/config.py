API_KEY = '68128fd24d42a59d5211eb6a5330bd89a7602b72'

# https://api.census.gov/data/2022/acs/acs5/variables.html
varnames =  {
    'population': {
        # --- Population basics ---
        "total_population"       : "B01003_001E",

        # --- Race ---
        "total_race"             : "B02001_001E",
        "white"                  : "B02001_002E",
        "black"                  : "B02001_003E",
        "indigenous"             : "B02001_004E",
        "asian"                  : "B02001_005E",
        "pacific"                : "B02001_006E",
        "other_race"             : "B02001_007E",
        "two_or_more_races"      : "B02001_008E",

        # --- Hispanic / Latino ethnicity ---
        "hispanic_total"         : "B03003_001E",
        "hispanic_yes"           : "B03003_003E",
        "hispanic_no"            : "B03003_002E",
        
        # --- Hispanic / Latino Races
        "white_hisp"                : "B03002_013E",
        "black_hisp"                : "B03002_014E",
        "indigenous_hisp"           : "B03002_015E",
        "asian_hisp"                : "B03002_016E",
        "pacific_hisp"              : "B03002_017E",
        "other_hisp"                : "B03002_018E",
        "two_or_more_hisp"          : "B03002_019E",   
        
        # --- Non-Hispanic Races
        "white_nonhisp"             : "B03002_003E",
        "black_nonhisp"             : "B03002_004E",
        "indigenous_nonhisp"        : "B03002_005E",
        "asian_nonhisp"             : "B03002_006E",
        "pacific_nonhisp"           : "B03002_007E",
        "other_nonhisp"             : "B03002_008E",
        "two_or_more_nonhisp"       : "B03002_009E",
    },
     
     'nativity': {

        # --- Nativity & foreign born (region of origin) ---
        "nativity_total"          : "B05002_001E",

        "native_born"             : "B05002_002E",

        "foreign_born_total"     : "B05002_013E",
        
        "foreign_born_naturalized": "B05002_014E",
        "fb_nat_europe"          : "B05002_015E",
        "fb_nat_asia"            : "B05002_016E",
        "fb_nat_africa"          : "B05002_017E",
        "fb_nat_oceania"         : "B05002_018E",
        "fb_nat_latam"           : "B05002_019E",
        "fb_nat_n_america"       : "B05002_020E",
        
        "fb_non_citizen_total"   : "B05002_021E",
        "fb_non_europe"          : "B05002_022E",
        "fb_non_asia"            : "B05002_023E",
        "fb_non_africa"          : "B05002_024E",
        "fb_non_oceania"         : "B05002_025E",
        "fb_non_latam"           : "B05002_026E",
        "fb_non_n_america"       : "B05002_027E",
    },
     
     'health': {
        # --- Health insurance coverage ---
        "health_ins_total"       : "B27010_001E",
        
        "health_ins_0-18_total"  : "B27010_002E",
        "health_ins_0-18_off"   : "B27010_017E",
        
        "health_ins_19-34_total" : "B27010_018E",
        "health_ins_19-34_off"  : "B27010_033E",
        
        "health_ins_35-64_total" : "B27010_034E",
        "health_ins_35-64_off"  : "B27010_050E",
        
        "health_ins_65+_total"   : "B27010_051E",
        "health_ins_65+_off"    : "B27010_066E",
    },
    
    'economic': {

        # --- Income & poverty ---
        "median_income"          : "B19013_001E",
        "per_capita_income"      : "B19301_001E",
        "poverty_total"          : "B17001_001E",
        "poverty_below"          : "B17001_002E",

        # --- Housing costs ---
        "median_rent"            : "B25064_001E",
        "median_rent_pct_income" : "B25071_001E",
        "median_home_value"      : "B25077_001E",


        # --- Employment status ---
        "employment_status_total": "B23025_001E",
        "labor_force_total"      : "B23025_002E",
        "labor_force_civ"        : "B23025_003E",
        "employed_total"         : "B23025_004E",
        "unemployed_total"       : "B23025_005E",
        "labor_force_mil"        : "B23025_006E",
        "not_in_labor_force"     : "B23025_007E",
        
        # --- Employment status by Age and Sex ---
        "16plus_employment_status" : "B23001_001E", 
 
        # --- Male ---
        "male_16_19_in_labor": "B23001_004E",
        "male_16_19_not_labor": "B23001_009E",

        "male_20_21_in_labor": "B23001_011E",
        "male_20_21_not_labor": "B23001_016E",

        "male_22_24_in_labor": "B23001_018E",
        "male_22_24_not_labor": "B23001_023E",

        "male_25_29_in_labor": "B23001_025E",
        "male_25_29_not_labor": "B23001_030E",

        "male_30_34_in_labor": "B23001_032E",
        "male_30_34_not_labor": "B23001_037E",

        "male_35_44_in_labor": "B23001_039E",
        "male_35_44_not_labor": "B23001_044E",

        "male_45_54_in_labor": "B23001_046E",
        "male_45_54_not_labor": "B23001_051E",

        "male_55_59_in_labor": "B23001_053E",
        "male_55_59_not_labor": "B23001_058E",

        "male_60_61_in_labor": "B23001_060E",
        "male_60_61_not_labor": "B23001_065E",

        "male_62_64_in_labor": "B23001_067E",
        "male_62_64_not_labor": "B23001_072E",

        "male_65_69_in_labor": "B23001_074E",
        "male_65_69_not_labor": "B23001_077E",

        "male_70_74_in_labor": "B23001_079E",
        "male_70_74_not_labor": "B23001_082E",

        "male_75plus_in_labor": "B23001_084E",
        "male_75plus_not_labor": "B23001_087E",

        # --- Female ---
        "female_16_19_in_labor": "B23001_090E",
        "female_16_19_not_labor": "B23001_095E",

        "female_20_21_in_labor": "B23001_097E",
        "female_20_21_not_labor": "B23001_102E",

        "female_22_24_in_labor": "B23001_104E",
        "female_22_24_not_labor": "B23001_109E",

        "female_25_29_in_labor": "B23001_111E",
        "female_25_29_not_labor": "B23001_116E",

        "female_30_34_in_labor": "B23001_118E",
        "female_30_34_not_labor": "B23001_123E",

        "female_35_44_in_labor": "B23001_125E",
        "female_35_44_not_labor": "B23001_130E",

        "female_45_54_in_labor": "B23001_132E",
        "female_45_54_not_labor": "B23001_137E",

        "female_55_59_in_labor": "B23001_139E",
        "female_55_59_not_labor": "B23001_144E",

        "female_60_61_in_labor": "B23001_146E",
        "female_60_61_not_labor": "B23001_151E",

        "female_62_64_in_labor": "B23001_153E",
        "female_62_64_not_labor": "B23001_158E",

        "female_65_69_in_labor": "B23001_160E",
        "female_65_69_not_labor": "B23001_163E",

        "female_70_74_in_labor": "B23001_165E",
        "female_70_74_not_labor": "B23001_168E",

        "female_75plus_in_labor": "B23001_170E",
        "female_75plus_not_labor": "B23001_173E",   
    },
    
    'labor_sectoral' : {

        # --- Industry (C24050) ---
        "ind_total"              : "C24050_001E",
        "ind_agriculture"        : "C24050_002E",
        "ind_construction"       : "C24050_003E",
        "ind_manufacturing"      : "C24050_004E",
        "ind_wholesale"          : "C24050_005E",
        "ind_retail"             : "C24050_006E",
        "ind_transport_ware"     : "C24050_007E",
        "ind_info"               : "C24050_008E",
        "ind_finance"            : "C24050_009E",
        "ind_professional"       : "C24050_010E",
        "in_edu_health"          : "C24050_011E",
        "ind_arts_food"          : "C24050_012E",
        "ind_other_services"     : "C24050_013E",
        "ind_public_admin"       : "C24050_014E",

        # --- Occupation groups (C24060) ---
        "occ_mgmt_business_sci"  : "C24060_002E",
        "occ_services"           : "C24060_003E",
        "occ_sales_office"       : "C24060_004E",
        "occ_nat_resources"      : "C24060_005E",
        "occ_production_transport": "C24060_006E",
    },

    'transportation' : {
        # --- Transportation to work (B08301) ---
        "commute_total"          : "B08301_001E",
        "commute_car_alone"      : "B08301_003E",
        "commute_carpool"        : "B08301_004E",
        "commute_public_transit" : "B08301_010E",
        "commute_taxi"           : "B08301_016E",
        "commute_motorcyle"      : "B08301_017E",
        "commute_bicycle"        : "B08301_018E",
        "commute_walked"         : "B08301_019E",
        "commute_other"          : "B08301_020E",
        "commute_work_home"      : "B08301_021E"
    },
}


# These are the PUMA codes specifically for Charlotte
pumas = ['03101', '03102', '03103', '03104', '03105']

