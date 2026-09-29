from pathlib import Path
import pandas as pd

PROJ_DIR = Path(__file__).resolve().parent.parent

log_file = PROJ_DIR / "data" /"raw" / "batt.csv"

df = pd.read_csv(log_file,low_memory=False)

print("total rows:", len(df))

print("total columns:", len(df.columns))

print("Available columns:", df.columns.tolist())

print("First 5 rows:")
print(df.head(5))

required_columns = ['Timestamp', 'Voltage_mV', 'Current_mA', 'AverageCurrent_mA', 'stateOfCharge_percent']

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

for col in required_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')


df = df.dropna(subset=required_columns).copy()

df['session_id'] = (df['Timestamp'].diff().lt(0)).cumsum()+1


print("Total sessions:", df['session_id'].nunique())
print("Session IDs:", df['session_id'].unique())
print("Rows per session:")
print(df.groupby('session_id').size())
