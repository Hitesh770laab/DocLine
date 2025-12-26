from src.queue_estimator import expected_wait_queue

# Example setup
lam = 1/6.0   # one patient every 6 minutes
mu  = 1/12.0  # one doctor serves one every 12 minutes
c   = 3       # number of doctors

wait = expected_wait_queue(lam, mu, c)
print("Predicted average waiting time (minutes):", round(wait, 2))
