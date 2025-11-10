"""
Utility functions for ETL pipeline
"""

import logging
import os
from datetime import datetime
from typing import Optional

# Setup logging
def setup_logging(log_file: Optional[str] = None):
    """Setup logging configuration"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return logging.getLogger(__name__)


def validate_dataframe(df, required_columns: list, logger: Optional[logging.Logger] = None):
    """Validate DataFrame has required columns"""
    if logger is None:
        logger = logging.getLogger(__name__)
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        error_msg = f"Missing required columns: {missing_cols}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"DataFrame validation passed. Shape: {df.shape}")
    return True


def log_execution_time(func):
    """Decorator to log execution time"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        start_time = datetime.now()
        logger.info(f"Starting {func.__name__}...")
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            logger.info(f"Completed {func.__name__} in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    
    return wrapper

