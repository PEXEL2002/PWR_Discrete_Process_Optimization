# Laboratorium 2 – Rozwiązanie problemu FP || C<sub>max</sub>

## 🎯 Cel zadania

Celem laboratorium było zapoznanie się z teorią szeregowania zadań oraz rozwiązywaniem problemów wielomaszynowych na przykładzie **permutacyjnego problemu przepływowego (Permutation Flow Shop Problem)**.  
Zadanie polegało na:
- Zdefiniowaniu problemu (funkcja celu i ograniczenia),
- Przygotowaniu danych wejściowych,
- Implementacji algorytmów:
  - Johnsona (dla 2 maszyn),
  - Przeglądu zupełnego (Brute Force),
  - Metody podziału i ograniczeń (Branch and Bound),
- Analizie działania i jakości algorytmów oraz wpływu dolnych ograniczeń.

## 🧠 Opis problemu

Problem **FP || C<sub>max</sub>** zakłada:
- Zbiór **n zadań**, z których każde składa się z **m operacji**,
- Operacje wykonywane są **w tej samej kolejności** technologicznej na wszystkich maszynach (1 → 2 → ... → m),
- Na każdej maszynie w danym momencie może być wykonywana tylko **jedna operacja**,
- Czas wykonania operacji `o<sub>ij</sub>` (zadanie `j` na maszynie `i`) to `p<sub>ij</sub>`,
- Celem jest **minimalizacja czasu zakończenia wszystkich zadań**:

\[
C_{max} = \max_{j \in J} C_{m,\pi(j)}
\]

## 📋 Przebieg zajęć

**Zajęcia 5–7** (łącznie 6 godzin) obejmowały:
- Generację instancji testowych,
- Implementację:
  - Funkcji celu (`C_max`),
  - Algorytmu Johnsona (dla 2 maszyn),
  - Brute Force (dla małych instancji),
  - Branch and Bound (dokładna metoda przeszukiwania drzewa przestrzeni rozwiązań),
- Ocenę działania algorytmów i wpływu metod liczenia dolnych ograniczeń (`LB`).

### 💯 Kryteria oceniania

- **Ocena 3:** Poprawna implementacja Johnsona dla FP2||Cmax,
- **Ocena 4:** Johnson + prosty BF lub bardzo prosty BnB dla FP || Cmax,
- **Ocena 5:** Johnson + pełna wersja BF + BnB z poprawnym LB i UB,  
  - +0,5 za analizę wpływu sposobu liczenia `LB`.

## 🧪 Przykład instancji

Dla instancji:

| j | p<sub>1j</sub> | p<sub>2j</sub> | p<sub>3j</sub> |
|--:|:--------------:|:--------------:|:--------------:|
| 1 | 4 | 1 | 4 |
| 2 | 4 | 3 | 3 |
| 3 | 1 | 2 | 3 |
| 4 | 5 | 1 | 3 |

Dla permutacji `π = (1, 2, 3, 4)`, harmonogram można zobaczyć na wykresie Gantta.  
**C<sub>max</sub> = czas zakończenia ostatniej operacji na ostatniej maszynie.**

## 🧬 Generacja instancji

Dla parametrów `n`, `m` oraz ziarna `Z`:

1. `init(Z)`  
2. Dla każdego `j ∈ J` oraz `i ∈ M`:  
   `p<sub>ij</sub> ← nextInt(1, 29)`

## ⚙️ Zaimplementowane algorytmy

- ✅ **Johnson** – optymalny dla dwóch maszyn (FP2||Cmax),
- ✅ **Brute Force** – przegląd wszystkich permutacji,
- ✅ **Branch and Bound (BnB)** – metoda przeszukiwania z dolnym ograniczeniem (`LB`) i górnym ograniczeniem (`UB`), pozwalająca na odcinanie niekorzystnych gałęzi.
