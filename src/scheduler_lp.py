# DocLine/src/scheduler_lp.py
import pulp
import pandas as pd

def run_batch_scheduler(patients, doctors, slots, service_time, emergency_flags):
    """
    Linear Programming model for hospital appointment scheduling.
    patients: list of patient IDs
    doctors: list of doctor IDs
    slots: list of time slots (e.g., 9:00, 9:15, ...)
    service_time: dict {patient: minutes required}
    emergency_flags: dict {patient: 1 if emergency else 0}
    """
    model = pulp.LpProblem("DocLine_Scheduler", pulp.LpMinimize)

    # Decision variable: x[p,d,s] = 1 if patient p assigned to doctor d at slot s
    x = pulp.LpVariable.dicts("assign", (patients, doctors, slots), cat="Binary")

    # Objective: minimize weighted waiting time (emergencies have high priority)
    model += pulp.lpSum(
        (1 + 4 * emergency_flags[p]) * (s * 5) * x[p][d][s]
        for p in patients for d in doctors for s in slots
    )

    # Constraints
    # 1. Each patient is assigned to exactly one doctor and slot
    for p in patients:
        model += pulp.lpSum(x[p][d][s] for d in doctors for s in slots) == 1

    # 2. Each doctor can only serve one patient per slot
    for d in doctors:
        for s in slots:
            model += pulp.lpSum(x[p][d][s] for p in patients) <= 1

    # 3. Optional: limit total slots a doctor works
    for d in doctors:
        model += pulp.lpSum(x[p][d][s] for p in patients for s in slots) <= len(slots)

    # Solve
    model.solve(pulp.PULP_CBC_CMD(msg=0, timeLimit=5))


    # Collect results
    assignments = []
    for p in patients:
        for d in doctors:
            for s in slots:
                if pulp.value(x[p][d][s]) == 1:
                    assignments.append({
                        "patient": p,
                        "doctor": d,
                        "slot": s,
                        "emergency": emergency_flags[p]
                    })

    return pd.DataFrame(assignments)
