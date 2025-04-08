from zad2 import branch_and_bound, calculate_LB, gen, bruteForce
import pandas as pd
import numpy as np
import time

# Definiowanie zmiennych
low, high = 0, 2147483646
seeds = np.linspace(low, high, 20, dtype=int)
machines = [5, 10, 20]
numberOfSentences = [5, 10, 20, 40]

# Lista do przechowywania wyników
results = []

for n in numberOfSentences:
    for m in machines:
        for seed in seeds:
            for i in range(5):
                print(f"n:{n}, m:{m}, seed:{seed}\t Type LB: {i}", end=" ")
                tic = time.perf_counter()
                _, _ = branch_and_bound(gen(seed, n, m), i)
                toc = time.perf_counter()
                time_taken = (toc - tic) * 1000
                print(f"Time: {time_taken:0.4f} ms")
                results.append({
                    'n': n,
                    'm': m,
                    'seed': seed,
                    'LB_type': i,
                    'time_ms': time_taken
                })
            if n == 5:
                print(f"n:{n}, m:{m}, seed:{seed}\t BruteForce", end=" ")
                tic = time.perf_counter()
                _, _ = bruteForce(gen(seed, n, m))
                toc = time.perf_counter()
                time_taken = (toc - tic) * 1000
                print(f"Time: {time_taken:0.4f} ms")
                results.append({
                    'n': n,
                    'm': m,
                    'seed': seed,
                    'LB_type': 'BruteForce',
                    'time_ms': time_taken
                })
df = pd.DataFrame(results)
df.to_csv('wyniki_badania.csv', index=False)
print("Wyniki zapisane do pliku 'wyniki_badania.csv'")
