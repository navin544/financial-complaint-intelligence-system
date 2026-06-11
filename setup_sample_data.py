"""
setup_sample_data.py
Creates a sample complaints.csv for bootstrapping the FAISS index.
Usage: python setup_sample_data.py <data_dir>
"""

import os, sys, csv

SAMPLES = [
    ("CC-001", "Credit Card", "I was charged a $35 late fee even though I paid on time. The bank refuses to reverse it and has been unresponsive to my calls for three weeks."),
    ("CC-002", "Credit Card", "Unauthorized transactions appeared on my credit card statement totaling $2,400. I did not make these purchases and reported fraud immediately but the bank is disputing my claim."),
    ("MT-001", "Mortgage", "My mortgage servicer applied my payment to the wrong account and then reported me 30 days late to the credit bureaus. This is destroying my credit score."),
    ("MT-002", "Mortgage", "I requested a loan modification six months ago. The servicer keeps losing my documents and I keep resubmitting. I am about to go into foreclosure."),
    ("SL-001", "Student Loan", "My student loan servicer incorrectly calculated my income-driven repayment amount. They are charging me $800/month when my income-based calculation should be $0."),
    ("BA-001", "Bank Account", "The bank froze my checking account without notice and will not tell me why. I have direct deposit and cannot access my paycheck. I have bills due."),
    ("BA-002", "Bank Account", "I was charged overdraft fees on transactions that I had sufficient funds for at the time. The bank reordered my transactions to maximize fees."),
    ("DC-001", "Debt Collection", "I am receiving 10+ calls per day from a debt collector about a debt that I already paid two years ago. They are calling my employer and family members."),
    ("DC-002", "Debt Collection", "A collection agency is attempting to collect a debt that is past the statute of limitations. They threatened to sue me if I do not pay immediately."),
    ("CR-001", "Credit Reporting", "Experian is reporting a collection account that belongs to someone else with a similar name. I have disputed this 4 times and they keep verifying it incorrectly."),
    ("CR-002", "Credit Reporting", "A bankruptcy from 2004 is still showing on my credit report. The 10-year reporting period has long passed. The bureaus refuse to remove it."),
    ("PL-001", "Payday Loan", "A payday lender is charging 390% APR and rolling over my loan repeatedly. I have paid 3x the original loan amount and still owe the full principal."),
    ("VL-001", "Vehicle Loan", "The dealer added GAP insurance and an extended warranty to my auto loan without my consent, increasing my loan by $4,000. I only discovered this after signing."),
    ("CC-003", "Credit Card", "My credit limit was reduced from $10,000 to $2,000 without notice right before the holidays. This hurt my credit utilization and my credit score dropped 80 points."),
    ("MT-003", "Mortgage", "My escrow account was miscalculated and I now owe a $3,200 escrow shortage. The servicer wants this paid in one lump sum within 30 days or they will spread it over 12 months with a much higher payment."),
]

def setup(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "complaints.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Complaint ID", "Product", "complaint_text", "Issue", "State"])
        for cid, product, text in SAMPLES:
            writer.writerow([cid, product, text, "", ""])
    print(f"✅  Sample data written: {csv_path}  ({len(SAMPLES)} records)")

if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "backend/data"
    setup(data_dir)
