import numpy as np
from RandomNumberGenerator import RandomNumberGenerator
def gen(seed,n,m):
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


if __name__ == "__main__":
    pass