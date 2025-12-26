# DocLine/plot_wait_times.py
import matplotlib.pyplot as plt
from src.data_utils import load_patients, predict_wait_over_time

# Step 1: Load the patient data
print("🔹 Loading data...")
df = load_patients("data/patients_sample.csv")

# Step 2: Predict waiting times per 15-minute window
print("🔹 Calculating predictions...")
result = predict_wait_over_time(df, mu=1/12, c=3, bin_minutes=15)

# Step 3: Plot the results
plt.figure(figsize=(10,5))
plt.plot(result["start_time"], result["predicted_wait_min"], marker="o", linestyle="-")
plt.title("DocLine – Predicted Waiting Time Throughout the Day")
plt.xlabel("Time of Day")
plt.ylabel("Predicted Wait (minutes)")
plt.grid(True)
plt.tight_layout()

# Step 4: Save and show
plt.savefig("outputs/predicted_wait_chart.png")
plt.show()
print("✅ Chart saved to outputs/predicted_wait_chart.png")
