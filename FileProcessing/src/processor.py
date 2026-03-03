from file_reader import read_csv_file
from validator import validate_all_records
from transformer import calculate_totals, aggregate_by_product, aggregate_by_store
from report_writer import write_summary_report, write_clean_csv, write_error_log

def process_sales_file(input_path: str, output_dir: str):
    """
    Main processing pipeline.
    
    1. Read the input file
    2. Validate all records
    3. Transform valid records
    4. Generate reports
    5. Handle any errors gracefully
    
    Returns: ProcessingResult with statistics
    """
    
    records: list[dict] = read_csv_file(input_path)
    valid_records, error_list = validate_all_records(records)
    transformed_records: list[dict] = calculate_totals(valid_records)
    aggregates: list = [aggregate_by_store(transformed_records), aggregate_by_product(transformed_records)]

    write_summary_report(output_dir, transformed_records, error_list, aggregates)
    write_clean_csv("clean-sales.csv", transformed_records)
    write_error_log("errors.txt", error_list)

if __name__ == "__main__":
    # Process from command line
    
    process_sales_file("../sample-sales.csv", "./")
