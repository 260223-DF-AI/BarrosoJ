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

    store_aggregate = sorted(store_aggregate.items(), key=lambda x: x[1], reverse=True)
    top_5_products = sorted(product_aggregate.items(), key=lambda x: x[1], reverse=True)[:5]

    store_aggregate_str: str = ""
    # for i, store in enumerate(store_aggregate):
    for store in store_aggregate:
        store_aggregate_str += f"\t-{store[0]}: ${store[1]}\n"

    product_str: str = ""
    for i, product in enumerate(top_5_products):
        product_str += f"\t{i+1}. {product[0]}: {product[1]} units\n"
    
    report: str = f"""Time: {datetime.now().strftime("%d/%m, %H:%M:%S")}
Total processed: {len(valid_records) + len(errors)}
Valid records: {len(valid_records)}
Errors: {len(errors)}\n\t{"\n\t".join(errors)}

Sales by store:
{store_aggregate_str}
Top 5 products:
{product_str}
"""
    
    with open(filepath, "w") as f:
        f.write(report)
    
    print(report)

def write_clean_csv(filepath: str, records: list[dict]):
    """
    Write validated records to a clean CSV file.
    """
    with open(filepath, "w") as f:
        for record in records:
            info = record.values()
            f.write(",".join([str(x) for x in info]) + "\n")

def write_error_log(filepath: str, errors: list[str]):
    """
    Write processing errors to a log file.
    """
    # write errors list with added new lines to error log file
    with open(filepath, "w") as f:
        f.writelines([x+"\n" for x in errors])
