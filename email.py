
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import schedule
import time
import threading
from datetime import datetime
from logger import logger
from config import EmailConfig

class EmailNotifier:

    
    def __init__(self):
        self.last_alert_times = {}
        self.alert_cooldown = EmailConfig.ALERT_COOLDOWN
        
        if EmailConfig.ENABLED:
            self._setup_scheduled_reports()
    
    def _setup_scheduled_reports(self):
     
        schedule.every().day.at(EmailConfig.DAILY_REPORT_TIME).do(
            self.send_daily_report
        )
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=self._run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        logger.logger.info("Email scheduler started")
    
    def _run_scheduler(self):
        """Run the schedule in background"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def send_alert(self, alert_type, message, sensor_data=None):
        """Send immediate alert email"""
        if not EmailConfig.ENABLED:
            return False
        
        # Check cooldown period
        current_time = time.time()
        last_alert = self.last_alert_times.get(alert_type, 0)
        
        if current_time - last_alert < self.alert_cooldown:
            logger.logger.debug(f"Alert {alert_type} skipped due to cooldown")
            return False
        
        try:
            subject = f"PLANT MONITOR ALERT: {alert_type}"
            
            body = f"""
            Plant Monitoring System Alert
            
            Alert Type: {alert_type}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Message: {message}
            
            Current Sensor Readings:
            """
            
            if sensor_data:
                for sensor, value in sensor_data.items():
                    if value is not None:
                        body += f"\n{sensor.upper()}: {value}"
            
            body += f"""
            
            Please check your plant monitoring system.
            
            System URL: http://your-raspberry-pi-ip:8080
            """
            
            success = self._send_email(subject, body)
            if success:
                self.last_alert_times[alert_type] = current_time
                logger.logger.info(f"Alert email sent: {alert_type}")
            return success
            
        except Exception as e:
            logger.log_alert("EMAIL_SEND", f"Failed to send alert: {str(e)}")
            return False
    
    def send_daily_report(self):
        """Send daily summary report"""
        if not EmailConfig.ENABLED:
            return
        
        try:
            subject = f"Plant Monitoring Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Generate report content (you can enhance this with actual data)
            body = f"""
            Plant Monitoring System - Daily Report
            
            Date: {datetime.now().strftime('%Y-%m-%d')}
            System Status: Operational
            
            Recent Alerts:
            - Check system logs for detailed alert history
            
            Sensor Status:
            - All sensors reporting normally
            
            Recommendations:
            - Check soil moisture levels
            - Review temperature trends
            - Verify system connectivity
            
            Next Maintenance Check: 7 days
            """
            
            success = self._send_email(subject, body)
            if success:
                logger.logger.info("Daily report email sent successfully")
            return success
            
        except Exception as e:
            logger.log_alert("EMAIL_REPORT", f"Failed to send daily report: {str(e)}")
            return False
    
    def _send_email(self, subject, body):
     
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = EmailConfig.SENDER_EMAIL
            msg['To'] = EmailConfig.RECEIVER_EMAIL
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MimeText(body, 'plain'))
            
            # Create server connection
            server = smtplib.SMTP(EmailConfig.SMTP_SERVER, EmailConfig.SMTP_PORT)
            server.starttls()
            server.login(EmailConfig.SENDER_EMAIL, EmailConfig.SENDER_PASSWORD)
            
            # Send email
            text = msg.as_string()
            server.sendmail(EmailConfig.SENDER_EMAIL, EmailConfig.RECEIVER_EMAIL, text)
            server.quit()
            
            return True
            
        except Exception as e:
            logger.logger.error(f"Email sending failed: {str(e)}")
            return False
    
    def test_connection(self):
      
        if not EmailConfig.ENABLED:
            logger.logger.warning("Email notifications are disabled")
            return False
        
        try:
            subject = "Plant Monitor Test Email"
            body = "This is a test email from your Plant Monitoring System."
            
            success = self._send_email(subject, body)
            if success:
                logger.logger.info("Email test successful")
            return success
            
        except Exception as e:
            logger.log_alert("EMAIL_TEST", f"Email test failed: {str(e)}")
            return False
