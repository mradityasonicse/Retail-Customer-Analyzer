# Academic Project Report: Retail Customer Analyzer

**Course:** Bachelor of Technology - Computer Science and Engineering  
**Specialization:** Artificial Intelligence and Machine Learning in association with Microsoft  
**School:** School of Computer Science and Engineering  
**Institution:** Rungta International Skills University  
**Subject:** Python Programming & Data Analytics Lab  
**Problem Statement No.:** 74  
**Project Title:** Retail Customer Analyzer  

---

## 1. Abstract
The **Retail Customer Analyzer** is a specialized analytical application built using **Python 3** and the **Pandas** data manipulation library. Developed to address **Problem Statement No. 74**, this system ingests customer transaction data from CSV files, performs automated schema standardization and data sanitization, computes descriptive statistical metrics (mean, median, extreme spenders), executes threshold-based customer segmentation, and calculates grouped regional summaries. The application incorporates full input validation, graceful missing file handling, and automated reporting.

---

## 2. Problem Statement & Objectives

### 2.1 Problem Definition
Retail enterprises handle customer purchase records spanning diverse geographic regions. Managers require immediate, accurate visibility into:
1. Overall customer spending trends and central tendencies.
2. Boundary-level segmentation to identify high-value VIP accounts.
3. Regional revenue concentrations to allocate marketing capital.

### 2.2 Core Objectives
- **Data Ingestion:** Load `customers.csv` safely using Pandas, handling missing or corrupted files without unhandled program termination.
- **Statistical Analytics:** Derive descriptive statistics for `TotalSpent`, including arithmetic mean, median, maximum, and minimum.
- **Dynamic Customer Filtering:** Enable users to set custom spending thresholds to isolate high-value customers.
- **Geographic Aggregation:** Group transaction records by `City` to yield total sales and mean expenditure per region.
- **Input Robustness:** Intercept non-numeric inputs and negative monetary limits with descriptive error feedback.
- **Console Interface:** Provide both an intuitive interactive CLI and scriptable command-line flags.

---

## 3. Dataset Description

The application processes structured customer records adhering to the following schema:

| Column Name | Data Type | Description |
|:------------|:---------:|:------------|
| `CustomerID` | String / Alphanumeric | Unique customer identifier (e.g., C01, C02) |
| `Name` | String | Customer full or first name |
| `City` | String | Residential or purchasing city (e.g., Raipur, Durg, Bhilai) |
| `Purchases` | Integer | Total count of distinct purchase transactions |
| `TotalSpent` | Numeric (Float/Int) | Aggregate amount spent in Rupees (Rs.) |

### Sample Dataset (`customers.csv`):
```csv
CustomerID,Name,City,Purchases,TotalSpent
C01,Asha,Raipur,5,12000
C02,Bhavin,Durg,2,3000
C03,Chitra,Raipur,8,25000
C04,Deepak,Bhilai,1,800
C05,Esha,Durg,4,9000
C06,Farhan,Raipur,3,6000
C07,Gita,Bhilai,6,15000
C08,Hari,Durg,2,2200
```

---

## 4. Technical Architecture & Methodology

```
+-------------------------------------------------------+
|                    customers.csv                      |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|               Data Ingestion & Hygiene                |
|  - File existence check (os.path.exists)              |
|  - Pandas read_csv with header normalization          |
|  - Numeric type coercion & NaN filtering              |
+-------------------------------------------------------+
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
+-----------------------+           +-----------------------+
| Spending Statistics   |           | Geographic Aggregation|
| - df.mean()           |           | - df.groupby('City')  |
| - df.median()         |           | - agg('sum', 'mean')  |
| - df.idxmax()         |           | - sort_values(desc)   |
| - df.idxmin()         |           +-----------------------+
+-----------------------+                     |
        |                                     v
        v                           +-----------------------+
+-----------------------+           | High-Value Filtering  |
| Visualizations        |           | - Input validation    |
| - Matplotlib (300 DPI)|           | - Boolean mask: >= X  |
+-----------------------+           +-----------------------+
```

### 4.1 Key Modules & Functions
1. **`load_customer_data(file_path)`**:
   - Validates file existence using `os.path.exists()`.
   - Normalizes column names (case-insensitive mapping to `CustomerID`, `Name`, `City`, `Purchases`, `TotalSpent`).
   - Coerces numbers with `pd.to_numeric(..., errors='coerce')` to eliminate data type corruptions.
2. **`get_spending_statistics(df)`**:
   - Computes `df['TotalSpent'].mean()` and `df['TotalSpent'].median()`.
   - Identifies index locations using `.idxmax()` and `.idxmin()` to extract exact customer names and spending.
3. **`validate_spending_limit(limit_input)`**:
   - Enforces two-tier validation: ensures string input parses to a floating-point number, and rejects values `< 0`.
4. **`get_high_value_customers(df, limit_value)`**:
   - Applies Pandas boolean indexing `df[df['TotalSpent'] >= limit]` and formats output lines as `CustomerID | Name | City | Rs. Amount`.
5. **`get_city_wise_summary(df)`**:
   - Groups records by `City` using `.groupby('City', as_index=False).agg(...)`.
   - Sorts records descending by Total Revenue to highlight top-performing cities.
6. **`generate_charts(df)`**:
   - Employs Matplotlib to output publication-quality PNG charts comparing regional and customer metrics.

---

## 5. Experimental Verification & Test Cases

All test cases specified in Problem Statement No. 74 were executed and validated.

### 5.1 Test Case 1: Normal Input (Spending Statistics)
- **Menu Selected:** `Spending statistics`
- **Output:**
```text
Mean spend: Rs. 9125.00
Median spend: Rs. 7500.00
Highest: Chitra (Rs. 25000)
Lowest: Deepak (Rs. 800)
```
- **Verification:**
  - Sum of expenditures = 12000 + 3000 + 25000 + 800 + 9000 + 6000 + 15000 + 2200 = Rs. 73,000.
  - Mean = 73,000 / 8 = **Rs. 9,125.00** *(Exact)*.
  - Sorted array: [800, 2200, 3000, 6000, 9000, 12000, 15000, 25000]. Median = (6000 + 9000) / 2 = **Rs. 7,500.00** *(Exact)*.
  - Maximum = Chitra (Rs. 25,000), Minimum = Deepak (Rs. 800). **Result: PASS**.

### 5.2 Test Case 2: Boundary / Minimum Input (High-Value Customers)
- **Menu Selected:** `High-value customers`
- **User Input Limit:** `25000`
- **Output:**
```text
High-value customers (TotalSpent >= 25000):
C03 | Chitra | Raipur | Rs. 25000
```
- **Verification:** Only customer C03 has `TotalSpent` >= 25000. **Result: PASS**.

### 5.3 Test Case 3: Invalid Input Handling
- **Scenario (a):** Limit = `abc`
  - **Output:** `Invalid amount. Please enter a number.`
  - **Verification:** Successfully caught `ValueError` during float conversion. **Result: PASS**.
- **Scenario (b):** Limit = `-500`
  - **Output:** `Amount must be 0 or more.`
  - **Verification:** Boundary validation rejected negative values. **Result: PASS**.

### 5.4 Test Case 4: City-Wise Summary
- **Menu Selected:** `City-wise summary`
- **Output:**
```text
Raipur : Total Rs. 43000 | Average Rs. 14333.33
Bhilai : Total Rs. 15800 | Average Rs. 7900.00
Durg : Total Rs. 14200 | Average Rs. 4733.33
```
- **Verification:**
  - Raipur: 12000 + 25000 + 6000 = Rs. 43,000 (Count: 3, Avg: Rs. 14,333.33).
  - Bhilai: 800 + 15000 = Rs. 15,800 (Count: 2, Avg: Rs. 7,900.00).
  - Durg: 3000 + 9000 + 2200 = Rs. 14,200 (Count: 3, Avg: Rs. 4,733.33).
  - Sorted descending by Total revenue. **Result: PASS**.

---

## 6. Test Suite Execution Summary

Automated testing was conducted via `test_runner.py`:

```text
=================================================================
      RETAIL CUSTOMER ANALYZER - AUTOMATED TEST HARNESS        
       Rungta International Skills University - PS 74          
=================================================================
[PASS] - Test Case 1: Spending Statistics (Normal Input)
[PASS] - Test Case 2: High-Value Customers (Boundary >= 25000)
[PASS] - Test Case 3a: Invalid Input (Non-numeric amount 'abc')
[PASS] - Test Case 3b: Invalid Input (Negative amount '-500')
[PASS] - Test Case 4: City-wise Summary (Grouped & Sorted)
[PASS] - Test Case 5: Missing File Error Handling
[PASS] - Interactive Console Simulation Test
=================================================================
SUMMARY: 7/7 Tests Passed (100% Success Rate)
=================================================================
[SUCCESS] All test cases validated and compliant with specification.
```

---

## 7. Conclusion
The **Retail Customer Analyzer (PS 74)** successfully satisfies all functional specifications, constraints, and edge-case requirements outlined by the School of Computer Science and Engineering at Rungta International Skills University. The modular implementation guarantees zero crashes, full data integrity, and seamless analytical reporting.
