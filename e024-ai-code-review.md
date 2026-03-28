# Exercise: AI Code Review Challenge

## Exercise ID: e024

## Overview

In this exercise, you will review AI-generated code for correctness, security, and best practices. You will act as the senior engineer reviewing pull requests from an "AI junior developer." This exercise builds the critical review skills necessary for production-quality AI-assisted development.

## Learning Objectives

- Review AI-generated code systematically for bugs and vulnerabilities
- Identify common patterns where AI produces incorrect or insecure code
- Apply a structured review checklist to AI output
- Improve AI-generated code to meet production standards

## Prerequisites

- Python 3.10+ knowledge
- SQL/BigQuery knowledge
- Completed Thursday written content on AI testing and debugging

## Time Estimate

45-60 minutes

---

## Part 1: Bug Detection (20 minutes)

Review the following AI-generated code snippets. Each contains at least one bug. Find and fix all bugs.

### Snippet 1: Data Deduplication

The AI was asked: "Write a Python function to deduplicate a DataFrame keeping the most recent record."

```python
def deduplicate_records(df, key_column, date_column):
    """Remove duplicate records, keeping the most recent."""
    df_sorted = df.sort_values(date_column, ascending=True)
    df_deduped = df_sorted.drop_duplicates(subset=key_column, keep='first')
    return df_deduped
```

**Questions:**

1. What bug(s) exist in this code? The DF should be sorted by descending, as the earliest records will be "first", and thus kept by drop_duplicates(keep='first')
2. What is the fix? sort_values by ascending=False (or keep='last', but I prefer ascending=False)
3. What edge cases are not handled? 

- If the dates are not datetime objects they may be sorted incorrectly.


### Snippet 2: BigQuery Table Creation

The AI was asked: "Write a function to create a partitioned BigQuery table."

```python
from google.cloud import bigquery

def create_partitioned_table(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    
    schema = [
        bigquery.SchemaField("order_id", "INTEGER"),
        bigquery.SchemaField("customer_id", "INTEGER"),
        bigquery.SchemaField("order_date", "DATE"),
        bigquery.SchemaField("amount", "FLOAT"),
    ]
    
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    table = bigquery.Table(table_ref, schema=schema)
    
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="order_date",
        expiration_ms=7776000000  # 90 days
    )
    
    table = client.create_table(table)
    print(f"Created table {table.table_id}")
    return table
```

**Questions:**

1. Is this code functionally correct?
2. What happens if the table already exists? An error will be raised
3. What data type issue exists with the `amount` field for financial data? It will use floating point numbers, which are imprecise and not ideal for financial data.
4. Is `expiration_ms` appropriate for a production fact table? What risks does it create? The business may want to go back and look at past data, either for analysis reasons or for compliance reasons.

### Snippet 3: CSV Processing Pipeline

The AI was asked: "Write a function to process CSV files and load to BigQuery."

```python
import pandas as pd
from google.cloud import bigquery

def process_and_load(file_path, table_id):
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Clean data
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    
    # Load to BigQuery
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    
    print(f"Loaded {len(df)} rows to {table_id}")
```

**Questions:**

1. What happens if the file does not exist? error :(
2. What happens if the `date` column contains invalid dates? ValueError :(
3. Is `dropna()` appropriate? What data might be lost? It may disregard perfectly usable and valid data solely because one column (possibly intentionally nullable) missing a value will get the whole entry thrown out.
4. What write disposition is used by default? Is this safe? BigQuery appends by default when using load_table_from_dataframe. It may not be safe as this operation is not idempotent - it would be worth having some sort of method to ensure the dataframe in this dataframe does not yet exist in bigquery.
5. What logging/monitoring is missing? The entries being dropped from the dataset should be logged for manual inspection. Other logging on the dataset and possible errors/edge cases of this function (like type problems, file read error, etc) should also be logged.

---

## Part 2: Security Review (15 minutes)

Review these AI-generated snippets for security issues.

### Snippet 4: Database Connection

```python
import os
from google.cloud import bigquery

def get_client():
    # Service account credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/keys/service-account.json'
    client = bigquery.Client(project='production-project-12345')
    return client

def run_query(query_text):
    client = get_client()
    query = f"SELECT * FROM analytics.customers WHERE name = '{query_text}'"
    results = client.query(query).result()
    return [dict(row) for row in results]
```

**Questions:**

1. Identify ALL security issues in this code
- The credentials file location is hard-coded, meaning anyone with access to the script's source code (difficult to obfuscate/hide in Python applications) knows where to find the JSON credentials file
- The project ID is hard coded and can give others info on your internal processes
- The query is manually built with an f-string, meaning SQL Injection is possible
2. For each issue, explain the risk
- A malicious actor may gain the keys to your bigquery cloud information
- relatively minor risk but the information can be combined with other information about your cloud services / account details to act maliciously
- SQL Injection may let someone retrieve all of your information, simply run your cloud costs up by running many queries, or drop all of your tables of cloud data
3. Rewrite the code with proper security practices

```
import os
from google.cloud import bigquery

def get_client():
    # Credentials should be handled by the environment, not hardcoded paths
    project_id = os.getenv("GCP_PROJECT_ID")
    return bigquery.Client(project=project_id)

def run_query(customer_name):
    client = get_client()
    
    # Use Parameterized Queries to prevent SQL Injection
    query = "SELECT * FROM analytics.customers WHERE name = @name"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("name", "STRING", customer_name)
        ]
    )
    
    results = client.query(query, job_config=job_config).result()
    return [dict(row) for row in results]
```

### Snippet 5: API Key Usage

```python
import requests

OPENAI_API_KEY = "sk-proj-abc123def456ghi789..."

def generate_summary(text):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": text}]
        }
    )
    return response.json()['choices'][0]['message']['content']
```

**Questions:**

1. What is the primary security issue? The API key should be stored in a .env file. Storing it in code gives access to anyone who can access the project code via a code repository or see their local application's code.
2. What happens if this code is committed to a public repository? Someone can steal the API key and use it themselves.
3. Rewrite using secure credential management

import os
from python-dotenv import python-dotenv

python-dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

---

## Part 3: Best Practices Review (10 minutes)

### Snippet 6: Data Validation

The AI was asked: "Write data validation for our ETL pipeline."

```python
def validate(df):
    if len(df) == 0:
        return False
    if df.isnull().sum().sum() > 0:
        return False
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].str.len().max() > 1000:
                return False
    return True
```

**Questions:**

1. What are the code quality issues?
2. The function returns a boolean -- is this sufficient for production use?
3. Rewrite to provide detailed validation results (which checks failed and why)
4. Add proper logging and documentation

---

## Part 4: Improvement Exercise (Optional, 15 minutes)

Take any ONE snippet from above and create a production-ready version:

1. Fix all bugs and security issues
2. Add comprehensive error handling
3. Add logging
4. Add type hints and docstrings
5. Add input validation
6. Write 3 unit tests for the improved code

You may use AI assistance for this task, but you must review every line of the AI's output and justify each acceptance or modification.

---

## Review Checklist (Print and Use)

For each code snippet:

| # | Check | Status |
| - | ----- | ------ |
| 1 | Does it do what was requested? | |
| 2 | Input validation present? | |
| 3 | Error handling present? | |
| 4 | No hardcoded credentials? | |
| 5 | SQL injection prevention? | |
| 6 | Appropriate logging? | |
| 7 | Type hints included? | |
| 8 | Docstrings present? | |
| 9 | Edge cases handled? | |
| 10 | Would pass code review? | |

## Submission

Submit:

1. Your bug findings for each snippet (Part 1)
2. Your security analysis (Part 2)
3. Your best practices review (Part 3)
4. Your improved code (Part 4, if completed)
5. Brief reflection: What patterns did you notice in AI-generated code issues?
