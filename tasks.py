import time

from datetime import datetime

def send_welcome_email(email: str, username: str):
    time.sleep(3)
    print(f"Welcome email sent to {email} for user {username}")

def send_deletion_notification(email: str, username: str):
    time.sleep(2)
    print(f"Account deletion notification sent to {email} for user {username}")

def log_request_to_file(method: str, url: str, status_code: int):
    with open("request_logs.txt", "a") as f:
        log_line = f"{datetime.now()} | {method} | {url} | {status_code}\n"
        f.write(log_line)