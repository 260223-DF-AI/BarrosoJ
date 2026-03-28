import os
import pandas as pd
from report_generator import gather_quality_check_data, generate_report

def main():
    # 1. Configuration
    input_file = "sample_data.csv"
    output_dir = "output"
    output_path = os.path.join(output_dir, "report.md")
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"--- Starting Data Quality Check for {input_file} ---")

    try:
        # 2. Read the CSV file
        df = pd.read_csv(input_file)
        
        # 3. Run all quality checks via report_generator
        results = gather_quality_check_data(df)
        
        # 4. Generate the report and save it to output/report.md
        # (Modified to accept a specific output path)
        generate_report(df, results, input_file)
        
        # Moving the generated file to the desired output folder
        # Note: If you modified generate_report to accept a path, 
        # you can pass output_path directly.
        if os.path.exists("quality_report.md"):
            os.rename("quality_report.md", output_path)

        # 5. Print a summary to the console
        print("\n[SUMMARY OF ISSUES]")
        print("-" * 20)
        print(f"Total Rows Processed: {len(df)}")
        print(f"Missing Names:       {results['nulls'].get('customer_name', 0)}")
        print(f"Duplicate IDs:       {len(results['duplicates'])}")
        print(f"Negative Amounts:    {results['negatives'].get('amount', 0)}")
        print(f"Future Dates:        {results['future_dates']['future_date_count']}")
        print(f"Malformed Emails:    {results['emails']['invalid_email_count']}")
        print("-" * 20)
        print(f"Success! Full report saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found. Please run the data generation script first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()