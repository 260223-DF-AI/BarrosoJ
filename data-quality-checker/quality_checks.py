from datetime import datetime
import pandas as pd
import re

def check_nulls(df: pd.DataFrame) -> dict:
    """Check for null values in each column."""
    # .isnull() identifies the nulls, .sum() counts them per column, 
    # and .to_dict() converts the resulting Series to a dictionary.
    return df.isnull().sum().to_dict()


def check_duplicates(df: pd.DataFrame, key_column: str) -> dict:
    """Find duplicate rows based on a key column and return counts."""
    # Filter for rows where the key_column is duplicated
    duplicates = df[df.duplicated(subset=[key_column], keep=False)]
    
    # Group by the key_column and count occurrences for each duplicated ID
    # This creates a dictionary of {value: count} for every non-unique entry
    return duplicates[key_column].value_counts().to_dict()


def check_negative_values(df: pd.DataFrame, numeric_columns: list) -> dict:
    """Flag negative values in specified numeric columns."""
    negative_report = {}
    
    for col in numeric_columns:
        if col in df.columns:
            # Filter for values less than zero and count them
            count = (df[col] < 0).sum()
            negative_report[col] = int(count)
            
    return negative_report


def check_future_dates(df: pd.DataFrame, date_column: str) -> dict:
    """Check for dates in the future."""
    # Ensure the column is in datetime format
    # errors='coerce' will turn unparseable dates into NaT (Not a Time)
    dates = pd.to_datetime(df[date_column], errors='coerce')
    
    # Get the current time for comparison
    now = datetime.now()
    
    # Filter for dates that are strictly greater than 'now'
    future_mask = dates > now
    future_count = future_mask.sum()
    
    # Return a report with the count and optionally the indices of the bad data
    return {
        "column": date_column,
        "future_date_count": int(future_count),
        "invalid_indices": df.index[future_mask].tolist()
    }


def check_email_format(df: pd.DataFrame, email_column: str) -> dict:
    """Validate email format in the specified column."""
    # A standard regex pattern for: local-part @ domain . extension
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # We use .str.match() which returns a boolean Series
    # We then negate it (~) to find the rows that DO NOT match the pattern
    # We also fill NaNs with False because a null isn't "malformed," it's "missing"
    invalid_mask = ~df[email_column].astype(str).str.match(email_regex, na=False)
    
    # Optional: Exclude nulls from this specific check if you want to handle them separately
    invalid_mask = invalid_mask & df[email_column].notnull()
    
    return {
        "column": email_column,
        "invalid_email_count": int(invalid_mask.sum()),
        "invalid_indices": df.index[invalid_mask].tolist()
    }