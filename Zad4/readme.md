# Laboratorium 4 – Rozwiązanie problemu J || C<sub>max</sub>

## 🎯 Cel zadania

Celem laboratorium było zapoznanie się z metodami przybliżonymi na przykładzie problemu **J || C<sub>max</sub>** (problem gniazdowy).  
Zadanie obejmowało:
- Zdefiniowanie problemu (funkcja celu, ograniczenia),
- Implementację generatora instancji,
- Implementację **algorytmu konstrukcyjnego INSA**,
- Budowę harmonogramu na podstawie permutacji operacji,
- Ocenę i interpretację wyników.

## 🧠 Opis problemu

Rozważany jest problem **J || C<sub>max</sub>**, czyli szeregowanie zadań z różną liczbą operacji i indywidualną marszrutą na wielu maszynach.

- Zbiór zadań `J = {1, 2, ..., n}`,
- Każde zadanie `j` składa się z `oⱼ` operacji,
- Każda operacja `k` ma:
  - Czas wykonania `p_{k,j}`,
  - Maszynę `µ_{k,j}` przypisaną do jej realizacji.

Harmonogramowanie uwzględnia:
- Kolejność operacji wewnątrz zadania,
- Dostępność maszyny (jedna operacja w danym czasie),
- Celem jest **minimalizacja czasu zakończenia wszystkich operacji**:


C<sub>max</sub> = max_{k \in O} C<sub>k</sub>


## 📋 Przebieg zajęć

**Zajęcia 10–11** (łącznie 4 godziny) obejmowały:
- Implementację generatora instancji (rozmiar, ziarno, zakres),
- Implementację funkcji oceniającej harmonogram (`C_max`),
- Implementację **algorytmu INSA** dla J || C<sub>max</sub>,
- Analizę wyników oraz porównania dla różnych permutacji operacji.

## ⚙️ Zaimplementowany algorytm

- ✅ **INSA (Insertion-based Scheduling Algorithm)** – algorytm konstrukcyjny dedykowany dla J || C<sub>max</sub>.
  - Operacje są wstawiane kolejno w odpowiednie miejsce w harmonogramie,
  - Kolejność ustalana z zachowaniem marszruty i zasobów maszynowych.

## 🧬 Generacja instancji

Dla parametrów `n` (liczba zadań), `m` (liczba maszyn), `Z` (ziarno):

```python
init(Z)
for j in range(n):
    o_j = nextInt(1, floor(1.2 * m))  # liczba operacji w zadaniu j
    for k in range(o_j):
        p_kj = nextInt(1, 29)         # czas wykonania operacji
        µ_kj = nextInt(1, m)          # przypisana maszyna
