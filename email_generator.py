import json
from groq import Groq
from config import GROQ_API_KEY
from pydantic import BaseModel

client = Groq(api_key=GROQ_API_KEY)

class GeneratedEmail(BaseModel):
    subject: str
    body: str
    tone_used: str
    stage_label: str

def generate_email(record):
    stage = record['stage']

    if stage['stage_key'] == 'escalation':
        return GeneratedEmail(
            subject=f"ESCALATION: Invoice {record['invoice_no']} - Assign to Finance Manager",
            body=f"Invoice {record['invoice_no']} for {record['client_name']} (Rs.{record['amount_due']}) is {record['days_overdue']} days overdue. Flagged for legal/finance review. NO automated email sent.",
            tone_used='Escalation',
            stage_label='Escalation Flag'
        )

    prompt = f'''You are a professional finance collections agent for an Indian company.
Generate a follow-up payment reminder email.

INVOICE DETAILS:
- Client Name: {record['client_name']}
- Invoice Number: {record['invoice_no']}
- Amount Due: Rs.{record['amount_due']}
- Due Date: {record['due_date']}
- Days Overdue: {record['days_overdue']} days
- Payment Link: {record['payment_link']}
- Follow-up number: {int(record['follow_up_count']) + 1}

REQUIRED TONE: {stage['tone']}
STAGE: {stage['label']}

RULES:
1. Address client by first name
2. Mention invoice number, amount, due date
3. Include payment link
4. Keep under 150 words
5. Match tone exactly

Respond ONLY with valid JSON, no markdown:
{{"subject": "subject here", "body": "body here"}}'''

    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.7,
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace('`json', '').replace('`', '').strip()
    parsed = json.loads(raw)

    return GeneratedEmail(
        subject=parsed['subject'],
        body=parsed['body'],
        tone_used=stage['tone'],
        stage_label=stage['label']
    )
