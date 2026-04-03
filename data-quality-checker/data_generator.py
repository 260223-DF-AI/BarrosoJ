import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 1. Setup basic data
rows = 50
data = {
    'order_id': [1000 + i for i in range(rows)],
    'customer_name': [f"Customer {i}" for i in range(rows)],
    'email': [f"user{i}@example.com" for i in range(rows)],
    'order_date': [(datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d') for i in range(rows)],
    'amount': [round(random.uniform(10.0, 500.0), 2) for i in range(rows)],
    'status': [random.choice(['pending', 'completed', 'cancelled']) for i in range(rows)]
}

df = pd.DataFrame(data)

# 2. Inject deliberate data quality issues
# 3 rows with null customer_name
df.loc[0:2, 'customer_name'] = np.nan

# 2 duplicate order_ids (reusing ID 1010 and 1011)
df.loc[3, 'order_id'] = 1010
df.loc[4, 'order_id'] = 1011

# 2 rows with negative amounts
df.loc[5, 'amount'] = -50.00
df.loc[6, 'amount'] = -125.50

# 1 row with an invalid email
df.loc[7, 'email'] = "bad_email_format.com"

# 1 row with a future date
df.loc[8, 'order_date'] = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

# 1 row with an invalid status
df.loc[9, 'status'] = "unknown_status"

# 3. Save to CSV
file_name = "sample_data.csv"
df.to_csv(file_name, index=False)

print(f"Success! '{file_name}' has been created with 50 rows and intentional errors.")