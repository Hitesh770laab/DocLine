from src.data_utils import load_patients, predict_wait_over_time

df = load_patients("data/patients_sample.csv")
result = predict_wait_over_time(df, mu=1/12, c=3, bin_minutes=15)

print(result.head(10))

