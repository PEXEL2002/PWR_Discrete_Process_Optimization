from RandomNumberGenerator import RandomNumberGenerator
import numpy as np
from copy import copy, deepcopy
def gen(seed,n,m):
    """
    Generates a random number using the RandomNumberGenerator class.
    :param seed:
    :param n: - ilość zadań
    :param m: - ilośc maszyn
    :return: wygenerowana macierz z czasem działania
    """
    S = np.zeros((n, m))
    rand = RandomNumberGenerator(seed)
    for i in range(n):
        for j in range(m):
            S[i, j] = rand.nextInt(1, 29)
    return S.T
def calculate_Cmax(Tasks, SorC=None):
    """
    Calculates the end and start
    :param Tasks: matrix of task
    :param SorC: 0 - start, 1 - end
    :return: matrix of end times, start times
    """
    C = np.zeros(Tasks.shape)
    S = np.zeros(Tasks.shape)
    for i in range(Tasks.shape[0]):
        for j in range(Tasks.shape[1]):
            if i == 0 and j == 0:
                C[i, j] = Tasks[i, j]
                S[i, j] = 0
            elif i == 0:
                C[i, j] = C[i, j - 1] + Tasks[i, j]
                S[i, j] = C[i, j] - Tasks[i, j]
            elif j == 0:
                C[i, j] = C[i - 1, j] + Tasks[i, j]
                S[i, j] = C[i, j] - Tasks[i, j]
            else:
                C[i, j] = max(C[i - 1, j], C[i, j - 1]) + Tasks[i, j]
                S[i, j] = C[i, j] - Tasks[i, j]
    if SorC is None:
        return S, C
    if SorC == 0:
        return S
    if SorC == 1:
        return C


def alg_Johnsona2_for_2machine(tasks, ToMultipleMachine=False):
    """
    Johnson's algorithm for two machines
    :param tasks: matrix of task times
    :return: full permutation of tasks
    """
    l = 0
    m, n = tasks.shape
    k = n - 1
    N = [i for i in range(n)]  # List of tasks
    pi = [None for _ in range(n)]  # Permutation list initialized with None
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
    if ToMultipleMachine:
        return pi
    else:
        return permuteTasks(pi, NewTasks)

def permuteTasks(pi, tasks):
    tasks_toReturn = np.zeros_like(tasks)
    for M in range(tasks.shape[0]):
        for i in range(len(pi)):
            tasks_toReturn[M][i] = tasks[M][pi[i]]
    return tasks_toReturn

def alf_Johnson(tasks):
    """
    Johnson's algorithm for more than two machines
    :param tasks: matrix of task times
    :return: full permutation of tasks
    """
    m, n = tasks.shape
    if m == 2:
        return alg_Johnsona2_for_2machine(tasks)
    else:
        tasks_transformed = np.zeros((2, n))
        for i in range(n):
            tasks_transformed[0, i] = np.sum(tasks[:m - 1, i])
            tasks_transformed[1, i] = np.sum(tasks[1:m, i])
        pi =  alg_Johnsona2_for_2machine(tasks_transformed, True)
        return permuteTasks(pi, tasks)

def bruteForce(Tasks):
    """
    bruteForce algorithm
    :param Tasks:
    :return:
    """
    min_Cmax = float('inf')
    best_perm = None
    task_order = list(range(Tasks.shape[1]))
    def generate_permutations(arr, level=0):
        nonlocal min_Cmax, best_perm
        if level == len(arr):
            permuted_tasks = permuteTasks(arr, Tasks)
            C = calculate_Cmax(permuted_tasks, SorC=1)
            Cmax = C[-1, -1]
            if Cmax < min_Cmax:
                min_Cmax = Cmax
                best_perm = arr.copy()
        else:
            for i in range(level, len(arr)):
                arr[level], arr[i] = arr[i], arr[level]
                generate_permutations(arr, level + 1)
                arr[level], arr[i] = arr[i], arr[level]
    generate_permutations(task_order)
    return min_Cmax, best_perm

def calculate_LB(Tasks, pi, N, method=0):
    m, n = Tasks.shape  # m maszyn, n zadań
    if pi:
        permuted = permuteTasks(pi, Tasks)
        C = calculate_Cmax(permuted, SorC=1)
        C_current = C[:, len(pi)-1]
    else:
        C_current = np.zeros(m)
    if method == 0:  # LB0
        LB = C_current[-1] + sum(Tasks[m - 1, j] for j in N)
    elif method == 1:  # LB1
        LB = max(C_current[i] + sum(Tasks[i, j] for j in N) for i in range(m))
    elif method == 2:  # LB2
        LB = 0
        for i in range(m):
            sum_pij = sum(Tasks[i, j] for j in N)
            min_rest = sum(min(Tasks[k, j] for j in range(n)) for k in range(i + 1, m))
            val = C_current[i] + sum_pij + min_rest
            LB = max(LB, val)
    elif method == 3:  # LB3
        LB = 0
        for i in range(m):
            sum_pij = sum(Tasks[i, j] for j in N)
            min_rest = sum(min(Tasks[k, j] for j in N) for k in range(i + 1, m)) if N else 0
            val = C_current[i] + sum_pij + min_rest
            LB = max(LB, val)
    elif method == 4:  # LB4
        LB = 0
        for i in range(m):
            sum_pij = sum(Tasks[i, j] for j in N)
            min_sum = min((sum(Tasks[k, j] for k in range(i + 1, m)) for j in N), default=0)
            val = C_current[i] + sum_pij + min_sum
            LB = max(LB, val)
    else:
        raise ValueError("Unknown LB method")
    return LB

def branch_and_bound(Tasks,method = 0):
    min_Cmax = float('inf')
    best_perm = None
    task_order = list(range(Tasks.shape[1]))
    UB = min_Cmax
    def BnB(N, pi):
        nonlocal min_Cmax, best_perm, UB, method
        if not N:
            permuted_tasks = permuteTasks(pi, Tasks)
            C = calculate_Cmax(permuted_tasks, SorC=1)
            Cmax = C[-1, -1]
            if Cmax < min_Cmax:
                min_Cmax = Cmax
                best_perm = pi.copy()
                UB = min_Cmax
        else:
            for j in N:
                N_copy = N.copy()
                N_copy.remove(j)
                pi.append(j)
                LB = calculate_LB(Tasks, pi, N_copy, method)
                if LB < UB:
                    BnB(N_copy, pi)
                pi.pop()

    BnB(task_order, [])
    return best_perm, min_Cmax


if __name__ == "__main__":
    tasks = gen(123123, 7, 6)
    print("Macierz zadań:")
    print(tasks)
    S,C = calculate_Cmax(deepcopy(tasks))
    print("Macierz S:")
    print(S)
    print("Macierz C:")
    print(C)
    print("=================================")
    print("Macierz po algorytmie uogulnionym Johnsona ")
    jonson = alf_Johnson(tasks)
    jonsonS,jonsonC = calculate_Cmax(jonson)
    print("Macierz S po algorytmie Johnson:")
    print(jonsonS)
    print("Macierz C po algorytmie Johnsona:")
    print(jonsonC)
    print("=================================")
    print("Brute Force")
    best_Cmax, best_permutation = bruteForce(deepcopy(tasks))
    print(f"best C_max = {best_Cmax}")
    print(f"best permutation =\n {permuteTasks(best_permutation,tasks)}")
    print("=================================")
    print("B&B")
    best_perm, min_Cmax = branch_and_bound(tasks,0)
    print(f"min B&B C_max = {min_Cmax}")
    print(f"min permutation =\n {permuteTasks(best_perm,tasks)}")
"""
    Done == uogulnienie Jonsona dla m > 2
    Done == Po prostu  (Brute Force) mam stos który symuluje drzewo
    Done == B&B

    na 5.5
    badania replikowalne
    ilość maszyn: 5, 10, 20
    liczba zadąń: dowolna min: 10
    wyniki w porocentach

    dla 5 zadań przegląd zupełny
    wykres porównanie LB 
"""