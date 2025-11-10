"""
Data quality checks for ETL pipeline
"""

import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def check_data_quality(df: pd.DataFrame, checks: List[str] = None) -> Dict[str, any]:
    """
    Perform data quality checks on DataFrame
    
    Args:
        df: DataFrame to check
        checks: List of checks to perform (default: all checks)
    
    Returns:
        Dictionary with quality check results
    """
    if checks is None:
        checks = ['nulls', 'duplicates', 'ranges', 'types']
    
    results = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'checks': {}
    }
    
    # Check for nulls
    if 'nulls' in checks:
        null_counts = df.isnull().sum()
        results['checks']['nulls'] = {
            'columns_with_nulls': null_counts[null_counts > 0].to_dict(),
            'total_nulls': null_counts.sum(),
            'null_percentage': (null_counts.sum() / len(df) * 100).round(2)
        }
        logger.info(f"Null check: {results['checks']['nulls']['total_nulls']} nulls found")
    
    # Check for duplicates
    if 'duplicates' in checks:
        duplicate_count = df.duplicated().sum()
        results['checks']['duplicates'] = {
            'count': duplicate_count,
            'percentage': (duplicate_count / len(df) * 100).round(2) if len(df) > 0 else 0
        }
        logger.info(f"Duplicate check: {duplicate_count} duplicates found")
    
    # Check for value ranges
    if 'ranges' in checks:
        range_checks = {}
        if 'amount' in df.columns:
            range_checks['amount'] = {
                'min': float(df['amount'].min()),
                'max': float(df['amount'].max()),
                'mean': float(df['amount'].mean()),
                'negative_count': int((df['amount'] < 0).sum())
            }
        if 'event_time' in df.columns:
            range_checks['event_time'] = {
                'min': str(df['event_time'].min()),
                'max': str(df['event_time'].max()),
                'future_dates': int((pd.to_datetime(df['event_time']) > pd.Timestamp.now()).sum())
            }
        results['checks']['ranges'] = range_checks
        logger.info(f"Range check completed for {len(range_checks)} columns")
    
    # Check for data types
    if 'types' in checks:
        results['checks']['types'] = df.dtypes.to_dict()
        logger.info(f"Type check: {len(df.dtypes)} columns checked")
    
    return results


def validate_transaction_data(df: pd.DataFrame) -> bool:
    """
    Validate transaction data meets quality standards
    
    Args:
        df: DataFrame to validate
    
    Returns:
        True if validation passes, raises exception otherwise
    """
    logger.info("Starting transaction data validation...")
    
    # Required columns
    required_columns = ['transaction_id', 'user_id', 'amount', 'event_time']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check for nulls in required columns
    null_required = df[required_columns].isnull().sum()
    if null_required.sum() > 0:
        logger.warning(f"Null values in required columns: {null_required[null_required > 0].to_dict()}")
    
    # Check for negative amounts
    if 'amount' in df.columns:
        negative_amounts = (df['amount'] < 0).sum()
        if negative_amounts > 0:
            logger.warning(f"Found {negative_amounts} transactions with negative amounts")
    
    # Check for future dates
    if 'event_time' in df.columns:
        future_dates = (pd.to_datetime(df['event_time']) > pd.Timestamp.now()).sum()
        if future_dates > 0:
            logger.warning(f"Found {future_dates} transactions with future dates")
    
    # Check for duplicates
    duplicate_count = df['transaction_id'].duplicated().sum()
    if duplicate_count > 0:
        logger.warning(f"Found {duplicate_count} duplicate transaction IDs")
    
    logger.info("Transaction data validation completed")
    return True

