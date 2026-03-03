from datetime import datetime

def write_summary_report(filepath: str, valid_records: list[dict], errors: list[str], aggregations: list[dict]):
    """
    Write a formatted summary report.
    
    Report should include:
    - Processing timestamp
    - Total records processed
    - Number of valid records
    - Number of errors (with details)
    - Sales by store
    - Top 5 products
    """

    store_aggregate, product_aggregate = aggregations[0], aggregations[1]
    store_aggregate = sorted(store_aggregate, key=lambda x: x["total"])
    top_5_products = sorted(product_aggregate, key=lambda x: x["product"])
    
    report: str = f"""Time:{datetime.now().strftime("%d/%m, %H:%M:%S")}
Total processed: {len(valid_records) + len(errors)}
Valid records: {len(valid_records)}
Errors: {len(errors)}\n{"\n".join(errors)}
Sales by store: {store_aggregate}
Top 5 products:{top_5_products}
"""

def write_clean_csv(filepath: str, records: list[dict]):
    """
    Write validated records to a clean CSV file.
    """
    with open(filepath, "w") as f:
        for record in records:
            f.write(",".join(record.values()))

def write_error_log(filepath: str, errors: list[str]):
    """
    Write processing errors to a log file.
    """
    with open(filepath, "a+") as f:
        f.writelines(errors)
