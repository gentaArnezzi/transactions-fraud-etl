"""
Unit tests for transform.py
"""

import pytest
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.data_quality import check_data_quality, validate_transaction_data


def test_check_data_quality():
    """Test data quality checks"""
    # Create sample DataFrame
    df = pd.DataFrame({
        'transaction_id': ['1', '2', '3'],
        'user_id': [100, 200, 300],
        'amount': [1000, 2000, 3000],
        'event_time': pd.date_range('2024-01-01', periods=3)
    })
    
    # Run quality checks
    results = check_data_quality(df)
    
    # Assertions
    assert results['total_rows'] == 3
    assert results['total_columns'] == 4
    assert 'checks' in results


def test_validate_transaction_data():
    """Test transaction data validation"""
    # Create valid DataFrame
    df = pd.DataFrame({
        'transaction_id': ['1', '2', '3'],
        'user_id': [100, 200, 300],
        'amount': [1000, 2000, 3000],
        'event_time': pd.date_range('2024-01-01', periods=3)
    })
    
    # Should not raise exception
    assert validate_transaction_data(df) == True


def test_validate_transaction_data_missing_columns():
    """Test validation with missing columns"""
    # Create DataFrame with missing columns
    df = pd.DataFrame({
        'transaction_id': ['1', '2', '3'],
        'amount': [1000, 2000, 3000]
    })
    
    # Should raise ValueError
    with pytest.raises(ValueError):
        validate_transaction_data(df)


if __name__ == "__main__":
    pytest.main([__file__])

