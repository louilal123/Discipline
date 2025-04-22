import pandas as pd

input_path = "templates/data/harasment-bullying.csv"
output_path = "templates/data/harassment_bullying_cleaned.csv"

# Load CSV and skip malformed lines
try:
    df = pd.read_csv(input_path, dtype=str, on_bad_lines='skip')
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Clean column headers
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
)

# Clean numeric values
for col in df.columns[1:]:
    df[col] = (
        df[col]
        .str.replace(",", "", regex=False)
        .fillna("0")
    )
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Save cleaned CSV
df.to_csv(output_path, index=False)
print(f"✅ Cleaned file saved as: {output_path}")
