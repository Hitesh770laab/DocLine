from src.scheduler_lp import run_batch_scheduler

# Example data
patients = [f"P{i}" for i in range(1, 11)]
doctors = ["D1", "D2", "D3"]
slots = list(range(8))  # 8 slots of 15 minutes each

# Random service times (in minutes)
service_time = {p: 10 for p in patients}

# Random emergency flags
emergency_flags = {"P1": 1, "P3": 1, "P7": 1, "P9": 0, "P2": 0, "P4": 0, "P5": 0, "P6": 0, "P8": 0, "P10": 0}

print("🔹 Running DocLine AI scheduler...")
df = run_batch_scheduler(patients, doctors, slots, service_time, emergency_flags)
print("✅ Scheduling complete!\n")
print(df)
