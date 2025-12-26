# DocLine/data/generate_patients.py
import csv, random, datetime

def make_sample_csv(path="data/patients_sample.csv", n=200):
    """
    Generate a fake dataset of patient arrivals over one day.
    """
    start_time = datetime.datetime(2025, 1, 1, 9, 0)  # 9 AM
    rows = []
    for i in range(n):
        # Random arrival within 8 hours (9AM–5PM)
        delta = random.randint(0, 8 * 60)  # minutes
        arrival = start_time + datetime.timedelta(minutes=delta)
        # Random service time between 5–20 minutes
        service_time = random.randint(5, 20)
        # Random patient type
        typ = random.choices(["walkin", "appointment", "emergency"], weights=[0.6, 0.35, 0.05])[0]
        priority = 1 if typ == "emergency" else 3
        rows.append([arrival.isoformat(), service_time, typ, priority])

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["arrival_time", "service_time", "type", "priority"])
        writer.writerows(rows)

if __name__ == "__main__":
    make_sample_csv()
    print("✅ Created data/patients_sample.csv with 200 sample patients")
