import pytest
import pandas as pd
from src.project_03.generate_data import generate_brand_data, generate_categories_data, generate_sellers_data


def test_generate_brand_data_structure():
    num_records = 5
    df = generate_brand_data(num_records)

    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame)
    # Check if it has the correct number of rows
    assert len(df) == num_records
    # Check if all expected columns exist
    expected_cols = ['brand_name', 'country', 'created_at']
    assert list(df.columns) == expected_cols

def test_generate_categories_data():
    # Test that Electronics and Fashion are always first
    df = generate_categories_data(5)
    assert df.iloc[0]['category_name'] == 'Electronics'
    assert df.iloc[1]['category_name'] == 'Fashion'
    assert df.iloc[2]['category_name'] == 'Others'
    assert pd.isnull(df.iloc[0]['parent_category_id'])
    assert df.iloc[3]['level'] == 2

def test_generate_sellers_data_structure():
    num_records = 5
    df = generate_sellers_data(num_records)
    # Check if it has the correct number of rows
    assert len(df) == num_records
    # Check if all expected columns exist
    expected_cols = ['seller_name', 'join_date', 'seller_type', 'rating', 'country']
    assert list(df.columns) == expected_cols
    assert df['rating'].dtype == 'float64'
