import pandas as pd

df = pd.read_csv(
    r"C:\Users\lenovo\Downloads\Ecommerce-Data-Warehouse-project\data\ecommerce_cleaned_sales.csv"
)

print("Cleaned rows:", len(df))
print("Columns:", len(df.columns))
