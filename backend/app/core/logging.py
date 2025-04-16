import logging
import sys
from typing import Any
import json
from datetime import datetime
from pydantic import BaseModel
from functools import lru_cache

class CustomFormatter(logging.Formatter):
    """Custom formatter that handles structured data"""
    def format(self, record: logging.LogRecord) -> str:
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        
        # Build base log entry
        log_entry = {
            "timestamp": timestamp,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        # Add extra data if present
        if hasattr(record, "data"):
            if isinstance(record.data, BaseModel):
                log_entry["data"] = record.data.model_dump()
            elif isinstance(record.data, dict):
                log_entry["data"] = record.data
            else:
                log_entry["data"] = str(record.data)
                
        return json.dumps(log_entry, default=str)

def get_logger(name: str = "jira-sonnet") -> logging.Logger:
    """Get configured logger instance"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    
    return logger

def log_request_response(logger: logging.Logger, endpoint: str, request_data: Any = None, response_data: Any = None, error: Exception = None):
    """Helper to log request and response data"""
    log_data = {
        "endpoint": endpoint,
        "request": request_data,
        "response": response_data,
        "error": str(error) if error else None
    }
    
    if error:
        logger.error("API call failed", extra={"data": log_data})
    else:
        logger.info("API call completed", extra={"data": log_data})