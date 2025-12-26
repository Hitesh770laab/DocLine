import matplotlib.pyplot as plt

greedy = 8.45
hybrid = 6.62
lp_refined = 4.80

plt.bar(["Greedy", "Hybrid", "LP Refined"], [greedy, hybrid, lp_refined],
        color=["skyblue", "lightgreen", "orange"])
plt.ylabel("Average Wait Time (min)")
plt.title("DocLine – Hybrid Scheduling Efficiency")
plt.tight_layout()
plt.show()
print("✅ Chart displayed comparing scheduling methods.")