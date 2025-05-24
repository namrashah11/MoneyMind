
import pandas as pd
from datetime import datetime
from openai_utils import generate_gpt_nudge

def detect_present_bias(df: pd.DataFrame, threshold=100.0):
    insights = []
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()

    for _, row in df.iterrows():
        if row['amount'] > threshold and row['day_of_week'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday']:
            merchant = row.get('merchant_name') or row.get('name') or "a merchant"
            insight = f"You spent ${row['amount']} at {merchant} on a weekday—impulse or intentional?"
            insights.append({
                "date": row['date'].strftime("%Y-%m-%d"),
                "merchant": merchant,
                "amount": row['amount'],
                "bias": "Present Bias",
                "insight": insight,
                "gpt_nudge": generate_gpt_nudge("Present Bias", insight)
            })
    return insights

def detect_mental_accounting(df: pd.DataFrame):
    insights = []
    df['date'] = pd.to_datetime(df['date'])
    large_inflows = df[(df['amount'] > 1000) & (df.get('transaction_type') == 'special')]

    for _, inflow in large_inflows.iterrows():
        same_day_spends = df[(df['date'] == inflow['date']) & (df['amount'] < 0)]
        total_spent = same_day_spends['amount'].sum()

        if abs(total_spent) > inflow['amount'] * 0.5:
            insight = f"You received ${inflow['amount']} and spent over 50% the same day—would you treat your salary this way?"
            insights.append({
                "date": inflow['date'],
                "bias": "Mental Accounting",
                "insight": insight,
                "gpt_nudge": generate_gpt_nudge("Mental Accounting", insight)
            })
    return insights

def generate_insights(df: pd.DataFrame):
    insights = []
    insights += detect_present_bias(df)
    insights += detect_mental_accounting(df)
    return insights
