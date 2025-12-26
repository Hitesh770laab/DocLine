from src.hybrid_scheduler import run_hybrid_scheduler

print("🚀 Starting DocLine Hybrid Scheduler...\n")
results = run_hybrid_scheduler(num_doctors=3, lam=1/5, mu=1/12, sim_time=480)
print("\n📊 Final Results:")
print(results)
