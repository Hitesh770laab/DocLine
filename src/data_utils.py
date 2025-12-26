# DocLine/src/data_utils.py
import pandas as pd
from datetime import datetime, timedelta
from src.queue_estimator import expected_wait_queue

def load_patients(csv_path="data/patients_sample.csv"):
    """Read the CSV and convert arrival_time column to datetime."""
    df = pd.read_csv(csv_path)
    df["arrival_time"] = pd.to_datetime(df["arrival_time"])
    return df

def compute_lambda_timeseries(df, bin_minutes=15):
    """
    Compute λ(t): number of arrivals per minute in each time window.
    Returns a DataFrame with columns: [start_time, lambda_per_minute, count]
    """
    start = df["arrival_time"].min().floor("T")
    end   = df["arrival_time"].max().ceil("T")
    bins = pd.date_range(start, end + pd.Timedelta(minutes=bin_minutes), freq=f"{bin_minutes}min")
    counts, _ = pd.cut(df["arrival_time"], bins=bins, right=False, retbins=True)
    grouped = df.groupby(counts).size().reset_index(name="count")
    grouped["start_time"] = grouped["arrival_time"].apply(lambda x: x.left)
    grouped["lambda_per_min"] = grouped["count"] / bin_minutes
    return grouped[["start_time", "lambda_per_min", "count"]]

def predict_wait_over_time(df, mu=1/12, c=3, bin_minutes=15):
    """
    Uses queue_estimator to compute expected wait for each time window.
    mu: service rate per doctor per minute (1/12 → 12 min per patient)
    c:  number of doctors
    """
    lambda_df = compute_lambda_timeseries(df, bin_minutes)
    lambda_df["predicted_wait_min"] = lambda_df["lambda_per_min"].apply(
        lambda lam: expected_wait_queue(lam, mu, c)
    )
    return lambda_df
