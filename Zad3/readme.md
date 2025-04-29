# Laboratorium 3 – Rozwiązanie problemu 1||∑wᵢTᵢ

## 🎯 Cel zadania

Celem laboratorium było zapoznanie się z podstawami teorii szeregowania zadań oraz sposobami modelowania i rozwiązywania podstawowych problemów dyskretnych.  
Zadanie obejmowało:
- Zdefiniowanie problemu (ograniczenia i funkcja celu),
- Przygotowanie danych wejściowych,
- Implementację dedykowanych algorytmów:
  - Zachłannego,
  - Przeglądu zupełnego (Brute Force),
  - Programowania dynamicznego (rekurencyjnego i iteracyjnego),
- Analizę działania algorytmów oraz interpretację wyników.

## 🧠 Opis problemu

Rozważany jest problem **1||∑wᵢTᵢ**, czyli jednomaszynowy problem szeregowania z minimalizacją ważonej sumy opóźnień.  
Dane:
- Zbiór zadań \( J = \{1, 2, ..., n\} \),
- Każde zadanie `j` opisane przez:
  - `pⱼ` – czas wykonania,
  - `wⱼ` – waga (współczynnik kary),
  - `dⱼ` – żądany termin zakończenia.

Zadania:
- Muszą być wykonywane bez przerw,
- Występują kolejno (ciągłość pracy maszyny),
- Spóźnienie definiujemy jako:

  T_{pi(j)} = max(C_{pi(j)} - d_{pi(j)}, 0)

Funkcja celu:
F(pi) = sum_{j in J} w_{pi(j)} * T_{pi(j)}

Celem jest znalezienie permutacji `π`, która minimalizuje wartość funkcji `F`.

## 📋 Przebieg zajęć

**Zajęcia 8–9** (łącznie 4 godziny) obejmowały:
- Implementację generatora instancji (rozmiar, zakres, źródło danych),
- Implementację metody oceny rozwiązania,
- Implementację algorytmów:
  - Zachłannego (sortowanie po `dⱼ`),
  - Przeglądu zupełnego (dla małych `n`),
  - Programowania dynamicznego (rekurencyjnie i iteracyjnie),
- Porównanie działania algorytmów dla różnych zakresów terminów `dⱼ`.


## 🧪 Przykład instancji

Dla instancji:

| j | pⱼ | wⱼ | dⱼ |
|--:|:--:|:--:|:--:|
| 1 | 3  | 3  | 3  |
| 2 | 4  | 2  | 10 |
| 3 | 2  | 1  | 6  |
| 4 | 2  | 2  | 15 |
| 5 | 3  | 4  | 21 |
| 6 | 4  | 2  | 16 |

Dla permutacji `π = (1, 2, 3, 4, 5, 6)`:

| j | Sⱼ | Cⱼ | Tⱼ |
|--:|:--:|:--:|:--:|
| 1 | 0  | 3  | 0  |
| 2 | 3  | 7  | 0  |
| 3 | 7  | 9  | 3  |
| 4 | 9  | 11 | 0  |
| 5 | 11 | 14 | 0  |
| 6 | 14 | 18 | 2  |

**F(π) = 7**

## 🧬 Generacja instancji

Dla parametrów `n`, `Z` (ziarno):

1. `init(Z)`  
2. Dla każdego `j ∈ J`:  
   - `pⱼ ← nextInt(1, 29)`  
3. `A ← ∑ pⱼ`  
4. `wⱼ ← nextInt(1, 9)`  
5. `dⱼ ← nextInt(1, X)` gdzie X = A lub X = 29

## ⚙️ Zaimplementowane algorytmy

- ✅ **Brute Force** – pełny przegląd permutacji `n!`,
- ✅ **Algorytm zachłanny** – sortowanie po `dⱼ`,
- ✅ **Programowanie dynamiczne**:
  - Wersja rekurencyjna z memoizacją,
  - Wersja iteracyjna z bitową reprezentacją zbiorów,
  - Backtracking – odtwarzanie rozwiązania.

## 📈 Optymalizacja

- Bitowa reprezentacja podproblemów:  
  `D = bin(...)` → szybki dostęp do `memory[D]` w czasie `O(1)`  
- Wydajność:
  - Rozmiar tablicy `memory` to `2ⁿ`
  - Efektywna iteracja po podproblemach

## 🛠 Operacje bitowe

| Operacja | Opis                              |
|----------|-----------------------------------|
| `x | y`  | Alternatywa bitowa                |
| `x ^ y`  | Różnica symetryczna               |
| `x & y`  | Koniunkcja bitowa                 |
| `x << n` | Przesunięcie w lewo o `n` bitów   |
| `x >> n` | Przesunięcie w prawo o `n` bitów  |
| `~x`     | Negacja bitowa                    |
