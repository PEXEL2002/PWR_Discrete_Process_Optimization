import random

from RandomNumberGenerator import RandomNumberGenerator
from collections import defaultdict
import time
import matplotlib.pyplot as plt

class Operation:
    def __init__(self, job_id, index, duration, machine):
        self.job_id = job_id
        self.index = index
        self.duration = duration
        self.machine = machine
        self.start = None
        self.end = None

    def __repr__(self):
        return f"J{self.job_id}-O{self.index}(M{self.machine}, t={self.duration})"

def generate_job_shop_tasks(n, m, Z=None):
    if Z is None:
        Z = random.randint(1, 10**9)
    rng = RandomNumberGenerator(Z)
    tasks = []
    for j in range(n):
        oj = rng.nextInt(1, int(m * 1.2))
        job = []
        for k in range(oj):
            time = rng.nextInt(1, 28)
            machine = rng.nextInt(0, m - 1)
            job.append(Operation(j, k, time, machine))
        tasks.append(job)
    return tasks

def flatten(tasks):
    operations = []
    for job in tasks:
        operations.extend(job)
    return operations

def is_valid(schedule):
    last_op_index = {}
    for op in schedule:
        idx = last_op_index.get(op.job_id, -1)
        if op.index == idx + 1:
            last_op_index[op.job_id] = op.index
        elif op.index <= idx:
            continue  # repeated
        else:
            return False  # invalid ordering
    return True

def evaluate_Cmax(ordering):
    machine_times = defaultdict(int)
    job_times = defaultdict(int)
    op_end = {}

    for op in ordering:
        prev_op_end = op_end.get((op.job_id, op.index - 1), 0)
        start = max(machine_times[op.machine], prev_op_end)
        end = start + op.duration
        machine_times[op.machine] = end
        op_end[(op.job_id, op.index)] = end
        job_times[op.job_id] = max(job_times[op.job_id], end)

        # zapamiętaj do wykresu
        op.start = start
        op.end = end

    return max(job_times.values())

def INSA(tasks):
    # Krok 1: policz sumę czasów dla każdego zadania
    task_weights = []
    for task in tasks:
        total_duration = sum(op.duration for op in task)
        task_weights.append((total_duration, task))

    # Krok 2: posortuj zadania malejąco
    task_weights.sort(reverse=True, key=lambda x: x[0])

    schedule = []

    # Krok 3: po kolei dodawaj zadania
    for weight, task in task_weights:
        for op in task:  # dodaj operacje w kolejności Op0, Op1, Op2...
            best_cmax = float('inf')
            best_schedule = None

            for pos in range(len(schedule) + 1):
                candidate = schedule[:pos] + [op] + schedule[pos:]
                if not is_valid(candidate):
                    continue
                cmax = evaluate_Cmax(candidate)
                if cmax < best_cmax:
                    best_cmax = cmax
                    best_schedule = candidate

            if best_schedule is not None:
                schedule = best_schedule
            else:
                print(f"⚠️ Nie znaleziono legalnej pozycji dla {op}, dodaję na koniec.")
                schedule.append(op)

    cmax = evaluate_Cmax(schedule)
    return schedule, cmax



def plot_schedule(schedule):
    import matplotlib.pyplot as plt

    machine_ops = defaultdict(list)
    for op in schedule:
        machine_ops[op.machine].append(op)

    fig, ax = plt.subplots(figsize=(10, 4))

    colors = plt.cm.tab20.colors
    yticks = []
    ylabels = []

    for machine, ops in machine_ops.items():
        for op in ops:
            ax.barh(
                y=machine,
                width=op.duration,
                left=op.start,
                height=0.8,
                color=colors[op.job_id % len(colors)],
                edgecolor='black'
            )
            ax.text(op.start + op.duration / 2, machine, f"J{op.job_id}-O{op.index}", ha='center', va='center', fontsize=8)

        yticks.append(machine)
        ylabels.append(f"M{machine}")

    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.set_xlabel("Czas")
    ax.set_title("Wykres Gantta – Harmonogram operacji (INSA)")
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# Główna część
if __name__ == "__main__":
    n = 5   # liczba zadań
    m = 3   # liczba maszyn
    Z = 42  # ziarno RNG

    tasks = generate_job_shop_tasks(n, m)

    print("Wygenerowane zadania:")
    for i, job in enumerate(tasks):
        print(f"Zadanie {i+1}: {job}")

    schedule, cmax = INSA(tasks)

    print("\nNajlepszy harmonogram:")
    for op in schedule:
        print(op)

    print(f"\nCmax: {cmax}")

    # Generuj wykres
    plot_schedule(schedule)