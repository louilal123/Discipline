import pandas as pd

# Load the dataset
file_path = "C:/COMMA/Discipline/templates/data/Alaska_cleaned.csv"
df = pd.read_csv(file_path)

# List of columns to remove decimals from (you can adjust this list)
columns_to_clean = [
    'Students_wo_w_Disabilities_Male_Percent',
    'Students_wo_w_Disabilities_Female_Percent',
    'Section504_Male_Percent',
    'Section504_Female_Percent',
    'IDEA_Male_Percent',
    'IDEA_Female_Percent',
    'Race_AmericanIndian_Male_Percent',
    'Race_AmericanIndian_Female_Percent',
    'Race_Asian_Male_Percent',
    'Race_Asian_Female_Percent',
    'Race_Hispanic_Male_Percent',
    'Race_Hispanic_Female_Percent',
    'Race_Black_Male_Percent',
    'Race_Black_Female_Percent',
    'Race_White_Male_Percent',
    'Race_White_Female_Percent',
    'Race_NativeHawaiian_Male_Percent',
    'Race_NativeHawaiian_Female_Percent',
    'Race_TwoOrMore_Male_Percent',
    'Race_TwoOrMore_Female_Percent',
    'ELL_Male_Percent',
    'ELL_Female_Percent'
]

# Replace non-numeric values (NaN or inf) with 0, then convert to integer
df[columns_to_clean] = df[columns_to_clean].apply(
    lambda x: pd.to_numeric(x, errors='coerce').fillna(0).astype(int)
)

# Save the cleaned dataset
output_path = "C:/COMMA/Discipline/templates/data/Alaska_cleaned_no_decimals.csv"
df.to_csv(output_path, index=False)

print(f"Cleaned dataset saved to {output_path}")
