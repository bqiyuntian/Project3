

import logging
import logging.handlers
import os
from config import LogConfig

class PlantMonitorLogger:
    
    
    def __init__(self):
        self._setup_logging()
    
    def _setup_logging(self):
        
        
        # Create logs directory if not exists
        os.makedirs(os.path.dirname(LogConfig.LOG_FILE), exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('PlantMonitor')
        self.logger.setLevel(getattr(logging, LogConfig.LOG_LEVEL))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Log format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            LogConfig.LOG_FILE,
            maxBytes=LogConfig.MAX_FILE_SIZE,
            backupCount=LogConfig.BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        if LogConfig.CONSOLE_OUTPUT:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        self.logger.info("Plant Monitor Logger initialized successfully")
    
    def log_sensor_reading(self, sensor_type, value, status="OK"):
 
        self.logger.info(f"SENSOR_READING - {sensor_type}: {value} - Status: {status}")
    
    def log_alert(self, alert_type, message, level="WARNING"):
      
        log_method = getattr(self.logger, level.lower())
        log_method(f"ALERT - {alert_type}: {message}")
    
    def log_prediction(self, prediction_value, confidence):
      
        self.logger.info(f"PREDICTION - Value: {prediction_value:.2f}, Confidence: {confidence:.2f}")
    
    def log_system_status(self, cpu_temp, memory_usage, disk_usage):
        """Log system health metrics"""
        self.logger.debug(f"SYSTEM_STATUS - CPU: {cpu_temp}C, Memory: {memory_usage}%, Disk: {disk_usage}%")

# Global logger instance
logger = PlantMonitorLogger()
