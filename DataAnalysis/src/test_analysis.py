import pytest
import pandas as pd
from analysis import *

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North']
    })

def test_clean_data_removes_duplicates(sample_data: pd.DataFrame):
    """Test that clean_data removes duplicate rows."""

    # duplicate row to make sure cleaned data removes duplicates
    print(sample_data)
    cleaned_data: pd.DataFrame = clean_data(pd.concat([sample_data, sample_data.iloc[0]]))
    assert cleaned_data.shape[0] == sample_data.shape[0]

def test_sales_by_category_calculation(sample_data: pd.DataFrame):
    """Test that category totals are calculated correctly."""
    sbc: pd.DataFrame = sales_by_category(sample_data)

    # electronics total sales should be 2*10 + 1*25 + 3*10 = 75
    assert sbc[sbc['category'] == 'Electronics']['total_sales'].values[0] == 75.00

def test_top_products_returns_correct_count(sample_data: pd.DataFrame):
    """Test that top_products returns requested number of items."""
    top_1: pd.DataFrame = top_products(sample_data, n=1)
    assert top_1.shape[0] == 1

# Add at least 5 more tests
