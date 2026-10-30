import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

run1 = pd.read_csv(DATA_DIR / "tickets_v3_run1.csv")
run2 = pd.read_csv(DATA_DIR / "tickets_v3_run2.csv")

print("Run 1 shape:", run1.shape)
print("Run 2 shape:", run2.shape)

if run1.equals(run2):
    print("PASS: Both datasets are identical.")
else:
    print("FAIL: The datasets differ.")

    differences = run1.ne(run2)

    print("Different cells:", differences.sum().sum())