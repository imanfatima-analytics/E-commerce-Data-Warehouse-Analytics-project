# E-Commerce Data Warehouse & BI Analytics

An end-to-end **Data Warehousing and Business Intelligence project**
that transforms raw e-commerce sales data into a structured Snowflake
star schema and prepares it for Power BI analytics.

The project covers **Python/Pandas ETL, data profiling, data cleaning,
validation, Snowflake staging, dimensional modeling, fact and dimension
tables, SQL business analysis, SCD Type 2, data-quality checks, and BI
readiness**.

------------------------------------------------------------------------

## 📌 Project Overview

### Business Problem

An e-commerce business needs a reliable analytical system to understand:

-   Sales and revenue performance
-   Cost and profit
-   Orders and quantity sold
-   Average Order Value (AOV)
-   Profit margin
-   Product and category performance
-   Customer performance
-   City/geographic performance
-   Monthly and yearly trends
-   Sales channels
-   Payment methods
-   Historical customer changes

The project separates **data preparation**, **warehouse
storage/modeling**, **analytics**, and **BI reporting** into a
structured pipeline.

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                 RAW E-COMMERCE CSV
                         |
                         v
                 PYTHON / PANDAS
                         |
          +--------------+--------------+
          |              |              |
       EXTRACT        PROFILE        CLEAN
          |              |              |
          +--------------+--------------+
                         |
                    TRANSFORM
                         |
                     VALIDATE
                         |
                         v
                CLEANED CSV DATA
                         |
                         v
              SNOWFLAKE STAGING
                 STAGING_SALES
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    DIM_CUSTOMER    DIM_PRODUCT     DIM_DATE
          \              |              /
           \             |             /
            +------------+------------+
                         |
                         v
                    FACT_SALES
                         |
                         v
                   STAR SCHEMA
                         |
                         v
                  SQL ANALYTICS
                         |
                         v
                     POWER BI
```

------------------------------------------------------------------------

## 🛠️ Technology Stack

  Technology   Purpose
  ------------ ---------------------------------------------
  Python       ETL and data processing
  Pandas       Data profiling, cleaning and transformation
  SQL          Warehouse creation and business analysis
  Snowflake    Cloud data warehouse
  Power BI     Business intelligence and visualization
  CSV          Source data format
  Git/GitHub   Version control and portfolio documentation

------------------------------------------------------------------------

## 📂 Project Structure

``` text
Ecommerce-Data-Warehouse-project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── Python/
│   └── ETL_pipeline.py
│
├── SQL/
│
├── schemas/
│
└── documentation/
```

------------------------------------------------------------------------

## 📊 Source Dataset

The project uses an e-commerce sales dataset containing fields related
to:

-   Orders
-   Customers
-   Products
-   Dates
-   Cities
-   Quantity
-   Prices
-   Discounts
-   Sales
-   Cost
-   Profit
-   Order status
-   Payment method
-   Sales channel
-   Product category

### Dataset Columns

  Column             Description
  ------------------ ------------------------------
  `ORDER_ID`         Business order identifier
  `CUSTOMER_ID`      Business customer identifier
  `PRODUCT_ID`       Business product identifier
  `ORDER_DATE`       Order/sales date
  `CITY`             Customer/location city
  `QUANTITY`         Units sold
  `UNIT_PRICE`       Unit selling price
  `DISCOUNT_PCT`     Discount percentage
  `SALES_AMOUNT`     Revenue/sales amount
  `COST_AMOUNT`      Cost amount
  `PROFIT`           Profit
  `ORDER_STATUS`     Order status
  `PAYMENT_METHOD`   Payment method
  `SALES_CHANNEL`    Sales channel
  `PRODUCT_NAME`     Product name
  `CATEGORY`         Product category

> **Data note:** The original practice dataset was intended to contain
> 50,000 rows. The cleaned CSV used for Snowflake contains **49,920
> rows**. Snowflake successfully loaded all 49,920 rows with zero load
> errors.

------------------------------------------------------------------------

# 🔄 ETL Pipeline

## 1. Extract

The raw CSV is loaded using Pandas.

``` python
import pandas as pd

df = pd.read_csv(
    r"C:\Users\lenovo\Downloads\Ecommerce-Data-Warehouse-project\data\ecommerce_raw_sales_50000.csv"
)
```

------------------------------------------------------------------------

## 2. Data Profiling

The dataset is profiled before transformation.

``` python
print("Shape:", df.shape)

print("Columns:")
print(df.columns.tolist())

print("Data types:")
print(df.dtypes)

print("Missing values:")
print(df.isnull().sum())

print("Duplicates:")
print(df.duplicated().sum())

print("Basic statistics:")
print(df.describe(include="all"))
```

### Profiling checks

-   Dataset shape
-   Column names
-   Data types
-   Missing values
-   Duplicate records
-   Basic statistics
-   Unique values

------------------------------------------------------------------------

## 3. Data Cleaning

Text fields are standardized and dates are converted.

``` python
df["city"] = df["city"].astype(str).str.strip().str.title()

df["product_name"] = (
    df["product_name"]
    .astype(str)
    .str.strip()
)

df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

df["order_status"] = (
    df["order_status"]
    .astype(str)
    .str.strip()
    .str.title()
)

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["discount_pct"] = df["discount_pct"].fillna(0)
```

------------------------------------------------------------------------

## 4. Transformation & Validation

### Sales validation

``` python
calculated_sales = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount_pct"].fillna(0))
)

df["sales_verified"] = (
    df["sales_amount"].round(2)
    == calculated_sales.round(2)
)
```

### Profit validation

``` python
df["calculated_profit"] = (
    df["sales_amount"]
    - df["cost_amount"]
).round(2)

df["profit_verified"] = (
    df["profit"].round(2)
    == df["calculated_profit"]
)
```

### Date transformation

``` python
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()
```

> **Business rule:** `PROFIT = SALES_AMOUNT - COST_AMOUNT`.

------------------------------------------------------------------------

## 5. Save Processed Data

``` python
df.to_csv(
    r"C:\Users\lenovo\Downloads\Ecommerce-Data-Warehouse-project\data\processed\ecommerce_cleaned_sales.csv",
    index=False
)

print("Cleaned rows:", len(df))
print("Columns:", len(df.columns))
```

------------------------------------------------------------------------

# ❄️ Snowflake Data Warehouse

## Database & Schema

``` sql
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS ECOMMERCE_DW;

CREATE SCHEMA IF NOT EXISTS ECOMMERCE_DW.WAREHOUSE;

USE DATABASE ECOMMERCE_DW;

USE SCHEMA WAREHOUSE;
```

------------------------------------------------------------------------

# 🟦 Staging Layer

## STAGING_SALES

The staging table is the intermediate landing area between the processed
source file and the dimensional warehouse.

``` sql
CREATE OR REPLACE TABLE STAGING_SALES (
    ORDER_ID INTEGER,
    CUSTOMER_ID INTEGER,
    PRODUCT_ID INTEGER,
    ORDER_DATE DATE,
    CITY VARCHAR(100),
    QUANTITY INTEGER,
    UNIT_PRICE DECIMAL(12,2),
    DISCOUNT_PCT DECIMAL(5,2),
    SALES_AMOUNT DECIMAL(14,2),
    COST_AMOUNT DECIMAL(14,2),
    PROFIT DECIMAL(14,2),
    ORDER_STATUS VARCHAR(50),
    PAYMENT_METHOD VARCHAR(50),
    SALES_CHANNEL VARCHAR(50),
    PRODUCT_NAME VARCHAR(200),
    CATEGORY VARCHAR(100)
);
```

The cleaned CSV was loaded into Snowflake through Snowsight ingestion.

Only the required destination columns were mapped; Python
helper/validation columns were not loaded into the staging table.

------------------------------------------------------------------------

# ⭐ Dimensional Model

The warehouse uses a **Star Schema**.

``` text
                  DIM_CUSTOMER
                       |
                       |
DIM_PRODUCT ------ FACT_SALES ------ DIM_DATE
```

------------------------------------------------------------------------

## 👤 DIM_CUSTOMER

``` sql
CREATE OR REPLACE TABLE DIM_CUSTOMER (
    CUSTOMER_KEY INTEGER AUTOINCREMENT,
    CUSTOMER_ID INTEGER,
    CUSTOMER_NAME VARCHAR(200),
    CITY VARCHAR(100),
    EMAIL VARCHAR(200),
    PRIMARY KEY (CUSTOMER_KEY)
);
```

### Load

``` sql
INSERT INTO DIM_CUSTOMER (
    CUSTOMER_ID,
    CUSTOMER_NAME,
    CITY,
    EMAIL
)
SELECT DISTINCT
    CUSTOMER_ID,
    'Customer ' || CUSTOMER_ID,
    INITCAP(TRIM(CITY)),
    NULL
FROM STAGING_SALES;
```

> The source dataset did not contain real customer names or emails.
> `CUSTOMER_NAME` is therefore a generated label and `EMAIL` is NULL.

------------------------------------------------------------------------

## 📦 DIM_PRODUCT

``` sql
CREATE OR REPLACE TABLE DIM_PRODUCT (
    PRODUCT_KEY INTEGER AUTOINCREMENT,
    PRODUCT_ID INTEGER,
    PRODUCT_NAME VARCHAR(200),
    CATEGORY VARCHAR(100),
    PRODUCT_PRICE DECIMAL(12,2),
    PRIMARY KEY (PRODUCT_KEY)
);
```

### Load

``` sql
INSERT INTO DIM_PRODUCT (
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    PRODUCT_PRICE
)
SELECT DISTINCT
    PRODUCT_ID,
    TRIM(PRODUCT_NAME),
    INITCAP(TRIM(CATEGORY)),
    UNIT_PRICE
FROM STAGING_SALES;
```

------------------------------------------------------------------------

## 📅 DIM_DATE

``` sql
CREATE OR REPLACE TABLE DIM_DATE (
    DATE_KEY INTEGER,
    FULL_DATE DATE,
    DAY INTEGER,
    MONTH INTEGER,
    MONTH_NAME VARCHAR(20),
    QUARTER VARCHAR(10),
    YEAR INTEGER,
    PRIMARY KEY (DATE_KEY)
);
```

### Load

``` sql
TRUNCATE TABLE DIM_DATE;

INSERT INTO DIM_DATE (
    DATE_KEY,
    FULL_DATE,
    DAY,
    MONTH,
    MONTH_NAME,
    QUARTER,
    YEAR
)
SELECT DISTINCT
    TO_NUMBER(TO_CHAR(ORDER_DATE, 'YYYYMMDD')),
    ORDER_DATE,
    DAY(ORDER_DATE),
    MONTH(ORDER_DATE),
    MONTHNAME(ORDER_DATE),
    'Q' || QUARTER(ORDER_DATE),
    YEAR(ORDER_DATE)
FROM STAGING_SALES
WHERE ORDER_DATE IS NOT NULL;
```

------------------------------------------------------------------------

# 📈 FACT_SALES

`FACT_SALES` is the central business-event table.

### Grain

> **One row represents one source sales/order-line record.**

``` sql
CREATE OR REPLACE TABLE FACT_SALES (
    SALES_KEY INTEGER AUTOINCREMENT,
    ORDER_ID INTEGER,
    CUSTOMER_KEY INTEGER,
    PRODUCT_KEY INTEGER,
    DATE_KEY INTEGER,
    QUANTITY INTEGER,
    SALES_AMOUNT DECIMAL(14,2),
    COST_AMOUNT DECIMAL(14,2),
    PROFIT DECIMAL(14,2),
    PRIMARY KEY (SALES_KEY)
);
```

### Load

``` sql
INSERT INTO FACT_SALES (
    ORDER_ID,
    CUSTOMER_KEY,
    PRODUCT_KEY,
    DATE_KEY,
    QUANTITY,
    SALES_AMOUNT,
    COST_AMOUNT,
    PROFIT
)
SELECT
    s.ORDER_ID,
    c.CUSTOMER_KEY,
    p.PRODUCT_KEY,
    d.DATE_KEY,
    s.QUANTITY,
    s.SALES_AMOUNT,
    s.COST_AMOUNT,
    s.PROFIT
FROM STAGING_SALES s
INNER JOIN DIM_CUSTOMER c
    ON s.CUSTOMER_ID = c.CUSTOMER_ID
INNER JOIN DIM_PRODUCT p
    ON s.PRODUCT_ID = p.PRODUCT_ID
INNER JOIN DIM_DATE d
    ON s.ORDER_DATE = d.FULL_DATE;
```

------------------------------------------------------------------------

# 🔍 Warehouse Verification

``` sql
SELECT
    f.ORDER_ID,
    c.CUSTOMER_ID,
    c.CITY,
    p.PRODUCT_NAME,
    p.CATEGORY,
    d.FULL_DATE,
    d.YEAR,
    d.MONTH_NAME,
    f.QUANTITY,
    f.SALES_AMOUNT,
    f.COST_AMOUNT,
    f.PROFIT
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
JOIN DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
JOIN DIM_DATE d
    ON f.DATE_KEY = d.DATE_KEY
LIMIT 10;
```

------------------------------------------------------------------------

# 📊 SQL Business Analysis

## Total Sales, Cost & Profit

``` sql
SELECT
    SUM(SALES_AMOUNT) AS TOTAL_SALES,
    SUM(COST_AMOUNT) AS TOTAL_COST,
    SUM(PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES;
```

## Orders & Quantity

``` sql
SELECT
    COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS,
    SUM(QUANTITY) AS TOTAL_QUANTITY
FROM FACT_SALES;
```

## Average Order Value

``` sql
SELECT
    ROUND(
        SUM(SALES_AMOUNT) /
        NULLIF(COUNT(DISTINCT ORDER_ID), 0),
        2
    ) AS AOV
FROM FACT_SALES;
```

## Profit Margin

``` sql
SELECT
    ROUND(
        SUM(PROFIT) /
        NULLIF(SUM(SALES_AMOUNT), 0) * 100,
        2
    ) AS PROFIT_MARGIN_PERCENT
FROM FACT_SALES;
```

## Sales by Product

``` sql
SELECT
    p.PRODUCT_NAME,
    p.CATEGORY,
    SUM(f.QUANTITY) AS TOTAL_QUANTITY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY p.PRODUCT_NAME, p.CATEGORY
ORDER BY TOTAL_SALES DESC;
```

## Sales by Category

``` sql
SELECT
    p.CATEGORY,
    SUM(f.QUANTITY) AS TOTAL_QUANTITY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY p.CATEGORY
ORDER BY TOTAL_SALES DESC;
```

## Top 5 Products

``` sql
SELECT
    p.PRODUCT_NAME,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN DIM_PRODUCT p
    ON f.PRODUCT_KEY = p.PRODUCT_KEY
GROUP BY p.PRODUCT_NAME
ORDER BY TOTAL_SALES DESC
LIMIT 5;
```

## Sales by City

``` sql
SELECT
    c.CITY,
    SUM(f.QUANTITY) AS TOTAL_QUANTITY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
GROUP BY c.CITY
ORDER BY TOTAL_SALES DESC;
```

## Top Customers

``` sql
SELECT
    c.CUSTOMER_ID,
    c.CITY,
    COUNT(DISTINCT f.ORDER_ID) AS TOTAL_ORDERS,
    SUM(f.QUANTITY) AS TOTAL_QUANTITY,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN DIM_CUSTOMER c
    ON f.CUSTOMER_KEY = c.CUSTOMER_KEY
GROUP BY c.CUSTOMER_ID, c.CITY
ORDER BY TOTAL_SALES DESC
LIMIT 10;
```

## Monthly Analysis

``` sql
SELECT
    d.YEAR,
    d.MONTH,
    d.MONTH_NAME,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.COST_AMOUNT) AS TOTAL_COST,
    SUM(f.PROFIT) AS TOTAL_PROFIT,
    COUNT(DISTINCT f.ORDER_ID) AS TOTAL_ORDERS
FROM FACT_SALES f
JOIN DIM_DATE d
    ON f.DATE_KEY = d.DATE_KEY
GROUP BY
    d.YEAR,
    d.MONTH,
    d.MONTH_NAME
ORDER BY
    d.YEAR,
    d.MONTH;
```

## Sales by Channel

``` sql
SELECT
    s.SALES_CHANNEL,
    COUNT(DISTINCT f.ORDER_ID) AS TOTAL_ORDERS,
    SUM(f.SALES_AMOUNT) AS TOTAL_SALES,
    SUM(f.PROFIT) AS TOTAL_PROFIT
FROM FACT_SALES f
JOIN STAGING_SALES s
    ON f.ORDER_ID = s.ORDER_ID
GROUP BY s.SALES_CHANNEL
ORDER BY TOTAL_SALES DESC;
```

------------------------------------------------------------------------

# 🔄 SCD Type 2

SCD Type 2 preserves historical dimension changes.

Example:

``` text
CUSTOMER_ID | CITY     | START_DATE | END_DATE   | IS_CURRENT
------------|----------|------------|------------|-----------
101         | Lahore   | 2026-01-01 | 2026-07-31 | FALSE
101         | Karachi  | 2026-08-01 | NULL       | TRUE
```

## SCD2 Table

``` sql
CREATE OR REPLACE TABLE DIM_CUSTOMER_SCD2 (
    CUSTOMER_KEY INTEGER AUTOINCREMENT,
    CUSTOMER_ID INTEGER,
    CUSTOMER_NAME VARCHAR(200),
    CITY VARCHAR(100),
    EMAIL VARCHAR(200),
    START_DATE DATE,
    END_DATE DATE,
    IS_CURRENT BOOLEAN,
    PRIMARY KEY (CUSTOMER_KEY)
);
```

## Initial Load

``` sql
INSERT INTO DIM_CUSTOMER_SCD2 (
    CUSTOMER_ID,
    CUSTOMER_NAME,
    CITY,
    EMAIL,
    START_DATE,
    END_DATE,
    IS_CURRENT
)
SELECT
    CUSTOMER_ID,
    CUSTOMER_NAME,
    CITY,
    EMAIL,
    CURRENT_DATE(),
    NULL,
    TRUE
FROM DIM_CUSTOMER;
```

### SCD2 logic

1.  Match on `CUSTOMER_ID`.
2.  Compare tracked attributes.
3.  If unchanged → keep current record.
4.  If changed → close old record.
5.  Insert a new version.
6.  Mark the new version as current.

------------------------------------------------------------------------

# ✅ Data Quality

## NULL Checks

``` sql
SELECT
    COUNT_IF(CUSTOMER_KEY IS NULL) AS NULL_CUSTOMERS,
    COUNT_IF(PRODUCT_KEY IS NULL) AS NULL_PRODUCTS,
    COUNT_IF(DATE_KEY IS NULL) AS NULL_DATES,
    COUNT_IF(SALES_AMOUNT IS NULL) AS NULL_SALES,
    COUNT_IF(PROFIT IS NULL) AS NULL_PROFIT
FROM FACT_SALES;
```

## Negative Values

``` sql
SELECT
    COUNT_IF(QUANTITY < 0) AS NEGATIVE_QUANTITY,
    COUNT_IF(SALES_AMOUNT < 0) AS NEGATIVE_SALES,
    COUNT_IF(COST_AMOUNT < 0) AS NEGATIVE_COST
FROM FACT_SALES;
```

## Profit Validation

``` sql
SELECT
    COUNT(*) AS TOTAL_ROWS,
    COUNT_IF(
        ROUND(PROFIT, 2) !=
        ROUND(SALES_AMOUNT - COST_AMOUNT, 2)
    ) AS INVALID_PROFIT_ROWS
FROM FACT_SALES;
```

## Important Note About Duplicate Orders

``` sql
SELECT
    ORDER_ID,
    COUNT(*) AS RECORD_COUNT
FROM FACT_SALES
GROUP BY ORDER_ID
HAVING COUNT(*) > 1;
```

Repeated `ORDER_ID` values are **not automatically errors** because the
fact grain can contain multiple sales/order-line records for one order.

------------------------------------------------------------------------

# ❄️ Snowflake Performance Concepts

Snowflake does not rely on traditional B-tree indexes in the same way as
traditional OLTP databases.

Instead, Snowflake uses:

-   Micro-partitions
-   Metadata
-   Partition pruning
-   Clustering where appropriate

For this approximately 50k-row learning dataset, clustering is not
necessary.

------------------------------------------------------------------------

# 🔗 Data Lineage

``` text
Raw CSV
   ↓
Python / Pandas
   ↓
Cleaned CSV
   ↓
STAGING_SALES
   ↓
DIMENSIONS + FACT
   ↓
SQL Analytics
   ↓
Power BI
```

This allows a Power BI metric to be traced back to the warehouse and
ultimately to the source data.

------------------------------------------------------------------------

# 📈 Power BI

The final warehouse is designed to feed a Power BI dashboard.

### Recommended Dashboard Pages

1.  **Executive Overview**
    -   Total Sales
    -   Total Profit
    -   Total Orders
    -   Quantity
    -   AOV
    -   Profit Margin
2.  **Product Performance**
    -   Top Products
    -   Category Sales
    -   Category Profit
3.  **Customer Analysis**
    -   Top Customers
    -   Customer Sales
    -   Customer Profit
4.  **Geographic Analysis**
    -   Sales by City
    -   Profit by City
5.  **Time Analysis**
    -   Monthly Sales
    -   Monthly Profit
    -   Yearly Trends
6.  **Channel & Payment**
    -   Sales Channel
    -   Payment Method
    -   Order Status

------------------------------------------------------------------------

# 🧪 Testing & Validation

  Test                Expected Result
  ------------------- ---------------------------------------
  CSV extraction      File loads successfully
  Data profiling      Shape/types/missing values identified
  Cleaning            Text and dates standardized
  Sales validation    Calculated sales matches source
  Profit validation   Profit = Sales − Cost
  Snowflake staging   49,920 rows loaded
  Dimension loading   Dimensions populated
  Fact loading        Matching dimension keys
  NULL checks         No unexpected NULL keys
  SCD Type 2          Historical versions preserved
  SQL analysis        Business metrics available
  Power BI            Warehouse ready for dashboard

------------------------------------------------------------------------

# 🚨 Troubleshooting Lessons

### DIM_DATE was empty

**Problem:** FACT_SALES returned zero rows.

**Cause:** The INNER JOIN required matching dates, but DIM_DATE had no
rows.

**Solution:** Populate DIM_DATE from distinct `ORDER_DATE` values in
`STAGING_SALES`.

------------------------------------------------------------------------

### 49,920 vs 50,000 rows

The original practice dataset was intended to have 50,000 rows, but the
cleaned CSV contained 49,920 rows.

Snowflake did **not** reject 80 rows.

The load successfully showed:

``` text
ROW_COUNT  = 49,920
ROW_PARSED = 49,920
ERROR_COUNT = 0
```

------------------------------------------------------------------------

### Extra columns during Snowflake ingestion

The cleaned Python file contained helper/validation columns in addition
to the warehouse source columns.

Only the required 16 columns were mapped into `STAGING_SALES`.

------------------------------------------------------------------------

# 🎯 Business Value

This project converts raw e-commerce data into a structured analytical
system that can help a business:

-   Monitor revenue
-   Measure profitability
-   Identify top products
-   Compare categories
-   Analyze customers
-   Compare cities
-   Understand time trends
-   Evaluate sales channels
-   Evaluate payment methods
-   Preserve customer history
-   Build trusted BI dashboards

------------------------------------------------------------------------

# 🚀 Future Improvements

For a production implementation, the project can be extended with:

-   Automated data ingestion
-   Incremental loading
-   Production-grade SCD2 MERGE logic
-   Data-quality testing framework
-   Pipeline orchestration
-   Error/quarantine tables
-   Logging and monitoring
-   Data freshness monitoring
-   Role-based security
-   Development/test/production environments
-   CI/CD
-   Data catalog and governance
-   Power BI semantic model
-   Automated dashboard refresh

------------------------------------------------------------------------

# 📌 Project Deliverables

-   `ETL_pipeline.py`
-   `ecommerce_cleaned_sales.csv`
-   `STAGING_SALES`
-   `DIM_CUSTOMER`
-   `DIM_PRODUCT`
-   `DIM_DATE`
-   `FACT_SALES`
-   `DIM_CUSTOMER_SCD2`
-   SQL business analysis
-   Data-quality validation
-   Star schema
-   Power BI-ready warehouse
-   Project documentation

------------------------------------------------------------------------

# 💼 Resume Project Description

**E-Commerce Data Warehouse & BI Analytics**

> Built an end-to-end e-commerce data warehouse using Python/Pandas,
> Snowflake and SQL. Performed data profiling, cleaning, transformation
> and validation on 49,920 cleaned sales records. Designed a dimensional
> star schema with customer, product, date and sales fact tables,
> implemented SCD Type 2 for historical customer tracking, developed SQL
> business analytics for sales, profit, AOV, products, customers and
> time trends, and prepared the warehouse for Power BI reporting.

------------------------------------------------------------------------

# 🗣️ Interview Explanation

> I built an end-to-end E-commerce Data Warehouse and BI Analytics
> project. I started with a raw CSV and used Python and Pandas for
> extraction, profiling, cleaning, transformation and validation. I then
> loaded the cleaned data into Snowflake staging and created customer,
> product and date dimensions along with a sales fact table using a star
> schema. I used SQL to analyze sales, cost, profit, AOV, products,
> categories, cities, customers, payment methods, channels and time
> trends. I also implemented SCD Type 2 to preserve customer history and
> added data-quality checks. The final warehouse is designed to feed a
> Power BI dashboard.

------------------------------------------------------------------------

## 📚 Learning Topics Covered

-   Data Warehousing
-   OLTP vs OLAP
-   ETL vs ELT
-   Data Lake vs Warehouse vs Lakehouse
-   Data Modeling
-   ERD
-   Primary & Foreign Keys
-   Natural & Surrogate Keys
-   Normalization
-   Star Schema
-   Snowflake Schema
-   Fact Tables
-   Dimension Tables
-   Fact Grain
-   Additive / Semi-additive / Non-additive Measures
-   Python ETL
-   Pandas
-   Snowflake
-   SQL Analytics
-   SCD Type 2
-   Data Quality
-   Data Lineage
-   Metadata
-   Micro-partitions
-   Query Pruning
-   Power BI

------------------------------------------------------------------------

## 👩‍💻 Author

**Iman Fatima**

Data & AI / Software Engineering Portfolio Project

**Project:** E-Commerce Data Warehouse & BI Analytics
