import pandas as pd
from datetime import datetime
import quality_checks as qc

def gather_quality_check_data(df: pd.DataFrame):
    """
    Runs all imported quality checks and aggregates results.
    """
    results = {
        "nulls": qc.check_nulls(df),
        "duplicates": qc.check_duplicates(df, 'order_id'),
        "negatives": qc.check_negative_values(df, ['amount']),
        "future_dates": qc.check_future_dates(df, 'order_date'),
        "emails": qc.check_email_format(df, 'email')
    }
    return results

def generate_report(df: pd.DataFrame, results: dict, filename: str) -> None:
    """
    Generates a Markdown report using quality check data.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_rows = len(df)
    
    # Helper to determine Status
    def get_status(count, is_critical=False):
        if count == 0: return "PASS"
        return "FAIL" if is_critical else "WARNING"

    # 1. Summary Table Calculation
    summary_data = [
        ("Null Values", get_status(sum(results['nulls'].values())), sum(results['nulls'].values())),
        ("Duplicates", get_status(len(results['duplicates']), True), len(results['duplicates'])),
        ("Negative Values", get_status(results['negatives'].get('amount', 0)), results['negatives'].get('amount', 0)),
        ("Future Dates", get_status(results['future_dates']['future_date_count']), results['future_dates']['future_date_count']),
        ("Email Format", get_status(results['emails']['invalid_email_count']), results['emails']['invalid_email_count']),
    ]

    # 2. Build Markdown String
    report = f"# Data Quality Report\n\n"
    report += f"**Generated**: {now}\n"
    report += f"**File**: {filename}\n"
    report += f"**Total Rows**: {total_rows}\n\n"
    
    report += "## Summary\n\n"
    report += "| Check | Status | Issues Found |\n| ----- | ------ | ------------ |\n"
    for name, status, count in summary_data:
        report += f"| {name} | {status} | {count} |\n"

    report += "\n## Detailed Results\n\n"
    
    # Detailed section: Nulls
    report += f"### Null Values - {get_status(sum(results['nulls'].values()))}\n"
    report += f"Found missing values in: { {k: v for k, v in results['nulls'].items() if v > 0} }\n\n"

    # Detailed section: Duplicates
    report += f"### Duplicates - {get_status(len(results['duplicates']), True)}\n"
    report += f"Duplicate IDs found: {results['duplicates']}\n\n"

    # Detailed section: Emails
    report += f"### Email Format - {get_status(results['emails']['invalid_email_count'])}\n"
    report += f"Malformed indices: {results['emails']['invalid_indices']}\n"

    # Print or Save to file
    with open("quality_report.md", "w") as f:
        f.write(report)
    
    print("Report generated: quality_report.md")

# --- Example Usage ---
if __name__ == "__main__":
    df = pd.read_csv("customer_orders_dirty.csv")
    data_results = gather_quality_check_data(df)
    generate_report(df, data_results, "customer_orders_dirty.csv")