import pandas as pd
import numpy as np

# Load the dataset
file_path = "templates/data/public_school_datapysical.csv"
df = pd.read_csv(file_path)

# Preview initial columns
print("Initial columns:", df.columns.tolist())

# Clean column names (strip spaces and fix typos)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace(r'[^\w]', '', regex=True)

# Function to clean numeric-looking strings
def to_numeric(val):
    try:
        # Remove commas and quotes
        val = str(val).replace(',', '').replace('"', '').strip()
        # Handle values like "1-3" or "01-Mar"
        if '-' in val or val.lower().endswith(('jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                                'jul', 'aug', 'sep', 'oct', 'nov', 'dec')):
            return np.nan
        return pd.to_numeric(val)
    except:
        return np.nan

# Identify which columns to convert (skip 'State' and similar identifiers)
columns_to_convert = [col for col in df.columns if col.lower() != 'state']
for col in columns_to_convert:
    df[col] = df[col].apply(to_numeric)

# Drop rows with no state info
df = df.dropna(subset=['State'])

# Optionally fill NaNs with 0 (or leave as-is)
df.fillna(0, inplace=True)

# Preview cleaned data
print(df.head())

# Save to new CSV for visualization
df.to_csv("templates/data/public_school_cleaned.csv", index=False)
print("✅ Cleaned CSV saved as 'public_school_cleaned.csv'")
