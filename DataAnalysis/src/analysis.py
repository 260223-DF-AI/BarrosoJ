import pandas as pd
from datetime import datetime
from math import ceil

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the orders dataset.
    - Parse dates correctly
    - Handle missing values
    - Return a clean DataFrame
    """
    
    df: pd.DataFrame = pd.read_csv(filepath)

    # fill in pd.NA value where fields are missing
    df = df.fillna(value=pd.NA)
    return df

def explore_data(df: pd.DataFrame):
    """
    Print basic statistics about the dataset:
    - Shape (rows, columns)
    - Data types
    - Missing value counts
    - Basic statistics for numeric columns
    - Date range covered
    """
    print(f"Dataframe Shape: {df.shape[0]} x {df.shape[1]}")
    print(f"Data types:\n{df.dtypes}\n")
    print(f"Missing values: {df.isna().sum().sum()}\n")

    # basic stats for quantity, unit_price cols
    print(f"""Quantity column statistics:
\tSum: {df['quantity'].sum()}
\tMean: {df['quantity'].mean()}

Unit_price column statistics:
\tSum: {round(df['unit_price'].sum(), 2)}
\tMean: {round(df['unit_price'].mean(), 2)} 
""")
    
    earliest, latest = df['order_date'].min(), df['order_date'].max()
    print(f"Date range covered: {earliest} through {latest}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset:
    - Remove duplicates
    - Fill or drop missing values (document your strategy) - dropping vals
    - Standardize text columns (strip whitespace, consistent case)
    - Add calculated columns: 'total_amount' = quantity * unit_price
    """

    df.drop_duplicates()
    # drop missing values
    df.dropna()

    # strip whitespace & lowercase string columns
    df.apply(lambda x: x.str.lower().strip() if x.dtype == object else x)

    # make new column of value quantity*unit_price
    df['total_amount'] = df.apply(lambda row: row.quantity * row.unit_price, axis=1)
    
    return df

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add time-based features:
    - day_of_week (0=Monday, 6=Sunday)
    - month
    - quarter
    - is_weekend (boolean)
    """

    def day_of_week(row: pd.Series) -> int:
        """Return int representing the day of the week a date was."""
        time: datetime = datetime.strptime(row.order_date, "%Y-%m-%d")
        return time.isoweekday()-1
    
    df['day_of_week'] = df.apply(day_of_week, axis=1)
    

    def month(row: pd.Series) -> int:
        """Return month the day represents."""
        time: datetime = datetime.strptime(row.order_date, "%Y-%m-%d")
        return time.month
    
    df['month'] = df.apply(month, axis=1)
    

    def quarter(row: pd.Series) -> int:
        """Return month the day represents."""
        month_num: int = month(row)
        return ceil(month_num/3)

    df['quarter'] = df.apply(quarter, axis=1)


    def is_weekend(row: pd.Series) -> bool:
        """Return bool representing the date landing on a weekend or not."""
        return day_of_week(row) in [5, 6]
    
    df['is_weekend'] = df.apply(is_weekend, axis=1)


    return df



def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total sales and order count by category.
    Returns: DataFrame with columns [category, total_sales, order_count, avg_order_value]
    Sorted by total_sales descending.
    """

    # gather series of each data point & combine into dataframe to return
    total_sales: pd.Series = df.groupby('category')['total_amount'].sum()
    order_count: pd.Series = df.groupby('category')['quantity'].sum()
    avg_order_value = df.groupby('category')['total_amount'].mean()

    data_dict: dict = {
        "total_sales": total_sales,
        "order_count": order_count,
        "avg_order_value": avg_order_value
    }

    updated_df: pd.DataFrame = pd.DataFrame(data=data_dict)
    
    return updated_df

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total sales by region.
    Returns: DataFrame with columns [region, total_sales, percentage_of_total]
    """
    overall_total_sales = df['total_amount'].sum()

    # Sum total sales per region
    total_by_region: pd.Series = df.groupby('region')['total_amount'].sum()

    # Create DataFrame with region and total_sales columns
    new_df: pd.DataFrame = total_by_region.rename('total_sales').reset_index()

    # Calculate percentage of overall total (as percent 0-100)
    if overall_total_sales and overall_total_sales != 0:
        new_df['percentage_of_total'] = (new_df['total_sales'] / overall_total_sales) * 100
    else:
        new_df['percentage_of_total'] = 0.0

    return new_df

def top_products(df: pd.DataFrame, n:int=10) -> pd.DataFrame:
    """
    Find top N products by total sales.
    Returns: DataFrame with columns [product_name, category, total_sales, units_sold]
    """

    return df.groupby(['product_name', 'category'])['total_amount'].sum().reset_index(name='total_sales').sort_values(by='total_sales', ascending=False).head(n)

def daily_sales_trend(df: pd.DataFrame):
    """
    Calculate daily sales totals.
    Returns: DataFrame with columns [date, total_sales, order_count]
    """

    new_df = df.groupby('order_date').agg(total_sales=('total_amount', 'sum'), order_count=('quantity', 'sum')).reset_index()    
    return new_df

def customer_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze customer purchasing behavior.
    Returns: DataFrame with columns [customer_id, total_spent, order_count, 
             avg_order_value, favorite_category]
    """
    
    new_df = df.groupby('customer_id').agg(
        total_spent=('total_amount', 'sum'),
        order_count=('quantity', 'sum'),
        avg_order_value=('total_amount', 'mean'),
        favorite_category=('category', lambda x: x.mode()[0] if not x.mode().empty else pd.NA)
    ).reset_index()

    return new_df

def weekend_vs_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare weekend vs weekday sales.
    Returns: Dict with weekend and weekday total sales and percentages.
    """
    new_df: pd.DataFrame = df.groupby('is_weekend')['total_amount'].agg(total_sales='sum').reset_index()
    new_df['percentage'] = (new_df['total_sales'] / new_df['total_sales'].sum()) * 100
    return 



import matplotlib.pyplot as plt

def create_category_bar_chart(category_data: pd.DataFrame, output_path: str):
    """
    Create a horizontal bar chart of sales by category.
    - Include value labels on bars
    - Use a professional color scheme
    - Save to output_path
    """
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(category_data.index, category_data['total_sales'], color='skyblue')
    plt.xlabel('Total Sales')
    plt.ylabel('Category')
    plt.title('Sales by Category')
    plt.tight_layout()
    plt.savefig(output_path)

def create_regional_pie_chart(region_data: pd.DataFrame, output_path: str):
    """
    Create a pie chart showing sales distribution by region.
    - Include percentages
    - Use distinct colors for each region
    - Save to output_path
    """
    plt.figure(figsize=(10, 6))
    plt.pie(region_data['total_sales'], labels=region_data['region'], autopct='%1.1f%%', startangle=90)
    plt.title('Sales Distribution by Region')
    plt.axis('equal')
    plt.savefig(output_path)

def create_sales_trend_line(daily_data, output_path):
    """
    Create a line chart showing daily sales trend.
    - Include moving average (7-day)
    - Mark weekends differently
    - Add proper axis labels and title
    - Save to output_path
    """
    pass

def create_dashboard(df, output_dir):
    """
    Create a multi-panel dashboard with 4 subplots:
    1. Sales by category (bar)
    2. Sales by region (pie)
    3. Daily trend (line)
    4. Top 10 products (horizontal bar)
    
    Save as a single figure.
    """
    pass



if __name__ == "__main__":
    df: pd.DataFrame = load_data("DataAnalysis/orders.csv")
    clean_df: pd.DataFrame = clean_data(df)
    clean_df: pd.DataFrame = add_time_features(clean_df)
    # explore_data(clean_df)
    # print(clean_df)
    # add_time_features(clean_df).to_csv("clean_orders.csv")
    cat_sales: pd.DataFrame = sales_by_category(clean_df)
    by_region: pd.DataFrame = sales_by_region(clean_df)
    # print(by_region)
    top_products: pd.DataFrame = top_products(clean_df)
    # print(top_products)
    daily_sales_trend = daily_sales_trend(clean_df)
    weekend_vs_weekday = weekend_vs_weekday(clean_df)
    cust_analysis = customer_analysis(clean_df)
    print(cust_analysis)