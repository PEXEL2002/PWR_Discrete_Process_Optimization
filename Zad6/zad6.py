from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from RandomNumberGenerator import RandomNumberGenerator

def gen(seed, n, m):
    S = np.zeros((n, m))
    rand = RandomNumberGenerator(seed)
    for i in range(n):
        for j in range(m):
            S[i, j] = rand.nextInt(1, 29)
    return S.T
def calculate_Cmax(Tasks):
    m, n = Tasks.shape
    C = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                C[i, j] = Tasks[i, j]
            elif i == 0:
                C[i, j] = C[i, j - 1] + Tasks[i, j]
            elif j == 0:
                C[i, j] = C[i - 1, j] + Tasks[i, j]
            else:
                C[i, j] = max(C[i - 1, j], C[i, j - 1]) + Tasks[i, j]
    return C[-1, -1]
# ===================================================================
# ================= Wyliczenie permutacji startowej =================
def alg_Johnsona2_for_2machine(tasks):
    l = 0
    m, n = tasks.shape
    k = n - 1
    N = [i for i in range(n)]
    pi = [None for _ in range(n)]
    NewTasks = deepcopy(tasks)
    while len(N) > 0:
        min_value = np.min(tasks)
        indices = np.where(tasks == min_value)
        j_star = indices[1][0]
        if tasks[0, j_star] < tasks[1, j_star]:
            pi[l] = int(j_star)
            l += 1
        else:
            pi[k] = int(j_star)
            k -= 1
        N.remove(j_star)
        tasks[:, j_star] = np.inf
    return pi

def permuteTasks(pi, tasks):
    tasks_toReturn = np.zeros_like(tasks)
    for M in range(tasks.shape[0]):
        for i in range(len(pi)):
            tasks_toReturn[M][i] = tasks[M][pi[i]]
    return tasks_toReturn

def alf_Johnson(tasks):
    m, n = tasks.shape
    if m == 2:
        return alg_Johnsona2_for_2machine(tasks)
    else:
        tasks_transformed = np.zeros((2, n))
        for i in range(n):
            tasks_transformed[0, i] = np.sum(tasks[:m - 1, i])
            tasks_transformed[1, i] = np.sum(tasks[1:m, i])
        pi =  alg_Johnsona2_for_2machine(tasks_transformed)
        return pi
# ===================================================================
# =========================== Tabu Search ===========================
def generate_block_neighbors(permutation, block_size=1):
    permutation = np.array(permutation)
    neighbors = []
    n = len(permutation)
    for i in range(n - block_size):
        for j in range(i + block_size, n - block_size + 1):
            new_perm = permutation.copy()
            temp = new_perm[i:i+block_size].copy()
            new_perm[i:i+block_size] = new_perm[j:j+block_size]
            new_perm[j:j+block_size] = temp
            neighbors.append((new_perm.tolist(), (i, j)))
    return neighbors

def tabuSearch(Tasks, start_permutation=None, stopValue=100, tabu_tenure=7, block_size=1):
    n = Tasks.shape[1]
    if start_permutation is None:
        current_perm = list(range(n))
    else:
        current_perm = start_permutation.copy()
    current_tasks = Tasks[:, current_perm]
    current_cmax = calculate_Cmax(current_tasks)
    best_perm = current_perm.copy()
    best_cmax = current_cmax
    tabu_list = []
    cmax_history = [current_cmax]
    #print(f"Startowa permutacja: {current_perm}, Cmax = {current_cmax}")
    for iteration in range(stopValue):
        neighbors = generate_block_neighbors(current_perm, block_size)
        best_neighbor = None
        best_neighbor_cmax = float('inf')
        best_move = None
        for neighbor_perm, move in neighbors:
            if move not in tabu_list or calculate_Cmax(Tasks[:, neighbor_perm]) < best_cmax:
                cmax = calculate_Cmax(Tasks[:, neighbor_perm])
                if cmax < best_neighbor_cmax:
                    best_neighbor = neighbor_perm
                    best_neighbor_cmax = cmax
                    best_move = move
        if best_neighbor is None:
            break
        current_perm = best_neighbor
        current_cmax = best_neighbor_cmax
        cmax_history.append(current_cmax)
        if current_cmax < best_cmax:
            best_perm = current_perm.copy()
            best_cmax = current_cmax
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
        # print(f"Iteracja {iteration + 1}: permutacja = {current_perm}, Cmax = {current_cmax}")
    return best_perm, best_cmax, cmax_history

# ===================================================================
if __name__ == "__main__":
    tasks = gen(123213, 20, 5)
    start_perm = alf_Johnson(tasks)
    print("Permutacja z algorytmu Johnsona:", start_perm)
    best_perm, best_cmax, cmax_history = tabuSearch(
        Tasks=tasks,
        start_permutation=start_perm,
        stopValue=1500,
        tabu_tenure=7,
        block_size=3
    )
    print("Najlepsza permutacja:", best_perm)
    print("Najlepsze Cmax:", best_cmax)

    # plt.figure(figsize=(10, 5))
    # plt.plot(cmax_history, marker='o')
    # plt.title("Spadek wartości Cmax (Tabu Search od permutacji Johnsona)")
    # plt.xlabel("Iteracja")
    # plt.ylabel("Cmax")
    # plt.grid(True)
    # plt.show()
