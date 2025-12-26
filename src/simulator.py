# DocLine/src/simulator.py
import simpy
import random
import statistics
from src.queue_estimator import expected_wait_queue

class Doctor:
    def __init__(self, env, doc_id, mu):
        self.env = env
        self.id = doc_id
        self.mu = mu
        self.resource = simpy.Resource(env, capacity=1)
        self.queue_length = 0

    def serve_patient(self, patient_id):
        """Doctor serves the patient for a random service duration."""
        service_time = random.expovariate(self.mu)
        yield self.env.timeout(service_time)
        self.queue_length = max(0, self.queue_length - 1)

class Hospital:
    def __init__(self, env, num_doctors, mu):
        self.env = env
        self.doctors = [Doctor(env, i, mu) for i in range(num_doctors)]

    def choose_best_doctor(self):
        """Greedy: choose doctor with shortest queue."""
        return min(self.doctors, key=lambda d: len(d.resource.queue))

def patient(env, patient_id, hospital, wait_times):
    """Simulates a single patient arriving and being treated."""
    arrival_time = env.now
    chosen_doctor = hospital.choose_best_doctor()

    with chosen_doctor.resource.request() as req:
        yield req
        wait = env.now - arrival_time
        wait_times.append(wait)
        chosen_doctor.queue_length += 1
        yield env.process(chosen_doctor.serve_patient(patient_id))

def run_simulation(num_doctors=3, lam=1/6, mu=1/12, sim_time=480):
    """Run a simulation for 8 hours (480 minutes)."""
    env = simpy.Environment()
    hospital = Hospital(env, num_doctors, mu)
    wait_times = []

    def arrival_process(env, lam, hospital):
        patient_id = 0
        while True:
            inter_arrival = random.expovariate(lam)
            yield env.timeout(inter_arrival)
            patient_id += 1
            env.process(patient(env, patient_id, hospital, wait_times))

    env.process(arrival_process(env, lam, hospital))
    env.run(until=sim_time)

    avg_wait = statistics.mean(wait_times) if wait_times else 0
    p95_wait = statistics.quantiles(wait_times, n=100)[94] if wait_times else 0

    # Approximate utilization per doctor using traffic intensity:
    # utilization = (arrival_rate) / (num_doctors * service_rate)
    # where `lam` is the arrival rate (patients per minute) and `mu` is the
    # service rate (services per minute) per doctor. Express as percent and
    # cap at 100%.
    try:
        util = (lam / (num_doctors * mu)) * 100
    except Exception:
        util = 0
    utilization_percent = round(min(100.0, util), 1)

    return {
        "num_patients": len(wait_times),
        "avg_wait_min": round(avg_wait, 2),
        "p95_wait_min": round(p95_wait, 2),
        "utilization_percent": utilization_percent
    }
