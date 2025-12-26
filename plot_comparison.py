import matplotlib.pyplot as plt

greedy = 6.75
lp = 10.35

plt.bar(["Greedy", "LP Optimizer"], [greedy, lp], color=["skyblue", "lightgreen"])
plt.title("DocLine – Scheduler Efficiency Comparison")
plt.ylabel("Average Waiting Time (minutes)")
plt.tight_layout()
plt.show()
