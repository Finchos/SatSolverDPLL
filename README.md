# SAT Solver - DPLL

**Autor:** Šimon Kolařík
**Jazyk:** Python 3 (bez závislostí na externích knihovnách)

## Struktura
* `main.py` - Hlavní vstupní bod programu (I/O, měření času).
* `dpll.py` - Samotná implementace algoritmu.
* `formula_tools/` - Modul pro parsování DIMACS formátu a poskytuje abstrakci pro čitelnější kód v samotném dpll
* `benchmarking.py` - Nástroj pro hromadné testování a generování CSV.

## Jak program spustit

Program nevyžaduje instalaci žádných balíčků. Stačí spustit hlavní skript pomocí terminálu ve složce celého projektu:

python3 main.py

Následně se program zeptá na cestu k cnf souboru v DIMACS formátu (doporučuji použít absoltní cestu)
