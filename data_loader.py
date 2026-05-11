import pandas as pd
from datetime import date
from config import ESCALATION_STAGES

def load_invoices(filepath="data/invoices.csv"):
    df = pd.read_csv(filepath)
    df["due_date"] = pd.to_datetime(df["due_date"])
    df["days_overdue"] = (
        pd.Timestamp(date.today()) - df["due_date"]
    ).dt.days
    df = df[df["days_overdue"] > 0]
    return df

def get_escalation_stage(days_overdue):
    for stage_key, stage in ESCALATION_STAGES.items():
        if stage["min"] <= days_overdue <= stage["max"]:
            return {"stage_key": stage_key, **stage}
    return {"stage_key": "escalation", **ESCALATION_STAGES["escalation"]}

def prepare_records(filepath="data/invoices.csv"):
    df = load_invoices(filepath)
    records = []
    for _, row in df.iterrows():
        stage = get_escalation_stage(int(row["days_overdue"]))
        record = row.to_dict()
        record["stage"] = stage
        records.append(record)
    return records