

import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_dht
import adafruit_bh1750
from logger import logger
from config import SensorConfig

class SensorManager:
    
    
    def __init__(self):
        self.sensors_available = {
            'moisture': False,
            'temperature': False,
            'humidity': False,
            'light': False
        }
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """Initialize all connected sensors"""
        try:
            # Setup GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(SensorConfig.MOISTURE_PIN, GPIO.IN)
            self.sensors_available['moisture'] = True
            logger.logger.info("Soil moisture sensor initialized")
        except Exception as e:
            logger.log_alert("SENSOR_INIT", f"Moisture sensor failed: {str(e)}")
        
        try:
            # DHT sensor for temperature and humidity
            if SensorConfig.DHT_TYPE == "DHT11":
                self.dht_sensor = adafruit_dht.DHT11(SensorConfig.DHT_PIN)
            else:
                self.dht_sensor = adafruit_dht.DHT22(SensorConfig.DHT_PIN)
            self.sensors_available['temperature'] = True
            self.sensors_available['humidity'] = True
            logger.logger.info("DHT sensor initialized")
        except Exception as e:
            logger.log_alert("SENSOR_INIT", f"DHT sensor failed: {str(e)}")
        
        try:
            # Light sensor via I2C
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.light_sensor = adafruit_bh1750.BH1750(self.i2c)
            self.sensors_available['light'] = True
            logger.logger.info("Light sensor initialized")
        except Exception as e:
            logger.log_alert("SENSOR_INIT", f"Light sensor failed: {str(e)}")
    
    def read_moisture(self):
     
        if not self.sensors_available['moisture']:
            return None
        
        try:
            readings = []
            for _ in range(SensorConfig.CALIBRATION_READINGS):
                raw_value = GPIO.input(SensorConfig.MOISTURE_PIN)
                # Convert to percentage (0=dry, 1=wet)
                moisture_pct = (1 - raw_value) * 100
                readings.append(moisture_pct)
                time.sleep(0.1)
            
            avg_moisture = sum(readings) / len(readings)
            status = "LOW" if avg_moisture < SensorConfig.MOISTURE_LOW else "OK"
            
            logger.log_sensor_reading("MOISTURE", f"{avg_moisture:.1f}%", status)
            return avg_moisture
            
        except Exception as e:
            logger.log_alert("MOISTURE_READ", f"Error reading moisture: {str(e)}")
            return None
    
    def read_temperature_humidity(self):
       
        if not self.sensors_available['temperature']:
            return None, None
        
        try:
            temperature = self.dht_sensor.temperature
            humidity = self.dht_sensor.humidity
            
            if temperature is not None:
                temp_status = "HIGH" if temperature > SensorConfig.TEMPERATURE_HIGH else "OK"
                logger.log_sensor_reading("TEMPERATURE", f"{temperature:.1f}C", temp_status)
            
            if humidity is not None:
                humid_status = "LOW" if humidity < SensorConfig.HUMIDITY_LOW else "OK"
                logger.log_sensor_reading("HUMIDITY", f"{humidity:.1f}%", humid_status)
            
            return temperature, humidity
            
        except Exception as e:
            logger.log_alert("DHT_READ", f"Error reading DHT sensor: {str(e)}")
            return None, None
    
    def read_light_intensity(self):
     
        if not self.sensors_available['light']:
            return None
        
        try:
            lux = self.light_sensor.lux
            logger.log_sensor_reading("LIGHT", f"{lux:.1f} lux", "OK")
            return lux
        except Exception as e:
            logger.log_alert("LIGHT_READ", f"Error reading light sensor: {str(e)}")
            return None
    
    def read_all_sensors(self):
     
        sensor_data = {
            'timestamp': time.time(),
            'moisture': self.read_moisture(),
            'temperature': self.read_temperature_humidity()[0],
            'humidity': self.read_temperature_humidity()[1],
            'light': self.read_light_intensity()
        }
        return sensor_data
    
    def cleanup(self):
       
        GPIO.cleanup()
        logger.logger.info("Sensor manager cleanup completed")
