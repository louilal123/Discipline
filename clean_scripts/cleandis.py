import pandas as pd
import numpy as np

# Define cleaner column names
clean_columns = {
    'State': 'state',
    'Total Students': 'total_students',
    'American Indian or Alaska Native Number': 'native_am_num',
    'American Indian or Alaska Native Percent': 'native_am_pct',
    'Asian Number': 'asian_num',
    'Asian Percent': 'asian_pct',
    'Hispanic or Latino of any race Number': 'hispanic_num',
    'Hispanic or Latino of any race Percent': 'hispanic_pct',
    'Black or African American Number': 'black_num',
    'Black or African American Percent': 'black_pct',
    'White Number': 'white_num',
    'White Percent': 'white_pct',
    'Native Hawaiian or Other Pacific Islander Number': 'pacific_islander_num',
    'Native Hawaiian or Other Pacific Islander Percent': 'pacific_islander_pct',
    'Two or more races Number': 'mixed_race_num',
    'Two or more races Percent': 'mixed_race_pct',
    'Students With Disabilities Served Under IDEA Number': 'idea_disabilities_num',
    'Students With Disabilities Served Under IDEA Percent': 'idea_disabilities_pct',
    'Students With Disabilities Served Only Under Section 504 Number': 'section504_disabilities_num',
    'Students With Disabilities Served Only Under Section 504 Percent': 'section504_disabilities_pct',
    'English Language Learners Number': 'ell_num',
    'English Language Learners Percent': 'ell_pct',
    'Number of Schools': 'schools_num',
    'Percent of Schools Reporting': 'schools_reporting_pct'
}

def clean_value(x):
    """Convert date-formatted numbers (01-Mar) to numeric"""
    if isinstance(x, str) and '-' in x:
        try:
            # Try to get the day part (before '-')
            return float(x.split('-')[0])
        except:
            return np.nan
    return x

def clean_education_data(filepath):
    # Read the CSV
    df = pd.read_csv(filepath)
    
    # Clean column names
    df = df.rename(columns=clean_columns)
    
    # Fix date-formatted numbers
    for col in df.columns:
        if col != 'state':
            df[col] = df[col].apply(clean_value)
    
    # Convert to numeric
    numeric_cols = [col for col in df.columns if col != 'state']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Ensure percentages are 0-100 (not 0-1)
    pct_cols = [col for col in df.columns if 'pct' in col]
    for col in pct_cols:
        if df[col].max() <= 1:
            df[col] = df[col] * 100
    
    # Optional: Fill NA values with 0 if appropriate for your analysis
    # df = df.fillna(0)
    
    return df

# Load and clean your data
cleaned_data = clean_education_data('templates/data/discipline_data.csv')

# Save cleaned data to new CSV``
cleaned_data.to_csv('templates/data/discipline_data_cleaned.csv', index=False)

# Show the first 5 rows to verify
print(cleaned_data.head())