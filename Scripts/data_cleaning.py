import pandas as pd
import numpy as np
import os

# Load raw dataset
input_path = "Data/Raw/zomato.csv"

df = pd.read_csv(input_path)

print("Original Dataset Shape:", df.shape)

# Remove unnecessary spaces from column names

df.columns = df.columns.str.strip()

# Remove extra spaces
df["rate"] = df["rate"].astype("string").str.strip()

# Extract numerical rating
df["rate"] = df["rate"].str.extract(
    r"(\d+(?:\.\d+)?)"
)[0]

# Convert rating into numeric format
df["rate"] = pd.to_numeric(
    df["rate"], errors="coerce"
)

# Remove commas and extra spaces

cost_column = "approx_cost(for two people)"

df[cost_column] = (
    df[cost_column]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.strip()
)

# Convert into numeric format

df[cost_column] = pd.to_numeric(
    df[cost_column], errors="coerce"
)

categorical_columns = [
    "online_order",
    "book_table",
    "location",
    "rest_type",
    "cuisines",
    "listed_in(type)",
    "listed_in(city)"
]

for col in categorical_columns:

    df[col] = df[col].astype("string").str.strip()

    df[col] = df[col].replace("", pd.NA)

# ---------- SQL-READY FIXES (for MySQL Workbench import) ----------

# Drop very large text columns (reviews up to 1.2M chars per cell)
# that make the CSV ~574 MB and break the Workbench import
df = df.drop(columns=["reviews_list", "menu_item", "url"])

# Phone numbers contain line breaks between multiple numbers,
# which split rows during import -> join them with ", "
df["phone"] = (
    df["phone"]
    .astype("string")
    .str.replace(r"\s*[\r\n]+\s*", ", ", regex=True)
    .str.strip()
)

# Rename columns containing brackets (invalid in plain SQL names)
df = df.rename(columns={
    "approx_cost(for two people)": "approx_cost",
    "listed_in(type)": "listed_type",
    "listed_in(city)": "listed_city"
})

cost_column = "approx_cost"

# Store whole-number columns as nullable integers (no "800.0")
df["votes"] = pd.to_numeric(df["votes"], errors="coerce").astype("Int64")
df[cost_column] = df[cost_column].round().astype("Int64")

# Remove duplicate rows
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)
print("\nDuplicate rows removed:", duplicates_before)

print("\n========== CLEANING RESULTS ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nRating Samples:")
print(df["rate"].head(20))

print("\nCost Samples:")
print(df[cost_column].head(20))

print("\nMissing Values:")
print(df.isnull().sum())

# Create processed folder if it doesn't exist

os.makedirs("Data/Processed", exist_ok=True)

# Save cleaned dataset

output_path = "Data/Processed/zomato_cleaned.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")

# FINAL DATA QUALITY CHECK

print("\n========== FINAL VALIDATION ==========")

# 1. Check dataset dimensions
print("Dataset Shape:", df.shape)

# 2. Check duplicate rows
print("Duplicate Rows:", df.duplicated().sum())

# 3. Check rating range
print("\nRating Statistics:")
print(df["rate"].describe())

# 4. Check invalid ratings
print(
    "Ratings outside 0-5:",
    ((df["rate"] < 0) | (df["rate"] > 5)).sum()
)

# 5. Check cost statistics
print("\nCost Statistics:")
print(df[cost_column].describe())

# 6. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 7. Verify processed file
check_df = pd.read_csv(output_path)

print("\nSaved File Shape:", check_df.shape)

print("\nVALIDATION COMPLETED!")