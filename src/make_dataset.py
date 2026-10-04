from pathlib import Path
import pandas as pd

SRC = Path(r"D:\loandata\loan-default-prediction\Accepted")
OUT = Path("data/raw/lending_club_subset.csv.gz")

# Variables known at application time, plus the outcome (loan_status)
# and issue date (for out-of-time validation later).
# grade, sub_grade and int_rate are kept for analysis only;
# we will exclude them from the model to avoid leakage.
WANTED = [
    "id", "loan_status", "issue_d",
    "loan_amnt", "term", "int_rate", "installment", "grade", "sub_grade",
    "emp_length", "home_ownership", "annual_inc", "verification_status",
    "purpose", "addr_state", "dti", "application_type", "initial_list_status",
    "delinq_2yrs", "earliest_cr_line", "fico_range_low", "fico_range_high",
    "inq_last_6mths", "mths_since_last_delinq", "mths_since_last_record",
    "open_acc", "pub_rec", "revol_bal", "revol_util", "total_acc",
    "mort_acc", "pub_rec_bankruptcies", "acc_open_past_24mths",
    "avg_cur_bal", "bc_util", "tot_cur_bal", "total_rev_hi_lim",
]

parts = sorted(SRC.glob("accepted_part_*.csv.gz"))
print(f"Found {len(parts)} files")

frames = []
for f in parts:
    df = pd.read_csv(f, usecols=lambda c: c in WANTED, low_memory=False)
    frames.append(df)
    print(f"{f.name}: {len(df):,} rows")

data = pd.concat(frames, ignore_index=True)

# The original file ends with a few footer rows that have no loan status
data = data.dropna(subset=["loan_status"])

missing = [c for c in WANTED if c not in data.columns]
print("Missing columns:", missing if missing else "none")

OUT.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(OUT, index=False)
print(f"Saved {OUT}: {data.shape[0]:,} rows, {data.shape[1]} columns")