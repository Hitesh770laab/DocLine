import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.queue_estimator import erlang_c_prob_wait, expected_wait_queue

def test_erlang_c_basic():
    lam = 1/6.0   # 1 patient every 6 minutes
    mu  = 1/12.0  # 1 doctor serves 1 patient every 12 minutes
    c   = 3       # 3 doctors
    p_wait = erlang_c_prob_wait(lam, mu, c)
    wq = expected_wait_queue(lam, mu, c)
    print("P(wait):", p_wait, "Wq (minutes):", wq)
    assert 0 <= p_wait <= 1
    assert wq >= 0
