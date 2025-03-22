from RandomNumberGenerator import RandomNumberGenerator
import numpy as np
import copy

def gen(seed,n):
    rand = RandomNumberGenerator(seed)
    S = []
    for i in range(n):
        S.append([rand.nextInt(1,29)])
    maxr = np.sum(S)
    for i in range(n):
        S[i].append(rand.nextInt(1,maxr))
    X = 29
    for i in range(n):
        S[i].append(rand.nextInt(1, X))
    return S
def printGen(S):
    """
        R - przygotowaniad
        P - czas przetwarzania
        Q - czas chłodzenia przetwarzania
    """
    print(S)

def C_max(s):
    S1 = s[0][0]
    C1 = S1 + s[0][1]
    C_max = C1 + s[0][2]
    for j in range(1, len(s)):
        Sj = max(s[j][0], C1)
        C1 = Sj + s[j][1]
        C_max = max(C_max, C1 + s[j][2])
    return C_max
def sort(S):
    S_sorted = sorted(S, key=lambda x: x[1])
    return S_sorted
def schrage(tasks):
    N = sorted(tasks, key=lambda x: x[0])
    G = []
    pi = []
    C_max = 0
    t = N[0][0] if N else 0
    while len(G) > 0 or len(N) > 0:
        while len(N)>0 and N[0][0] <= t:
            G.append(N.pop(0))
        if len(G) > 0:
            j_star = max(G, key=lambda x: x[2])
            G.remove(j_star)
            pi.append(j_star)
            t += j_star[1]
            C_max = max(C_max, t + j_star[2])
        else:
            t = N[0][0] if N else t
    return pi, C_max
def schrageWithInterupt(tasks):
    N = sorted(tasks, key=lambda x: x[0])
    G = []
    t = 0
    C_max = 0
    l = None
    while G or N:
        while N and N[0][0] <= t:
            j = N.pop(0)
            G.append(j)
            if l and j[2] > l[2]:
                l[1] -= (t - j[0])
                t = j[0]
                if l[1] > 0:
                    G.append(l)
        if G:
            j_star = max(G, key=lambda x: x[2])
            G.remove(j_star)
            l = j_star
            t += j_star[1]
            C_max = max(C_max, t + j_star[2])
        else:
            t = N[0][0] if N else t
    return C_max


def carlier(tasks, UB=float('inf'), best_pi=None):
    pi, U = schrage(tasks)
    if U < UB:
        UB = U
        best_pi = list(pi)
    C_max_values = [sum(task[1] for task in pi[:i + 1]) + pi[i][2] for i in range(len(pi))]
    b = max(range(len(pi)), key=lambda j: C_max_values[j])
    a = min(
        (j for j in range(b + 1)),
        key=lambda j: pi[j][0] + sum(pi[k][1] for k in range(j, b + 1)) + pi[b][2]
    )
    c_candidates = [j for j in range(a, b) if pi[j][2] < pi[b][2]]
    c = max(c_candidates) if c_candidates else None
    if c is None:
        if best_pi is None:
            best_pi = list(pi)
            return UB, best_pi
    K = pi[c + 1:b + 1] if c is not None else []
    r_hat = min((task[0] for task in K), default=0)
    q_hat = min((task[2] for task in K), default=0)
    p_hat = sum(task[1] for task in K)
    original_r_c, original_p_c, original_q_c = pi[c]
    pi_copy = list(pi)
    pi_copy[c] = (max(original_r_c, r_hat + p_hat), original_p_c, original_q_c)
    LB = schrageWithInterupt(pi_copy)
    if LB < UB:
        UB, best_pi = carlier(pi_copy, UB, best_pi)
    pi[c] = (original_r_c, original_p_c, original_q_c)
    pi_copy = list(pi)
    pi_copy[c] = (original_r_c, original_p_c, max(original_q_c, q_hat + p_hat))
    LB = schrageWithInterupt(pi_copy)
    if LB < UB:
        UB, best_pi = carlier(pi_copy, UB, best_pi)
    pi[c] = (original_r_c, original_p_c, original_q_c)
    return UB, best_pi


seed = int(input("Podaj ziarno losowania: "))
n = int(input("Podaj liczbę operacji: "))
S = gen(seed,n)
data_copy = copy.deepcopy(S) # tworzenie głębokiej kopi
S_schrage = C_max(schrage(copy.deepcopy(S))[0])
S_schrage_with_Interupt = schrageWithInterupt(copy.deepcopy(S))
S_carier = carlier(S.copy(), S_schrage)
print("Wygenerowana sekfencja: ")
printGen(S)
print("C_max:",C_max(S))
print("Wynik po algorytmnie Shrage: ")
printGen(schrage(copy.deepcopy(S)))
print(f"C_max dla Shrage: {S_schrage}" )
print(f"C_max dla Shrage z przerwaniami: {S_schrage_with_Interupt}")
print(f"Wynik po algorytmie Carlier:")
printGen(S_carier)
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
#
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
#
# for i in range(4):
#     data_copy = copy.deepcopy(data[i]) # tworzenie głębokiej kopi
#     car = carlier(data_copy, UB=float('inf'))[0]
#     C_maxV = C_max(copy.deepcopy(data[i]))
#     schrageV = schrage(copy.deepcopy(data[i]))[1]
#     if(CarierT[i] != car):
#         print(f"błąd dla liczenia Carier {i+1}")
#         print(f"{CarierT[i]} \t {car}")
#     if(C_maxT[i] != C_maxV):
#         print(f"błąd dla liczenia C_max {i+1}")
#     if(SchrageT[i] != schrageV):
#         print(f"błąd dla liczenia Schrage {i+1}")
#         print(f"{SchrageT[i]} \t {schrageV}")
