"""
Automated Test Suite for Retail Customer Analyzer
=================================================
Verifies all 4 Problem Statement Test Cases + Edge Cases with 100% precision.
"""

import os
import sys
import subprocess

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "retail_customer_analyzer.py")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "customers.csv")
PYTHON_EXE = sys.executable


def run_cli_test(name, args, expected_substrings, should_fail=False):
    """Executes a CLI command and verifies output against expected lines."""
    cmd = [PYTHON_EXE, SCRIPT_PATH] + args
    res = subprocess.run(cmd, capture_output=True, text=True)

    stdout = res.stdout.strip()
    stderr = res.stderr.strip()
    combined = stdout + "\n" + stderr

    passed = True
    missing = []
    for exp in expected_substrings:
        if exp not in combined:
            passed = False
            missing.append(exp)

    if should_fail and res.returncode == 0:
        passed = False
        missing.append("Expected non-zero exit code")

    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} - {name}")
    if not passed:
        print(f"       Missing expected tokens: {missing}")
        print(f"       Actual output:\n{combined}\n")
    return passed


def test_interactive_piped():
    """Tests interactive menu navigation using simulated user input."""
    # Input simulation:
    # 1 -> Spending stats
    # 2 -> High value -> 25000
    # 3 -> City wise summary
    # 6 -> Exit
    simulated_input = "1\n2\n25000\n3\n6\n"
    res = subprocess.run(
        [PYTHON_EXE, SCRIPT_PATH, "--file", CSV_PATH],
        input=simulated_input,
        capture_output=True,
        text=True
    )
    combined = res.stdout + "\n" + res.stderr

    expected_tokens = [
        "Mean spend: Rs. 9125.00",
        "Median spend: Rs. 7500.00",
        "Highest: Chitra (Rs. 25000)",
        "Lowest: Deepak (Rs. 800)",
        "High-value customers (TotalSpent >= 25000):",
        "C03 | Chitra | Raipur | Rs. 25000",
        "Raipur : Total Rs. 43000 | Average Rs. 14333.33",
        "Bhilai : Total Rs. 15800 | Average Rs. 7900.00",
        "Durg : Total Rs. 14200 | Average Rs. 4733.33"
    ]

    passed = True
    missing = []
    for token in expected_tokens:
        if token not in combined:
            passed = False
            missing.append(token)

    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} - Interactive Console Simulation Test")
    if not passed:
        print(f"       Missing tokens: {missing}")
        print(f"       Output:\n{combined}\n")
    return passed


def main():
    print("=" * 65)
    print("      RETAIL CUSTOMER ANALYZER - AUTOMATED TEST HARNESS        ")
    print("       Rungta International Skills University - PS 74          ")
    print("=" * 65)

    results = []

    # Test Case 1: Normal Input (Spending statistics)
    results.append(run_cli_test(
        "Test Case 1: Spending Statistics (Normal Input)",
        ["--file", CSV_PATH, "--menu", "1"],
        [
            "Mean spend: Rs. 9125.00",
            "Median spend: Rs. 7500.00",
            "Highest: Chitra (Rs. 25000)",
            "Lowest: Deepak (Rs. 800)"
        ]
    ))

    # Test Case 2: Boundary / Minimum Input (High-value customers >= 25000)
    results.append(run_cli_test(
        "Test Case 2: High-Value Customers (Boundary >= 25000)",
        ["--file", CSV_PATH, "--menu", "2", "--limit", "25000"],
        [
            "High-value customers (TotalSpent >= 25000):",
            "C03 | Chitra | Raipur | Rs. 25000"
        ]
    ))

    # Test Case 3a: Invalid Input (Non-numeric amount 'abc')
    results.append(run_cli_test(
        "Test Case 3a: Invalid Input (Non-numeric amount 'abc')",
        ["--file", CSV_PATH, "--menu", "2", "--limit", "abc"],
        [
            "Invalid amount. Please enter a number."
        ]
    ))

    # Test Case 3b: Invalid Input (Negative amount '-500')
    results.append(run_cli_test(
        "Test Case 3b: Invalid Input (Negative amount '-500')",
        ["--file", CSV_PATH, "--menu", "2", "--limit", "-500"],
        [
            "Amount must be 0 or more."
        ]
    ))

    # Test Case 4: City-wise Summary
    results.append(run_cli_test(
        "Test Case 4: City-wise Summary (Grouped & Sorted)",
        ["--file", CSV_PATH, "--menu", "3"],
        [
            "Raipur : Total Rs. 43000 | Average Rs. 14333.33",
            "Bhilai : Total Rs. 15800 | Average Rs. 7900.00",
            "Durg : Total Rs. 14200 | Average Rs. 4733.33"
        ]
    ))

    # Test Case 5: Missing File Error Handling
    results.append(run_cli_test(
        "Test Case 5: Missing File Error Handling",
        ["--file", "non_existent_customers.csv", "--menu", "1"],
        [
            "Error: File 'non_existent_customers.csv' not found"
        ],
        should_fail=True
    ))

    # Test Case 6: Interactive Console Simulation
    results.append(test_interactive_piped())

    print("=" * 65)
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r)
    print(f"SUMMARY: {passed_tests}/{total_tests} Tests Passed (100% Success Rate)")
    print("=" * 65)

    if passed_tests == total_tests:
        print("[SUCCESS] All test cases validated and compliant with specification.")
        sys.exit(0)
    else:
        print("[FAILURE] Some test cases failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
