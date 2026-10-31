import pandas as pd
import os

# Dataset path
file_path = "Data/Raw/zomato.csv"

# Check whether file exists
if os.path.exists(file_path):

    print("Dataset found successfully!")

    # Load dataset
    df = pd.read_csv(file_path)

    # Dataset information
    print("\nDataset Shape:")
    print(df.shape)

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nDataset Information:")
    df.info()

else:
    print("Dataset not found!")

    # Check missing values

print("\nMissing Values:")
print(df.isnull().sum())

# Missing percentage

print("\nMissing Percentage:")
missing_percentage = (df.isnull().sum() / len(df)) * 100

print(missing_percentage.sort_values(ascending=False))

# Check duplicate records

print("\nDuplicate Records:")
print(df.duplicated().sum())

# Check unique values

print("\nUnique Values:")
print(df.nunique())

# Check sample ratings

print("\nRating Values:")
print(df["rate"].value_counts().head(15))

# Check online ordering values

print("\nOnline Order Values:")
print(df["online_order"].value_counts())

# Investigating inconsistent values

print("\n========== RATE ANALYSIS ==========")
print(df["rate"].value_counts(dropna=False).to_string())

print("\n========== APPROX COST ANALYSIS ==========")
print(df["approx_cost(for two people)"].value_counts(dropna=False).head(30))

print("\n========== BOOK TABLE ANALYSIS ==========")
print(df["book_table"].value_counts(dropna=False))

print("\n========== RESTAURANT TYPE ANALYSIS ==========")
print(df["rest_type"].value_counts(dropna=False).head(20))

print("\n========== LOCATION ANALYSIS ==========")
print(df["location"].value_counts(dropna=False).head(20))

# Detailed rating investigation

print("\n--- Unique Rating Values ---")

print(sorted(df["rate"].dropna().unique()))

print("\n--- Rating Value Counts ---")

print(df["rate"].value_counts(dropna=False).tail(20))


# Detailed cost investigation

print("\n--- Unique Cost Values ---")

print(df["approx_cost(for two people)"].unique())

print("\n--- Cost Value Counts ---")

print(
    df["approx_cost(for two people)"]
    .value_counts(dropna=False)
    .tail(20)
)