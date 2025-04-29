from RandomNumberGenerator import RandomNumberGenerator
class Task:
    def __init__(self, duration, weight, deadline):
        self.duration = duration
        self.weight = weight
        self.deadline = deadline
    def __str__(self):
        return f"p={self.duration},\t w={self.weight},\t d={self.deadline}"

def generate_Tasks(n, Z, X=None):
    rand = RandomNumberGenerator(Z)
    durations = [rand.nextInt(1, 28) for _ in range(n)]  # pⱼ ∈ [1,29]
    A = sum(durations)
    if X is None:
        X = A
    weights = [rand.nextInt(1, 8) for _ in range(n)]     # wⱼ ∈ [1,9]
    deadlines = [rand.nextInt(1, X) for _ in range(n)]   # dⱼ ∈ [1,X]
    tasks = [Task(p, w, d) for p, w, d in zip(durations, weights, deadlines)]
    return tasks

def calculate_Cmax(tasks):
    current_time = 0
    total_penalty = 0
    for task in tasks:
        current_time += task.duration
        tardiness = max(0, current_time - task.deadline)
        total_penalty += task.weight * tardiness
    return total_penalty

def print_tasks(tasks):
    for i, task in enumerate(tasks):
        print(f"{task}")

def greedy_by_deadline(tasks):
    indexed_tasks = list(enumerate(tasks))
    indexed_tasks.sort(key=lambda x: x[1].deadline)
    order = [idx for idx, _ in indexed_tasks]
    return order

def brute_force_no_itertools(tasks):
    n = len(tasks)
    min_penalty = float('inf')
    best_order = []

    def permute(current, remaining):
        nonlocal min_penalty, best_order
        if not remaining:
            permuted_tasks = apply_permutation(tasks, current)
            penalty = calculate_Cmax(permuted_tasks)
            if penalty < min_penalty:
                min_penalty = penalty
                best_order = current[:]
            return

        for i in range(len(remaining)):
            permute(current + [remaining[i]], remaining[:i] + remaining[i+1:])

    permute([], list(range(n)))
    return best_order

def apply_permutation(tasks, permutation):
    return [tasks[i] for i in permutation]

def find_optimal_task_order(tasks):
    n = len(tasks)
    dp = [float('inf')] * (1 << n)
    completion_time = [0] * (1 << n)
    parent = [-1] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                completion_time[mask] += tasks[i].duration

    for mask in range(1, 1 << n):
        for k in range(n):
            if mask & (1 << k):
                prev_mask = mask ^ (1 << k)
                tardiness = max(0, completion_time[mask] - tasks[k].deadline)
                penalty = tasks[k].weight * tardiness
                if dp[mask] > dp[prev_mask] + penalty:
                    dp[mask] = dp[prev_mask] + penalty
                    parent[mask] = k

    order = []
    mask = (1 << n) - 1
    while mask:
        k = parent[mask]
        order.append(k)
        mask ^= (1 << k)

    order.reverse()
    return order
def find_optimal_task_order_recursive(tasks):
    n = len(tasks)
    memory = [-1] * (1 << n)
    parent = [-1] * (1 << n)
    def dp(mask):
        if mask == 0:
            return 0
        if memory[mask] != -1:
            return memory[mask]
        total_duration = sum(tasks[j].duration for j in range(n) if mask & (1 << j))
        min_penalty = float('inf')
        best_task = -1
        for j in range(n):
            if mask & (1 << j):
                prev_mask = mask ^ (1 << j)
                tardiness = max(0, total_duration - tasks[j].deadline)
                penalty = tasks[j].weight * tardiness + dp(prev_mask)
                if penalty < min_penalty:
                    min_penalty = penalty
                    best_task = j
        memory[mask] = min_penalty
        parent[mask] = best_task
        return min_penalty
    dp((1 << n) - 1)
    order = []
    mask = (1 << n) - 1
    while mask:
        k = parent[mask]
        order.append(k)
        mask ^= (1 << k)

    order.reverse()
    return order
if __name__ == "__main__":
    n = 10
    Z = 1231233
    tasks = generate_Tasks(n, Z)
    print(f"n={n}, Z={Z}")
    print("Generated Tasks:")
    print_tasks(tasks)
    print(f"Total Penalty in Generated order: {calculate_Cmax(tasks)}")
    print(f"Penalty in Greedy order: {calculate_Cmax(apply_permutation(tasks, greedy_by_deadline(tasks)))}")
    print(f"Optimal Penalty: {calculate_Cmax(apply_permutation(tasks, find_optimal_task_order(tasks)))}")
    print(f"Optimal Penalty Recursive: {calculate_Cmax(apply_permutation(tasks, find_optimal_task_order_recursive(tasks)))}")
    print(f"Brute Force Penalty: {calculate_Cmax(apply_permutation(tasks, brute_force_no_itertools(tasks)))}")

