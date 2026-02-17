"""
Logger
Centralized logging for the framework
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger


class Logger:
    """Centralized logger for PAD Framework"""
    
    def __init__(self, config):
        """
        Initialize logger
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.log_path = config.get_path("logs")
        self.log_entries = []
        
        # Remove default handler
        logger.remove()
        
        # Add console handler if enabled
        if config.get("logging.console_output", True):
            logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
                level=config.get("logging.level", "INFO"),
                colorize=True
            )
        
        # Add file handler if enabled
        if config.get("logging.file_output", True):
            log_file = self.log_path / "pad_framework_{time:YYYY-MM-DD}.log"
            logger.add(
                str(log_file),
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
                level=config.get("logging.level", "INFO"),
                rotation=config.get("logging.max_file_size", "10 MB"),
                retention=config.get("logging.backup_count", 5),
                compression="zip"
            )
        
        self.logger = logger
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(message, **kwargs)
        self._store_entry("DEBUG", message)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(message, **kwargs)
        self._store_entry("INFO", message)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(message, **kwargs)
        self._store_entry("WARNING", message)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message"""
        self.logger.error(message, **kwargs)
        self._store_entry("ERROR", message)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message"""
        self.logger.critical(message, **kwargs)
        self._store_entry("CRITICAL", message)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log exception message"""
        self.logger.exception(message, **kwargs)
        self._store_entry("EXCEPTION", message)
    
    def _store_entry(self, level: str, message: str) -> None:
        """
        Store log entry for retrieval
        
        Args:
            level: Log level
            message: Log message
        """
        entry = {
            "timestamp": datetime.now(),
            "level": level,
            "message": message
        }
        self.log_entries.append(entry)
        
        # Keep only last 1000 entries in memory
        if len(self.log_entries) > 1000:
            self.log_entries = self.log_entries[-1000:]
    
    def get_logs(
        self,
        flow_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve logs with filters
        
        Args:
            flow_name: Optional flow name filter
            start_time: Optional start time filter
            end_time: Optional end time filter
            level: Optional log level filter
            
        Returns:
            List of log entries
        """
        filtered_logs = self.log_entries.copy()
        
        if start_time:
            filtered_logs = [
                log for log in filtered_logs
                if log["timestamp"] >= start_time
            ]
        
        if end_time:
            filtered_logs = [
                log for log in filtered_logs
                if log["timestamp"] <= end_time
            ]
        
        if level:
            filtered_logs = [
                log for log in filtered_logs
                if log["level"] == level.upper()
            ]
        
        if flow_name:
            filtered_logs = [
                log for log in filtered_logs
                if flow_name.lower() in log["message"].lower()
            ]
        
        return filtered_logs
