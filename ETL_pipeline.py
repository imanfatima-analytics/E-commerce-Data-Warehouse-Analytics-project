import pandas as pd

# =========================
#       ETL PROCESS
# =========================

# =========================
# EXTRACT
# =========================

df = pd.read_csv(
    r"C:\Users\lenovo\Downloads\Ecommerce-Data-Warehouse-project\data\ecommerce_raw_sales_50000.csv"
)

print("Data extracted successfully!")
print(df.head())


# =========================
# DATA PROFILING
# =========================

# 1. Shape
print("\n1. Shape:")
print(df.shape)


# 2. Columns
print("\n2. Columns:")
print(df.columns.tolist())


# 3. Data Types
print("\n3. Data Types:")
print(df.dtypes)


# 4. Missing Values
print("\n4. Missing Values:")
print(df.isnull().sum())


# 5. Duplicate Records
print("\n5. Duplicate Records:")
print(df.duplicated().sum())


# 6. Basic Statistics
print("\n6. Basic Statistics:")
print(df.describe())


# 7. Unique Values
print("\n7. Unique Values:")
print(df.nunique())


# =========================
# DATA VALIDATION
# =========================

# Check sales calculation
calculated_sales = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount_pct"].fillna(0))
)

df["sales_verified"] = (
    df["sales_amount"].round(2) == calculated_sales.round(2)
)

print("\nSales Validation:")
print(df["sales_verified"].value_counts())


# =========================
# CALCULATE PROFIT
# =========================

df["calculated_profit"] = (
    df["sales_amount"] - df["cost_amount"]
).round(2)

df["profit_verified"] = (
    df["profit"].round(2) == df["calculated_profit"]
)

print("\nProfit Validation:")
print(df["profit_verified"].value_counts())


# =========================
# PROFIT CHECK
# =========================

print("\nProfit Check:")
print(
    df[
        ["sales_amount", "cost_amount", "profit", "calculated_profit"]
    ].head(10)
)

print("\nTotal Profit:")
print(df["profit"].sum())

import pandas as pd

df = pd.read_csv(
    r"C:\Users\lenovo\Downloads\Ecommerce-Data-Warehouse-project\data\ecommerce_cleaned_sales.csv"
)

print("Cleaned rows:", len(df))
print("Columns:", len(df.columns))
