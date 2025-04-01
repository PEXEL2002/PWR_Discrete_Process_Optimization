from RandomNumberGenerator import RandomNumberGenerator
import numpy as np
from copy import copy, deepcopy

def gen(seed,n):
    rand = RandomNumberGenerator(seed)
    S = []
    for i in range(n):
        S.append([0,0,0])
        S[i][1]=rand.nextInt(1,29)
    maxr = 0
    for i in range(n):
        maxr +=S[i][1]
    for i in range(n):
        S[i][0]=rand.nextInt(1,maxr)
    X = 29
    for i in range(n):
        S[i][2]=rand.nextInt(1, X)
    return S
def printGen(S):
    print("ID\tr\tp\tq")
    for i, task in enumerate(S):
        print(f"{i+1}\t{task[0]}\t{task[1]}\t{task[2]}")

def C_max(s):
    t = s[0][0]
    C = t + s[0][1]
    C_max = C + s[0][2]
    for j in range(1, len(s)):
        t = max(s[j][0], C)
        C = t + s[j][1]
        C_max = max(C_max, C + s[j][2])
    return C_max

def schrage(tasks):
    N = sorted(tasks, key=lambda x: x[0])
    G = []
    pi = []
    C_max = 0
    t = N[0][0] if N else 0
    while G or N:
        while N and N[0][0] <= t:
            G.append(N.pop(0))
        if G:
            j_star = max(G, key=lambda x: x[2])
            G.remove(j_star)
            pi.append(j_star)
            t += j_star[1]
            C_max = max(C_max, t + j_star[2])
        else:
            t = N[0][0] if N else t
    return [list(task) for task in pi], C_max

def schrageWithInterupt(tasks):
    N = [list(task) for task in sorted(tasks, key=lambda x: x[0])]
    G = []
    t = 0
    C_max = 0
    l = None
    while G or N:
        while N and N[0][0] <= t:
            j = list(N.pop(0))
            G.append(j)
            if l and j[2] > l[2]:
                l[1] -= (t - j[0])
                t = j[0]
                if l[1] > 0:
                    G.append(l)
        if G:
            j_star = max(G, key=lambda x: x[2])
            G.remove(j_star)
            l = list(j_star)
            t += l[1]
            C_max = max(C_max, t + l[2])
        else:
            t = N[0][0] if N else t
    return C_max

def find_task_index(task, tasks):
    for i, t in enumerate(tasks):
        if t[0] == task[0] and t[1] == task[1] and t[2] == task[2]:
            return i
    raise ValueError("Task not found in original list.")


def carlier(tasks, UB=float('inf'), best_pi=None):
    pi, U = schrage(tasks)
    if U < UB:
        UB = U
        best_pi = [list(task) for task in pi]
    C = 0
    S = []
    C_max_list = []
    for task in pi:
        C = max(C, task[0]) + task[1]
        S.append(C - task[1])
        C_max_list.append(C + task[2])
    b = max(range(len(C_max_list)), key=lambda j: C_max_list[j])
    a = None
    for j in range(b + 1):
        sum_p = sum(pi[k][1] for k in range(j, b + 1))
        if pi[j][0] + sum_p + pi[b][2] == C_max_list[b]:
            a = j
            break
    c = None
    for j in range(b - 1, a-1, -1):
        if pi[j][2] < pi[b][2]:
            if c is None:
                c = j
            else:
                if pi[j][2] > pi[c][2]:
                    c = j
    if c is None:
        return UB, best_pi

    # Wyznacz K, r̂, q̂, p̂
    K = pi[c + 1:b + 1]
    r_hat = min((task[0] for task in K), default=0)
    q_hat = min((task[2] for task in K), default=0)
    p_hat = sum(task[1] for task in K)

    task_c = pi[c]
    idx_c = find_task_index(task_c, tasks)

    tasks_r = [list(task) for task in tasks]
    restoreR = tasks_r
    tasks_r[idx_c][0] = max(task_c[0], r_hat + p_hat)
    LB = schrageWithInterupt(tasks_r)
    if LB < UB:
        carlier(tasks_r, UB, best_pi)
    tasks_r = restoreR

    tasks_q = [list(task) for task in tasks]
    restoreQ = tasks_q
    tasks_q[idx_c][2] = max(task_c[2], q_hat + p_hat)
    LB = schrageWithInterupt(tasks_q)
    if LB < UB:
        carlier(tasks_q, UB, best_pi)
    tasks_q = restoreQ
    return UB, best_pi
seed = int(input("Podaj ziarno losowania: "))
n = int(input("Podaj liczbę operacji: "))
S = gen(seed,n)
data_copy = deepcopy(S) # tworzenie głębokiej kopi
S_shrage = schrage(deepcopy(S))
S_schrage = C_max(S_shrage[0])
S_schrage_with_Interupt = schrageWithInterupt(deepcopy(S))
S_carier = carlier(deepcopy(S), float('inf'))
print(S_carier)
print("Wygenerowana sekfencja: ")
printGen(S)
print("C_max:",C_max(S))
#print("Wynik po algorytmnie Shrage: ")
#printGen(S_shrage[0])
print(f"C_max dla Shrage: {S_shrage[1]}" )
print(f"C_max dla Shrage z przerwaniami: {S_schrage_with_Interupt}")
#print(f"Wynik po algorytmie Carlier:")
#printGen(S_carier[1])
print(f"C_max po algorytmie Carlier: {S_carier[0]}")

""" DANE TESTOWE
          (C_max)    Schrage Carlier
data:1     25994      13981   13862
data:2     33465      21529   20917
data:3     57403      31683   31343
data:4     51444      34444   33878
"""
# data1 = [[8354, 1, 5507], [8455, 696, 512],[2900, 435, 8619],[6176, 424, 3688],[586, 971, 76],
#          [7751, 134, 5877],[7935, 516, 3017],[5957, 266, 5540],[68, 275, 4040],[1688, 308, 2907],
#          [436, 171, 2963],[5683, 412, 6456],[3066, 14, 3960],[5104, 792, 5696],[8200, 258, 1170],
#          [8731, 726, 3081],[5017, 912, 5131],[84, 124, 3846],[8355, 473, 1100],[1541, 306, 6302],
#          [1808, 20, 5363],[114, 874, 5494],[3815, 472, 759],[2734, 482, 7478]]
# data2 = [
#     [0, 831, 0], [0, 867, 0], [0, 814, 0], [0, 915, 0], [0, 947, 0],
#     [0, 997, 0], [0, 826, 0], [0, 966, 0], [0, 946, 0], [0, 871, 0],
#     [0, 894, 0], [0, 989, 0], [0, 910, 0], [0, 851, 0], [0, 852, 0],
#     [0, 931, 0], [0, 863, 0], [0, 822, 0], [0, 982, 0], [0, 926, 0],
#     [0, 993, 0], [0, 945, 0], [0, 978, 0], [8368, 1, 12548]
# ]
# data3 = [
#     [15808, 838, 11659], [11731, 470, 14049], [8933, 177, 8647], [15165, 472, 4137], [10164, 732, 13213],
#     [9520, 768, 2848], [13481, 895, 11629], [16681, 524, 13649], [237, 811, 15392], [360, 890, 1967],
#     [15796, 746, 13667], [2136, 278, 16456], [8538, 901, 4775], [6024, 810, 11081], [2585, 401, 828],
#     [7363, 446, 10186], [10646, 283, 2371], [12951, 89, 4913], [5838, 890, 14786], [14342, 581, 4353],
#     [9183, 755, 15985], [1779, 78, 17029], [14311, 915, 15371], [16625, 631, 13507], [4447, 820, 6351],
#     [3713, 602, 13893], [14087, 80, 10919], [8794, 339, 8833], [1340, 950, 8731], [796, 225, 6267],
#     [7073, 475, 16773], [9661, 910, 6338], [2954, 862, 14425], [10270, 529, 9684], [2394, 869, 12045],
#     [4633, 55, 2210], [6519, 455, 1497], [10455, 200, 12583], [10056, 886, 6003], [13293, 476, 16248],
#     [10386, 275, 16512], [982, 51, 579], [7028, 674, 3541], [468, 446, 887], [13872, 375, 16660],
#     [10637, 324, 11792], [2168, 347, 1592], [849, 550, 5221]
# ]
# data4 = [
#     [11677, 544, 2607], [8548, 616, 5612], [16383, 259, 3807], [9028, 124, 14310], [16337, 642, 10526],
#     [5655, 873, 13648], [2756, 162, 7089], [2365, 527, 3206], [10868, 836, 2817], [6086, 300, 8692],
#     [16651, 875, 1550], [2356, 542, 15443], [9581, 970, 17113], [14007, 898, 14057], [4695, 720, 14801],
#     [7391, 387, 4611], [1180, 321, 7311], [16868, 922, 16055], [899, 136, 9421], [1255, 630, 5519],
#     [1363, 166, 17011], [11196, 604, 5447], [3298, 743, 9029], [4336, 274, 11206], [2225, 611, 8642],
#     [7696, 421, 7240], [5801, 512, 7569], [7739, 577, 2521], [2318, 959, 3608], [9952, 280, 14196],
#     [7748, 592, 873], [6242, 642, 5133], [11292, 481, 14653], [16817, 259, 15829], [12313, 191, 3968],
#     [8414, 16, 13600], [502, 350, 17206], [16484, 25, 1261], [15749, 289, 14335], [16075, 309, 8495],
#     [2117, 626, 12438], [9434, 99, 2360], [5618, 426, 10292], [15660, 303, 6816], [1021, 121, 7862],
#     [7004, 857, 12068], [9750, 768, 13436], [5673, 203, 9138]
# ]
# data = [data1,data2,data3,data4]
# C_maxT = [25994,33465,57403,51444]
# SchrageT = [13981,21529,31683,34444]
# CarierT = [13862,20917,31343,33878]
# for i in range(4):
#     data_copy = [list(task) for task in deepcopy(data[i])]
#     print(f"carlier {i+1}")
#     car = carlier(data_copy, UB=float('inf'))[0]
#     print(f"c_max {i+1}")
#     C_maxV = C_max(deepcopy(data_copy))
#     print(f"schrage {i+1}")
#     schrageV = schrage(deepcopy(data_copy))[1]
#     if CarierT[i] != car:
#         print(f"błąd dla liczenia Carier {i+1}")
#         print(f"{CarierT[i]} \t {car}")
#     if C_maxT[i] != C_maxV:
#         print(f"błąd dla liczenia C_max {i+1}")
#     if SchrageT[i] != schrageV:
#         print(f"błąd dla liczenia Schrage {i+1}")
#         print(f"{SchrageT[i]} \t {schrageV}")
#     print(i)