# Laboratorium 0 – Wprowadzenie do teorii szeregowania zadań

## 🎯 Cel zadania

Celem laboratorium jest poznanie podstaw teorii szeregowania zadań, sposobów ich modelowania oraz rozwiązywania prostych problemów szeregowania.  
W szczególności laboratorium obejmuje:
- Zdefiniowanie problemu (ograniczenia oraz funkcja celu),
- Określenie danych wejściowych,
- Implementację prostego algorytmu opartego na sortowaniu,
- Interpretację wyników.

## 🧠 Opis problemu

Rozważany problem to klasyczne zadanie z teorii szeregowania, oznaczane jako:  
**1‖r<sub>j</sub>‖C<sub>max</sub>**

Dany jest zbiór zadań **J = {1, 2, ..., n}**, które mają zostać wykonane na jednej maszynie.  
Każde zadanie **j** ma dwa parametry:
- **r<sub>j</sub>** – czas przygotowania (moment dostępności zadania),
- **p<sub>j</sub>** – czas wykonania.

Ograniczenia:
- W danym momencie maszyna może wykonywać tylko jedno zadanie,
- Zadania są wykonywane nieprzerwanie,
- Każde kolejne zadanie może się rozpocząć dopiero po przygotowaniu oraz zakończeniu poprzedniego.

Celem jest minimalizacja czasu zakończenia ostatniego zadania:  
**C<sub>max</sub> = C<sub>π(n)</sub>**

## 🔄 Przebieg zajęć

1. Wygenerowanie instancji danych (rozmiar, ziarno, zakres),
2. Implementacja funkcji celu (C<sub>max</sub>),
3. Implementacja algorytmu szeregowania opartego na sortowaniu,
4. Porównanie wyników dla różnych permutacji zadań.

## 🧪 Przykład

Dla danych:

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| r<sub>j</sub> | 1 | 2 | 8 | 7 | 6 | 4 |
| p<sub>j</sub> | 2 | 3 | 1 | 2 | 3 | 4 |

Uzyskano harmonogram z czasami startu (S<sub>j</sub>) i zakończenia (C<sub>j</sub>) zadań:

| j | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| S<sub>j</sub> | 1 | 3 | 8 | 9 | 11 | 14 |
| C<sub>j</sub> | 3 | 6 | 9 | 11 | 14 | **18** |

Zatem **C<sub>max</sub> = 18**.

## 🧬 Generacja instancji

Przykładowy algorytm generacji danych:

1. `init(Z)` – inicjalizacja generatora (ziarno),
2. Dla każdego zadania: `p<sub>j</sub> ← nextInt(1, 29)`,
3. Oblicz sumę A = ∑ p<sub>j</sub>,
4. Dla każdego zadania: `r<sub>j</sub> ← nextInt(1, A)`.

Przykład instancji dla n = 10, Z = 1:

| j | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| r<sub>j</sub> | 52 | 70 | 112 | 5 | 8 | 71 | 90 | 2 | 52 | 9 |
| p<sub>j</sub> | 1  | 4  | 22  | 14| 16| 7  | 2  | 20| 20| 28 |