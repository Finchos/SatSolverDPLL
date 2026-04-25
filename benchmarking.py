import csv
import signal
import time
from pathlib import Path

import dpll
from formula_tools.formula import Formula

benchmark_folder = "/Users/simon/PycharmProjects/SatSolverDPLL/benchmarks/pidgeon-hole/"
result_csv = "/Users/simon/PycharmProjects/SatSolverDPLL/results/results_pidgeon-hole.csv"
timeout_seconds = 30

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()


def main():
    print("Zahajuji procházení složky...")

    signal.signal(signal.SIGALRM, timeout_handler)

    with open(result_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')

        writer.writerow(["File", "Result", "Init Time", "Solve Time", "Propagations", "Decisions"])

        file_list = Path(benchmark_folder).rglob('*.cnf')


        for file in file_list:
            filepath = str(file)
            filename = file.name

            print(f"Zpracovávám: {filename} ...\n", end=" ", flush=True)

            init_time_start = time.process_time()
            try:
                formula = Formula(filepath)
                init_time = time.process_time() - init_time_start
            except Exception as e:
                writer.writerow([filename, "ERROR", 0, 0, 0, 0])
                continue

            solve_time_start = time.process_time()

            signal.alarm(timeout_seconds)

            try:
                result = dpll.search(formula)

                signal.alarm(0)

                solve_time = time.process_time() - solve_time_start
                propagation = dpll.propagation
                decision = dpll.decision
                writer.writerow([filename, result, init_time, solve_time, propagation, decision])

            except TimeoutException:
                solve_time = time.process_time() - solve_time_start
                writer.writerow([filename, "TIMEOUT", init_time, solve_time, "N/A", "N/A"])

            except Exception as e:
                signal.alarm(0)
                writer.writerow([filename, "FATAL", init_time, 0, 0, 0])

            csv_file.flush()

    print("Všechny soubory prošly smyčkou.")


if __name__ == "__main__":
    main()