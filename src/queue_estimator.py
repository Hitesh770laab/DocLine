# src/queue_estimator.py
import math

def factorial(n):
    return math.factorial(int(n))

def erlang_c_prob_wait(lam, mu, c):
    """
    Calculates probability that an arriving patient will need to wait.
    lam: arrival rate (patients per minute)
    mu: service rate (patients served per minute)
    c: number of doctors
    """
    if c <= 0:
        raise ValueError("Number of doctors must be ≥ 1")
    rho = lam / (c * mu)
    if rho >= 1:
        return 1.0  # overloaded system, everyone waits
    crho = c * rho
    sum_terms = sum((crho ** n) / factorial(n) for n in range(c))
    last_term = (crho ** c) / (factorial(c) * (1 - rho))
    denom = sum_terms + last_term
    p0 = 1 / denom
    p_wait = last_term * p0
    return p_wait

def expected_wait_queue(lam, mu, c):
    """
    Computes expected waiting time (Wq) in minutes.
    """
    rho = lam / (c * mu)
    if rho >= 1:
        return float('inf')
    p_wait = erlang_c_prob_wait(lam, mu, c)
    wq = p_wait / (c * mu - lam)
    return wq

def little_law_L(lam, W):
    """Little’s Law: L = λ × W"""
    return lam * W
