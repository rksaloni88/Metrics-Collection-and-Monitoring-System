import sqlite3
import time
import smtplib
from email.mime.text import MIMEText
import logging

DATABASE_NAME = 'metrics.db'
ALERT_LOG_FILE = 'alerts.log'
CPU_THRESHOLD = 80
CHECK_INTERVAL = 60  # Check every minute
ALERT_DURATION = 300  # Duration to check for threshold (in seconds, 5 minutes)

# Configure logging
logging.basicConfig(
    filename=ALERT_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def log_alert(message):
    logging.info(message)

def send_email_alert(subject, message):
    sender = 'your-email@gmail.com'
    receivers = ['receiver-email@gmail.com']
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, 'your-password')
            server.sendmail(sender, receivers, msg.as_string())
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")

def check_thresholds():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Calculate the time threshold
    time_threshold = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - ALERT_DURATION))
    
    query = "SELECT AVG(cpu) FROM metrics WHERE timestamp > ?"
    cursor.execute(query, (time_threshold,))
    result = cursor.fetchone()
    
    if result and result[0] and result[0] > CPU_THRESHOLD:
        message = f"High CPU Usage Alert: Average CPU usage > {CPU_THRESHOLD}% for the last {ALERT_DURATION / 60} minutes."
        log_alert(message)
        send_email_alert("High CPU Usage Alert", message)
    
    conn.close()

def main():
    while True:
        check_thresholds()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()