from RandomNumberGenerator import RandomNumberGenerator
import numpy as np

def gen(seed,n):
    rand = RandomNumberGenerator(seed)
    S = []
    for i in range(n):
        S.append([rand.nextInt(1,29)])
    maxr = np.sum(S)
    for i in range(n):
        S[i].append(rand.nextInt(1,maxr))
    return S

def printGen(S):
    """R - przygotowania
        P - czas przetwarzania
        """
    print(S)

def C_max(S):
    cMax = 0
    cMax += S[0][0]
    for i in range(len(S)-1):
        cMax += S[i][1]
        if cMax < S[i+1][0]:
            cMax += S[i+1][0] - cMax
    cMax += S[-1][1]
    return cMax

def sort(S):
    S_sorted = sorted(S, key=lambda x: x[0])
    return S_sorted

if __name__ == '__main__':
    seed = int(input("Podaj ziarno losowania: "))
    n = int(input("Podaj liczbę operacji: "))
    S = gen(seed,n)
    print("Wygenerowana sekfencja: ")
    printGen(S)
    print("C_max:",C_max(S))
    print("Posortowana kolejność: ")
    S = sort(S)
    printGen(S)
    print("C_max dla posortowanego :", C_max(S))