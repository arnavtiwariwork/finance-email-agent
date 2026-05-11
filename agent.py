from data_loader import prepare_records
from email_generator import generate_email
from utils import log_entry, print_email_preview
from config import DRY_RUN

def run_agent():
    print('\n' + '='*65)
    print('   FINANCE CREDIT FOLLOW-UP EMAIL AGENT')
    print('='*65)
    print('   MODE: DRY RUN - no real emails sent' if DRY_RUN else '   MODE: LIVE')
    print('='*65 + '\n')

    records = prepare_records()

    if not records:
        print('No overdue invoices found!')
        return

    print(f'Found {len(records)} overdue invoice(s).\n')

    escalated = []
    processed = 0
    errors = 0

    for record in records:
        try:
            print(f'Processing {record["invoice_no"]} - {record["client_name"]}...')
            email = generate_email(record)

            if record['stage']['stage_key'] == 'escalation':
                escalated.append(record)
                print_email_preview(record, email)
                log_entry(record, email, 'ESCALATED_NO_EMAIL')
            else:
                print_email_preview(record, email)
                status = 'DRY_RUN' if DRY_RUN else 'SENT'
                if DRY_RUN:
                    print(f'   [DRY RUN] Would send to: {record["client_email"]}')
                log_entry(record, email, status)
                processed += 1

        except Exception as e:
            print(f'   ERROR on {record["invoice_no"]}: {e}')
            errors += 1

    print('\n' + '='*65)
    print('   SUMMARY')
    print('='*65)
    print(f'   Processed : {processed}')
    print(f'   Escalated : {len(escalated)}')
    print(f'   Errors    : {errors}')
    print(f'   Log       : logs/audit_log.json')
    print('='*65 + '\n')
