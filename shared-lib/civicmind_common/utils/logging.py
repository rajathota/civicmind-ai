"""
Shared Utilities for CivicMind Services
=======================================

Common utility functions used across microservices.
"""

import logging
import json
import time
from typing import Dict, Any
from datetime import datetime


def setup_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Setup structured logging for microservices.
    
    Args:
        service_name: Name of the service (e.g., "parking-agent")
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler with structured format
    handler = logging.StreamHandler()
    formatter = StructuredFormatter(service_name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter for microservices"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        super().__init__()
    
    def format(self, record) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "thread": record.thread,
            "process": record.process
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in ('name', 'msg', 'args', 'levelname', 'levelno', 
                          'pathname', 'filename', 'module', 'lineno', 
                          'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process',
                          'getMessage', 'exc_info', 'exc_text', 'stack_info'):
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


def generate_trace_id() -> str:
    """Generate a unique trace ID for request tracking"""
    import uuid
    return str(uuid.uuid4())


def measure_time(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Add timing info to result if it's a dict
        if isinstance(result, dict):
            result['processing_time_ms'] = execution_time
        
        return result
    return wrapper


def sanitize_input(text: str, max_length: int = 2000) -> str:
    """Sanitize user input for processing"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    sanitized = " ".join(text.split())
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized


def format_response_time(time_ms: float) -> str:
    """Format response time for human readability"""
    if time_ms < 1000:
        return f"{time_ms:.0f}ms"
    else:
        return f"{time_ms/1000:.1f}s"
