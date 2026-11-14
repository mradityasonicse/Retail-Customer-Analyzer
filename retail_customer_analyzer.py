"""
Retail Customer Analyzer
========================
Institution : Rungta International Skills University
School      : School of Computer Science and Engineering
Program     : B.Tech CSE (AI & ML) in association with Microsoft
PS No.      : 74
Title       : Retail Customer Analyzer

Concepts    : Pandas, Filtering, Grouping, Statistics, Data Validation
Language    : Python 3
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np


def format_amount(value):
    """
    Format monetary amounts: display as an integer if it has no fractional part,
    otherwise display with two decimal places.
    """
    try:
        val_float = float(value)
        if val_float.is_integer():
            return str(int(val_float))
        return f"{val_float:.2f}"
    except (ValueError, TypeError):
        return str(value)


def load_customer_data(file_path):
    """
    Loads customer data from a CSV file using Pandas with robust error handling.
    Validates presence of file and required schema columns.
    
    Returns:
        tuple: (pandas.DataFrame or None, str or None) -> (df, error_message)
    """
    if not file_path:
        return None, "Error: No file path provided."

    clean_path = str(file_path).strip().strip("'\"").lstrip("\ufeff")

    if not os.path.exists(clean_path):
        return None, f"Error: File '{clean_path}' not found. Please verify the file path."

    try:
        # Load with pandas
        df = pd.read_csv(clean_path)

        if df.empty:
            return None, f"Error: File '{clean_path}' is empty."

        # Normalize column headers (strip whitespace and handle casing)
        col_map = {}
        for col in df.columns:
            cleaned_col = str(col).strip().lstrip("\ufeff")
            lower_col = cleaned_col.lower()
            if "customerid" in lower_col or "customer_id" in lower_col or "id" == lower_col:
                col_map[col] = "CustomerID"
            elif "name" in lower_col:
                col_map[col] = "Name"
            elif "city" in lower_col:
                col_map[col] = "City"
            elif "purchases" in lower_col or "purchase" in lower_col:
                col_map[col] = "Purchases"
            elif "totalspent" in lower_col or "total_spent" in lower_col or "spent" in lower_col:
                col_map[col] = "TotalSpent"

        df = df.rename(columns=col_map)

        # Validate required columns
        required_cols = ["CustomerID", "Name", "City", "Purchases", "TotalSpent"]
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            return None, f"Error: Missing required column(s) in CSV: {', '.join(missing_cols)}"

        # Coerce numeric fields
        df["Purchases"] = pd.to_numeric(df["Purchases"], errors="coerce").fillna(0).astype(int)
        df["TotalSpent"] = pd.to_numeric(df["TotalSpent"], errors="coerce")

        # Drop any row where TotalSpent is NaN
        df = df.dropna(subset=["TotalSpent"]).reset_index(drop=True)

        return df, None

    except pd.errors.EmptyDataError:
        return None, f"Error: File '{clean_path}' contains no readable data."
    except Exception as e:
        return None, f"Error reading file '{clean_path}': {str(e)}"


def get_spending_statistics(df):
    """
    Computes spending statistics:
    - Mean spend (2 decimal places)
    - Median spend (2 decimal places)
    - Highest spending customer (Name and TotalSpent)
    - Lowest spending customer (Name and TotalSpent)

    Returns:
        list of str: Formatted output lines exactly matching Test Case 1 specification.
    """
    if df is None or df.empty:
        return ["Error: No data available to calculate statistics."]

    mean_val = df["TotalSpent"].mean()
    median_val = df["TotalSpent"].median()

    # Locate highest and lowest spending records
    highest_idx = df["TotalSpent"].idxmax()
    lowest_idx = df["TotalSpent"].idxmin()

    highest_row = df.loc[highest_idx]
    lowest_row = df.loc[lowest_idx]

    highest_name = highest_row["Name"]
    highest_spent = format_amount(highest_row["TotalSpent"])

    lowest_name = lowest_row["Name"]
    lowest_spent = format_amount(lowest_row["TotalSpent"])

    lines = [
        f"Mean spend: Rs. {mean_val:.2f}",
        f"Median spend: Rs. {median_val:.2f}",
        f"Highest: {highest_name} (Rs. {highest_spent})",
        f"Lowest: {lowest_name} (Rs. {lowest_spent})"
    ]
    return lines


def validate_spending_limit(limit_input):
    """
    Validates user input for spending limit:
    - Must be a valid numeric value.
    - Must be >= 0.

    Returns:
        tuple: (float or None, str or None) -> (valid_limit, error_message)
    """
    if limit_input is None:
        return None, "Invalid amount. Please enter a number."

    limit_str = str(limit_input).strip()
    try:
        val = float(limit_str)
    except ValueError:
        return None, "Invalid amount. Please enter a number."

    if val < 0:
        return None, "Amount must be 0 or more."

    return val, None


def get_high_value_customers(df, limit_value):
    """
    Filters customers whose TotalSpent >= limit_value.

    Returns:
        list of str: Formatted output lines matching Test Case 2 specification.
    """
    if df is None or df.empty:
        return ["Error: No data available."]

    limit_num, err = validate_spending_limit(limit_value)
    if err:
        return [err]

    formatted_limit = format_amount(limit_num)
    filtered_df = df[df["TotalSpent"] >= limit_num]

    header = f"High-value customers (TotalSpent >= {formatted_limit}):"
    lines = [header]

    if filtered_df.empty:
        lines.append(f"No customers found with TotalSpent >= {formatted_limit}.")
        return lines

    for _, row in filtered_df.iterrows():
        cid = str(row["CustomerID"]).strip()
        name = str(row["Name"]).strip()
        city = str(row["City"]).strip()
        spent = format_amount(row["TotalSpent"])
        lines.append(f"{cid} | {name} | {city} | Rs. {spent}")

    return lines


def get_city_wise_summary(df):
    """
    Groups data by City, calculates Total and Average TotalSpent per city,
    sorted by Total spending descending.

    Returns:
        list of str: Formatted output lines matching Test Case 4 specification.
    """
    if df is None or df.empty:
        return ["Error: No data available to calculate city summary."]

    city_group = df.groupby("City", as_index=False).agg(
        Total=("TotalSpent", "sum"),
        Average=("TotalSpent", "mean"),
        CustomerCount=("CustomerID", "count")
    )

    # Sort descending by Total spending to match specification
    city_group = city_group.sort_values(by="Total", ascending=False).reset_index(drop=True)

    lines = []
    for _, row in city_group.iterrows():
        city_name = str(row["City"]).strip()
        total_str = format_amount(row["Total"])
        avg_float = float(row["Average"])
        lines.append(f"{city_name} : Total Rs. {total_str} | Average Rs. {avg_float:.2f}")

    return lines


def generate_charts(df, output_dir=None):
    """
    Generates high-resolution Matplotlib charts for visual insights:
    1. city_spending_summary.png - Total and Average spending per city
    2. customer_spending_distribution.png - Individual customer spending vs mean/median
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend safe for all environments
        import matplotlib.pyplot as plt

        target_dir = output_dir if output_dir else os.path.dirname(os.path.abspath(__file__))

        # --- Chart 1: City-wise Spending Summary ---
        city_group = df.groupby("City", as_index=False).agg(
            Total=("TotalSpent", "sum"),
            Average=("TotalSpent", "mean")
        ).sort_values(by="Total", ascending=False)

        cities = city_group["City"].tolist()
        totals = city_group["Total"].tolist()
        averages = city_group["Average"].tolist()

        x = np.arange(len(cities))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        rects1 = ax.bar(x - width/2, totals, width, label="Total Spending (Rs.)", color="#2563EB", edgecolor="#1E40AF")
        rects2 = ax.bar(x + width/2, averages, width, label="Average Spending (Rs.)", color="#10B981", edgecolor="#047857")

        ax.set_title("Retail Customer Analyzer: City-wise Spending Summary", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("City", fontsize=11, fontweight="bold")
        ax.set_ylabel("Amount (Rs.)", fontsize=11, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(cities, fontsize=10)
        ax.legend(frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        # Bar value annotations
        for rect in rects1:
            height = rect.get_height()
            ax.annotate(f"Rs. {int(height)}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")

        for rect in rects2:
            height = rect.get_height()
            ax.annotate(f"Rs. {height:.1f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")

        fig.tight_layout()
        chart1_path = os.path.join(target_dir, "city_spending_summary.png")
        fig.savefig(chart1_path)
        plt.close(fig)

        # --- Chart 2: Customer Spending Distribution ---
        sorted_customers = df.sort_values(by="TotalSpent", ascending=True)
        names = sorted_customers["Name"].tolist()
        spent = sorted_customers["TotalSpent"].tolist()

        fig2, ax2 = plt.subplots(figsize=(9, 5), dpi=300)
        bars = ax2.barh(names, spent, color="#6366F1", edgecolor="#4338CA", height=0.6)

        mean_val = df["TotalSpent"].mean()
        median_val = df["TotalSpent"].median()

        ax2.axvline(mean_val, color="#EF4444", linestyle="--", linewidth=1.5, label=f"Mean (Rs. {mean_val:.2f})")
        ax2.axvline(median_val, color="#F59E0B", linestyle="-.", linewidth=1.5, label=f"Median (Rs. {median_val:.2f})")

        ax2.set_title("Retail Customer Analyzer: Individual Customer Spending", fontsize=14, fontweight="bold", pad=15)
        ax2.set_xlabel("Total Spent (Rs.)", fontsize=11, fontweight="bold")
        ax2.set_ylabel("Customer Name", fontsize=11, fontweight="bold")
        ax2.legend(loc="lower right", frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1")
        ax2.grid(axis="x", linestyle="--", alpha=0.5)

        for bar in bars:
            width_val = bar.get_width()
            ax2.annotate(f"Rs. {int(width_val)}",
                         xy=(width_val, bar.get_y() + bar.get_height() / 2),
                         xytext=(5, 0), textcoords="offset points",
                         ha="left", va="center", fontsize=8, fontweight="bold")

        fig2.tight_layout()
        chart2_path = os.path.join(target_dir, "customer_spending_distribution.png")
        fig2.savefig(chart2_path)
        plt.close(fig2)

        return True, [chart1_path, chart2_path]

    except Exception as e:
        return False, [f"Error generating charts: {str(e)}"]


def run_interactive(file_path="customers.csv"):
    """
    Runs the full interactive console interface for the user.
    """
    print("=" * 60)
    print("           RETAIL CUSTOMER ANALYZER (PS NO. 74)          ")
    print("       Rungta International Skills University, CSE      ")
    print("=" * 60)

    current_file = file_path
    df, err = load_customer_data(current_file)

    while df is None:
        print(f"\n[!] {err}")
        try:
            current_file = input("Enter path to customers CSV file (or 'exit' to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting program.")
            return

        if current_file.lower() in ["exit", "quit", "q"]:
            print("Exiting program.")
            return

        df, err = load_customer_data(current_file)

    print(f"\n[+] Successfully loaded: {current_file}")
    print(f"[+] Total Customers: {len(df)} | Columns: {list(df.columns)}")

    while True:
        print("\n" + "-" * 50)
        print(f"ACTIVE FILE: {current_file}")
        print("MAIN MENU:")
        print("  1. Spending statistics")
        print("  2. High-value customers")
        print("  3. City-wise summary")
        print("  4. Generate Graphical Charts (Matplotlib)")
        print("  5. Change CSV file")
        print("  6. Exit")
        print("-" * 50)

        try:
            choice = input("Enter choice (1-6 or Menu Name): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        cleaned_choice = choice.lower().replace("_", " ").replace("-", " ")

        if cleaned_choice in ["1", "spending statistics", "spending", "stats"]:
            print("\n--- Spending Statistics ---")
            lines = get_spending_statistics(df)
            for line in lines:
                print(line)

        elif cleaned_choice in ["2", "high value customers", "high value", "filter"]:
            print("\n--- High-Value Customers Filter ---")
            try:
                limit_in = input("Enter spending limit: ").strip()
            except (EOFError, KeyboardInterrupt):
                continue

            lines = get_high_value_customers(df, limit_in)
            for line in lines:
                print(line)

        elif cleaned_choice in ["3", "city wise summary", "city wise", "city summary", "cities"]:
            print("\n--- City-wise Summary ---")
            lines = get_city_wise_summary(df)
            for line in lines:
                print(line)

        elif cleaned_choice in ["4", "charts", "visualizations", "plot"]:
            print("\nGenerating charts...")
            success, paths = generate_charts(df, os.path.dirname(os.path.abspath(current_file)))
            if success:
                print("[+] Charts generated successfully:")
                for p in paths:
                    print(f"    - {os.path.basename(p)}")
            else:
                print(f"[!] Chart generation error: {paths[0]}")

        elif cleaned_choice in ["5", "change file", "load file", "change"]:
            try:
                new_file = input("Enter path to new CSV file: ").strip()
            except (EOFError, KeyboardInterrupt):
                continue

            new_df, new_err = load_customer_data(new_file)
            if new_df is not None:
                df = new_df
                current_file = new_file
                print(f"[+] Loaded '{current_file}' successfully with {len(df)} records.")
            else:
                print(f"[!] {new_err}")
                print(f"[*] Keeping current file: {current_file}")

        elif cleaned_choice in ["6", "exit", "quit", "q"]:
            print("\nThank you for using Retail Customer Analyzer. Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")


def main():
    """
    Main entry point supporting both CLI automation arguments and interactive mode.
    """
    parser = argparse.ArgumentParser(
        description="Retail Customer Analyzer (Problem Statement No. 74) - Rungta International Skills University"
    )
    parser.add_argument(
        "--file", "-f", default="customers.csv", help="Path to customers.csv file (default: customers.csv)"
    )
    parser.add_argument(
        "--menu", "-m", choices=["1", "2", "3", "4", "Spending statistics", "High-value customers", "City-wise summary"],
        help="Directly run a menu option non-interactively"
    )
    parser.add_argument(
        "--limit", "-l", help="Spending limit for Menu Option 2 (High-value customers)"
    )
    parser.add_argument(
        "--charts", action="store_true", help="Generate analytics charts to current working directory"
    )

    args = parser.parse_args()

    # If menu option specified via CLI, run non-interactively
    if args.menu:
        df, err = load_customer_data(args.file)
        if err:
            print(err)
            sys.exit(1)

        menu_val = args.menu.lower()
        if menu_val in ["1", "spending statistics"]:
            for line in get_spending_statistics(df):
                print(line)

        elif menu_val in ["2", "high-value customers"]:
            limit_val = args.limit
            if limit_val is None:
                # Prompt if not provided via flag
                limit_val = input("Enter spending limit: ").strip()
            for line in get_high_value_customers(df, limit_val):
                print(line)

        elif menu_val in ["3", "city-wise summary"]:
            for line in get_city_wise_summary(df):
                print(line)

        elif menu_val in ["4"]:
            success, paths = generate_charts(df)
            for p in paths:
                print(p)

        if args.charts:
            generate_charts(df)

        return

    # If --charts flag alone is passed
    if args.charts:
        df, err = load_customer_data(args.file)
        if err:
            print(err)
            sys.exit(1)
        success, paths = generate_charts(df)
        for p in paths:
            print(p)
        return

    # Otherwise run full interactive console loop
    run_interactive(args.file)


if __name__ == "__main__":
    main()
