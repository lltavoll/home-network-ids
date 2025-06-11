# Home Network Threat Detection & Alert System
# Technologies: Python, Windows Firewall Logs, Email Alerts, AbuseIPDB

import re
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- Configuration ---
LOG_FILE_PATH = 'C:/Windows/System32/logfiles/firewall/pfirewall.log'
ALERT_THRESHOLD = 5
EMAIL_SENDER = 'youremail@example.com'
EMAIL_RECEIVER = 'youralert@example.com'
EMAIL_PASSWORD = 'yourpassword'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# --- Read log and find suspicious IPs ---
def parse_firewall_logs():
    suspicious_ips = {}
    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split(' ')
            if len(parts) >= 5:
                action = parts[0]
                protocol = parts[1]
                src_ip = parts[2]
                dst_ip = parts[3]
                
                # Flag dropped connections from unknown IPs
                if action == 'DROP':
                    suspicious_ips[src_ip] = suspicious_ips.get(src_ip, 0) + 1
    return suspicious_ips

# --- Send Email Alert ---
def send_alert(ip, count):
    msg = EmailMessage()
    msg['Subject'] = f'ALERT: Suspicious activity from IP {ip}'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f"Detected {count} suspicious attempts from IP {ip} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# --- Main Logic ---
def monitor():
    alerts_sent = 0
    ip_hits = parse_firewall_logs()
    for ip, count in ip_hits.items():
        if count >= ALERT_THRESHOLD:
            send_alert(ip, count)
            alerts_sent += 1
    print(f"{alerts_sent} alerts sent.")

if __name__ == '__main__':
    monitor()
