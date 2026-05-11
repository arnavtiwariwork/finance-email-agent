import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)
LOG_FILE = "logs/audit_log.json"

def log_entry(record, email, send_status):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "invoice_no": record["invoice_no"],
        "client_name": record["client_name"],
        "client_email": record["client_email"],
        "amount_due": record["amount_due"],
        "days_overdue": int(record["days_overdue"]),
        "stage": record["stage"]["label"],
        "tone_used": email.tone_used,
        "subject": email.subject,
        "send_status": send_status
    }
    logs = []
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def print_email_preview(record, email):
    stage = record["stage"]
    color = {
        "stage_1": Fore.GREEN,
        "stage_2": Fore.YELLOW,
        "stage_3": Fore.LIGHTYELLOW_EX,
        "stage_4": Fore.RED,
        "escalation": Fore.MAGENTA
    }.get(stage["stage_key"], Fore.WHITE)

    print(f"\n{color}{'='*65}")
    print(f"  {stage['label'].upper()}")
    print(f"  Client  : {record['client_name']}")
    print(f"  Invoice : {record['invoice_no']}")
    print(f"  Amount  : Rs.{record['amount_due']:,}")
    print(f"  Overdue : {record['days_overdue']} days")
    print(f"  Tone    : {email.tone_used}")
    print(f"\n  SUBJECT : {email.subject}")
    print(f"\n  BODY:")
    print(f"  {email.body}")
    print(f"{'='*65}{Style.RESET_ALL}")