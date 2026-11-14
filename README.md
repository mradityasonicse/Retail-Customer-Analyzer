# Retail Customer Analyzer (PS No. 74)

[![Python 3](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x%20%7C%203.x-150458.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24+-013243.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-11557c.svg)](https://matplotlib.org/)
[![Tests](https://img.shields.io/badge/Test_Suite-100%25_Passing-brightgreen.svg)]()

> **Rungta International Skills University**  
> **School of Computer Science and Engineering**  
> *Bachelor of Technology - Computer Science and Engineering (Artificial Intelligence and Machine Learning in association with Microsoft)*

A high-performance, console-based Python 3 retail customer analytics system built to analyze retail transactions, filter high-value spenders, perform statistical aggregations, and compute city-wise spending distributions using **Pandas**.

---

## 📌 Problem Statement & Specifications

- **Problem Statement No.:** 74
- **Project Title:** Retail Customer Analyzer
- **Description:** Read `customers.csv` with Pandas. Show mean, median, highest and lowest spending, list customers who spent at least a limit entered by the user, and show city-wise total and average spending.
- **Language:** Python 3
- **Core Concepts:** Pandas, Filtering, Grouping, Statistics, Input Validation, File Exception Handling

---

## 🚀 Bare Minimum Requirements Compliance Matrix

| # | Bare Minimum Requirement | Implementation Detail | Status |
|---|--------------------------|-----------------------|:------:|
| **1** | Write the solution in Python 3 (one `.py` file) and run it from the console | Standalone implementation in [`retail_customer_analyzer.py`](retail_customer_analyzer.py) with interactive console loop and CLI automation | **PASS** |
| **2** | Load `customers.csv` with Pandas and handle a missing file | Validated in `load_customer_data()` catching `FileNotFoundError`, empty CSVs, and malformed headers gracefully | **PASS** |
| **3** | Calculate mean, median, highest and lowest `TotalSpent` | Evaluated in `get_spending_statistics()` returning formatted Mean, Median, Highest customer, and Lowest customer | **PASS** |
| **4** | Filter and list customers whose `TotalSpent` is at least the limit entered by the user | Evaluated in `get_high_value_customers()` with numeric validation (handles non-numbers and negative numbers) | **PASS** |
| **5** | Test the program with all four test cases | Verified with 100% precision via [`test_runner.py`](test_runner.py) | **PASS** |

---

## 📂 Project Directory Structure

```text
E:\Retail Customer Analyzer\
│
├── retail_customer_analyzer.py  # Core standalone solution (Requirement 1)
├── main.py                      # Application entry point delegating to core analyzer
├── customers.csv                # Primary sample dataset (8 rows, 5 columns)
├── test_runner.py               # Automated test suite executing all 4 test cases
├── requirements.txt             # Python dependencies (pandas, numpy, matplotlib)
├── .gitignore                   # Version control ignore rules
├── README.md                    # Project manual & documentation
├── PROJECT_REPORT.md            # Academic project report (Rungta University standard)
│
├── city_spending_summary.png          # Matplotlib chart: Total & Average spending per city
└── customer_spending_distribution.png  # Matplotlib chart: Individual customer spending vs mean/median
```

---

## 📊 Dataset Schema (`customers.csv`)

The sample dataset consists of 5 columns and 8 customer records:

| CustomerID | Name | City | Purchases | TotalSpent (Rs.) |
|:----------:|:-----|:-----|:---------:|:----------------:|
| **C01** | Asha | Raipur | 5 | 12,000 |
| **C02** | Bhavin | Durg | 2 | 3,000 |
| **C03** | Chitra | Raipur | 8 | 25,000 |
| **C04** | Deepak | Bhilai | 1 | 800 |
| **C05** | Esha | Durg | 4 | 9,000 |
| **C06** | Farhan | Raipur | 3 | 6,000 |
| **C07** | Gita | Bhilai | 6 | 15,000 |
| **C08** | Hari | Durg | 2 | 2,200 |

---

## 🧪 Test Cases & Verified Outputs

### Test Case 1: Normal Input (Spending Statistics)
- **Input:** Menu: `Spending statistics` (Option `1`)
- **Expected & Verified Output:**
```text
Mean spend: Rs. 9125.00
Median spend: Rs. 7500.00
Highest: Chitra (Rs. 25000)
Lowest: Deepak (Rs. 800)
```

---

### Test Case 2: Boundary / Minimum Input (High-Value Customers)
- **Input:** Menu: `High-value customers` (Option `2`), Limit: `25000`
- **Expected & Verified Output:**
```text
High-value customers (TotalSpent >= 25000):
C03 | Chitra | Raipur | Rs. 25000
```

---

### Test Case 3: Invalid Input
- **(a) Non-numeric input:** Menu: `High-value customers`, Limit: `abc`
  - **Expected & Verified Output:**
  ```text
  Invalid amount. Please enter a number.
  ```
- **(b) Negative amount:** Menu: `High-value customers`, Limit: `-500`
  - **Expected & Verified Output:**
  ```text
  Amount must be 0 or more.
  ```

---

### Test Case 4: Different Valid Scenario (City-wise Summary)
- **Input:** Menu: `City-wise summary` (Option `3`)
- **Expected & Verified Output:**
```text
Raipur : Total Rs. 43000 | Average Rs. 14333.33
Bhilai : Total Rs. 15800 | Average Rs. 7900.00
Durg : Total Rs. 14200 | Average Rs. 4733.33
```
*Note: Ranked descending by Total Spending (Raipur: Rs. 43,000 > Bhilai: Rs. 15,800 > Durg: Rs. 14,200).*

---

## 🛠️ Installation & Execution Guide

### 1. Prerequisites
Ensure Python 3.8+ is installed on your system.

### 2. Install Dependencies
Navigate to the project folder and install the required libraries:
```bash
cd "E:\Retail Customer Analyzer"
pip install -r requirements.txt
```

### 3. Run Interactively
Launch the interactive console application:
```bash
python retail_customer_analyzer.py
```
*(or via `python main.py`)*

### 4. Run Automated Test Suite
Execute the full test verification suite:
```bash
python test_runner.py
```

### 5. Run Non-Interactively via CLI Arguments
The application supports non-interactive CLI flags for grading and batch scripts:
```bash
# Test Case 1: Spending statistics
python retail_customer_analyzer.py --file customers.csv --menu 1

# Test Case 2: High-value customers with boundary
python retail_customer_analyzer.py --file customers.csv --menu 2 --limit 25000

# Test Case 3a: Non-numeric validation
python retail_customer_analyzer.py --file customers.csv --menu 2 --limit abc

# Test Case 3b: Negative number validation
python retail_customer_analyzer.py --file customers.csv --menu 2 --limit -500

# Test Case 4: City-wise summary
python retail_customer_analyzer.py --file customers.csv --menu 3

# Generate Matplotlib visualization charts
python retail_customer_analyzer.py --file customers.csv --charts
```

---

## 📈 Visualizations

The program includes an automated chart generation engine producing high-resolution (300 DPI) analytics charts:
1. `city_spending_summary.png`: Compares total revenue against average spending per transaction across cities.
2. `customer_spending_distribution.png`: Ranks customer expenditures against dataset mean (Rs. 9,125.00) and median (Rs. 7,500.00) benchmarks.

---

## 👨‍💻 Academic Details
- **Student Name:** Student / Project Author
- **Institution:** Rungta International Skills University
- **Department:** School of Computer Science and Engineering
- **Program:** B.Tech CSE (AI & ML) in association with Microsoft
- **Problem Statement:** PS No. 74 — Retail Customer Analyzer
