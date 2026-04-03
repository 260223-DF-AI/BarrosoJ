# Data Quality Report

**Generated**: 2026-03-28 16:20:21
**File**: sample_data.csv
**Total Rows**: 50

## Summary

| Check | Status | Issues Found |
| ----- | ------ | ------------ |
| Null Values | WARNING | 3 |
| Duplicates | FAIL | 2 |
| Negative Values | WARNING | 2 |
| Future Dates | WARNING | 1 |
| Email Format | WARNING | 1 |

## Detailed Results

### Null Values - WARNING
Found missing values in: {'customer_name': 3}

### Duplicates - FAIL
Duplicate IDs found: {1010: 2, 1011: 2}

### Email Format - WARNING
Malformed indices: [7]
