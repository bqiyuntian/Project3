import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime
sensor_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)


with open('moisture_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Moisture_Level"])

    try:
        while True:
            
            moisture_value = GPIO.input(sensor_pin)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          
            writer.writerow([timestamp, moisture_value])
            print(f"Time: {timestamp}, Moisture: {moisture_value}")
           
            time.sleep(1800) 

    except KeyboardInterrupt:
        print("Stopping data collection.")
    finally:
        GPIO.cleanup()
