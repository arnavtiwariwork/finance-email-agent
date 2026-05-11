import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = 'llama3-8b-8192'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'finance@yourcompany.com')

DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

ESCALATION_STAGES = {
    'stage_1': {'min': 1,  'max': 7,  'tone': 'Warm & Friendly',  'label': '1st Follow-Up'},
    'stage_2': {'min': 8,  'max': 14, 'tone': 'Polite but Firm',  'label': '2nd Follow-Up'},
    'stage_3': {'min': 15, 'max': 21, 'tone': 'Formal & Serious', 'label': '3rd Follow-Up'},
    'stage_4': {'min': 22, 'max': 30, 'tone': 'Stern & Urgent',   'label': '4th Follow-Up'},
    'escalation': {'min': 31, 'max': 9999, 'tone': 'Escalation',  'label': 'Escalation Flag'},
}
