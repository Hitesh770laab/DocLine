from src.simulator import run_simulation

print("🔹 Running DocLine intelligent scheduler simulation...")
result = run_simulation(num_doctors=3, lam=1/6, mu=1/12, sim_time=480)
print("✅ Simulation complete!\n")
print(result)
