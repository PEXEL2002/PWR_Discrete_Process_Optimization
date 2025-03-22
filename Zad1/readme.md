# Laboratorium 1 – Rozwiązanie problemu 1|r<sub>j</sub>, q<sub>j</sub>|C<sub>max</sub>

## 🎯 Cel zadania

Celem laboratorium było zapoznanie się z jednomaszynowym problemem szeregowania zadań z czasami dostępności i dostarczenia (RPQ).  
Zadanie polegało na:
- Zdefiniowaniu problemu (funkcja celu i ograniczenia),
- Przygotowaniu danych wejściowych,
- Implementacji algorytmów Schrage i Carlier,
- Analizie ich działania na wygenerowanych instancjach.

## 🧠 Opis problemu

Problem **1|r<sub>j</sub>, q<sub>j</sub>|C<sub>max</sub>** zakłada:
- Zbiór **n zadań**, które mają:
  - **r<sub>j</sub>** – czas dostępności,
  - **p<sub>j</sub>** – czas wykonania,
  - **q<sub>j</sub>** – czas dostarczenia (tzw. „czas stygnięcia”),
- Maszyna przetwarza zadania jedno po drugim (brak równoległości),
- Celem jest **zminimalizowanie maksymalnego czasu zakończenia i dostarczenia zadań**:
  
  \[
  C_{max} = \max_{j \in J} (C_j + q_j)
  \]

### 📍 Wersja z przerwaniami

W problemie **1|r<sub>j</sub>, q<sub>j</sub>, pmtn|C<sub>max</sub>** dopuszcza się przerywanie zadań, co wymaga użycia zmodyfikowanego algorytmu Schrage (`SchragePmtn`).

## 📋 Przebieg zajęć

**Zajęcia 2–4** obejmowały:
- Generację instancji danych,
- Obliczanie funkcji celu,
- Implementację:
  - Algorytmu Schrage,
  - Schrage z przerwaniami (pmtn),
  - Algorytmu Carlier’a (dokładny, oparty na metodzie podziału i ograniczeń),
- Analizę wpływu parametrów (np. zakresów wartości q<sub>j</sub>).

## 🧪 Przykład instancji

Dla danych:

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| r<sub>j</sub> | 1 | 2 | 8 | 7 | 6 | 4 |
| p<sub>j</sub> | 2 | 3 | 1 | 2 | 3 | 4 |
| q<sub>j</sub> | 5 | 4 | 6 | 3 | 7 | 1 |

Wygenerowany harmonogram:

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| S<sub>j</sub> | 1 | 3 | 8 | 9 | 11 | 14 |
| C<sub>j</sub> | 3 | 6 | 9 | 11 | 14 | 18 |
| C<sub>j</sub> + q<sub>j</sub> | 8 | 10 | 15 | 14 | **21** | 19 |

→ **C<sub>max</sub> = 21**

## 🧬 Generacja instancji

Dla `n` i ziarna `Z`:

1. `init(Z)`
2. Dla każdego j: `p<sub>j</sub> ← nextInt(1, 29)`
3. A ← ∑ p<sub>j</sub>
4. Dla każdego j: `r<sub>j</sub> ← nextInt(1, A)`
5. Dla każdego j: `q<sub>j</sub> ← nextInt(1, X)` (testowane dla X = 29 oraz X = A)

## 🧠 Zaimplementowane algorytmy

- ✅ **Schrage** – wersja bez przerwań
- ✅ **SchragePmtn** – wersja z przerwaniami
- ✅ **Carlier** – dokładna metoda z zastosowaniem *branch & bound* (metoda podziału i ograniczeń – algorytm przeszukuje przestrzeń możliwych rozwiązań, odrzucając te, które nie mogą dać lepszego wyniku niż już znalezione rozwiązanie)