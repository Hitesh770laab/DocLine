import random
import pandas as pd
from src.simulator import run_simulation
from src.scheduler_lp import run_batch_scheduler

def compare_schedulers():
    print("🔹 Comparing Greedy Simulation vs LP Optimizer...\n")

    # Simulation settings
    num_doctors = 3
    mu = 1/12      # avg 12 min per patient
    lam = 1/5      # one arrival every 5 min (busy hospital)
    sim_time = 480 # 8 hours

    # Run Greedy simulation
    res_greedy = run_simulation(num_doctors=num_doctors, lam=lam, mu=mu, sim_time=sim_time)
    avg_greedy = res_greedy["avg_wait_min"]
    print(f"🧠 Greedy simulation avg wait: {avg_greedy:.2f} min")

    # Prepare LP data (10 patients × 3 doctors × 8 slots)
    patients = [f"P{i}" for i in range(1, 7)]
    doctors = [f"D{j}" for j in range(1, 1+num_doctors)]
    slots = list(range(6))
    service_time = {p: random.randint(6, 15) for p in patients}
    emergency_flags = {p: random.choice([0, 0, 0, 1]) for p in patients}

    # Run LP optimizer
    df_lp = run_batch_scheduler(patients, doctors, slots, service_time, emergency_flags)
    avg_lp_slot = df_lp["slot"].mean() * 15  # 15 min per slot → estimate of avg wait
    print(f"🤖 LP optimizer avg wait (estimated): {avg_lp_slot:.2f} min")

    improvement = ((avg_greedy - avg_lp_slot) / avg_greedy) * 100
    print(f"\n✅ Efficiency gain: {improvement:.1f}% shorter waits (LP vs Greedy)")

    # Save result table
    df_lp.to_csv("outputs/lp_schedule.csv", index=False)
    print("📁 LP schedule saved → outputs/lp_schedule.csv")

if __name__ == "__main__":
    compare_schedulers()
