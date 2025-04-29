# Laboratorium 6 – Projekt dodatkowy na ocenę 5.5  
**Temat 6: Algorytm TabuAB (blokowy) dla problemu FP‖C<sub>max</sub>**

## 🎯 Cel projektu

Celem projektu jest zaimplementowanie algorytmu metaheurystycznego **Tabu Search** w wersji blokowej (**TabuAB**) do rozwiązania **permutacyjnego problemu przepływowego** (**FP‖C<sub>max</sub>**).  
Zadaniem algorytmu jest znalezienie permutacji zadań, wspólnej dla wszystkich maszyn, która minimalizuje czas zakończenia ostatniej operacji (**makespan**).

---

## 🧠 Opis problemu FP‖C<sub>max</sub>

Rozważany jest permutacyjny problem przepływowy:
- Mamy `n` zadań i `m` maszyn,
- Każde zadanie `j` musi przejść kolejno przez maszyny `1 → 2 → ... → m`,
- Czas wykonania zadania `j` na maszynie `i` to `p_ij`,
- Na każdej maszynie może być wykonywane w danym momencie tylko jedno zadanie,
- Celem jest minimalizacja:

C<sub>max</sub> = max_{j in J} C_(m,pi(j))


gdzie `π` to permutacja zadań wspólna dla wszystkich maszyn.

---

## ⚙️ Algorytm TabuAB (blokowy Tabu Search)

Algorytm **TabuAB** opiera się na klasycznym **Tabu Search**, ale operuje na **blokach zadań** zamiast pojedynczych zamian. Kluczowe cechy:
- Generowanie sąsiedztwa przez **przestawianie całych bloków zadań**,
- Wykorzystywanie **listy tabu** (czasowej pamięci ostatnich ruchów),
- Możliwość użycia reguł **aspiracji** (np. nadpisanie tabu, jeśli ruch poprawia globalne minimum),
- Opcjonalne strategie **intensyfikacji** i **dywersyfikacji** po określonej liczbie iteracji bez poprawy.
---


