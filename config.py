
import os
from datetime import datetime

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sensor Configuration
class SensorConfig:
    # GPIO Pins
    MOISTURE_PIN = 17
    DHT_PIN = 4
    LIGHT_PIN = 27
    
    # Sensor Types
    DHT_TYPE = "DHT22"  # DHT11 or DHT22
    MOISTURE_TYPE = "FC-28"
    
    # Reading intervals (seconds)
    COLLECTION_INTERVAL = 300  # 5 minutes
    CALIBRATION_READINGS = 5
    
    # Thresholds for alerts
    MOISTURE_LOW = 30
    MOISTURE_HIGH = 80
    TEMPERATURE_HIGH = 35
    HUMIDITY_LOW = 40

# Email Configuration
class EmailConfig:
    ENABLED = True
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 465
    
    # Email credentials
    SENDER_EMAIL = "17605229265@163.com"
    SENDER_PASSWORD = "qw1357erty"
    RECEIVER_EMAIL = "alerts@example.com"
    
    # Alert settings
    ALERT_COOLDOWN = 3600  # 1 hour between same alerts
    DAILY_REPORT_TIME = "08:00"  # Daily report time

# Data Configuration
class DataConfig:
    RAW_DATA_FILE = os.path.join(BASE_DIR, "data/sensor_data.csv")
    MODEL_FILE = os.path.join(BASE_DIR, "models/predictor_model.h5")
    
    # Data retention
    MAX_DATA_DAYS = 30
    BACKUP_ENABLED = True
    
    # Prediction settings
    LOOKBACK_HOURS = 24
    PREDICT_HOURS = 6

# Logging Configuration
class LogConfig:
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = os.path.join(BASE_DIR, f"logs/monitor_{datetime.now().strftime('%Y%m')}.log")
    CONSOLE_OUTPUT = True
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5

# System Configuration
class SystemConfig:
    CPU_TEMP_WARNING = 70
    MEMORY_WARNING = 85
    CHECK_INTERVAL = 300  # 5 minutes
