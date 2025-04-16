import pytest
from app.core.logging import get_logger

def test_get_logger():
    # Act
    logger = get_logger()
    
    # Assert
    assert logger.name == "jira-sonnet"
    assert logger.level == 20  # INFO level
    assert len(logger.handlers) == 1
    assert logger.handlers[0].formatter is not None

def test_logger_caching():
    # Act
    logger1 = get_logger()
    logger2 = get_logger()
    
    # Assert
    assert logger1 is logger2  # Same instance due to lru_cache