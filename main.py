import time

import dpll
from formula_tools.formula import Formula
from formula_tools.utils import Value

#phase 1
path = input("Enter cnf file path: ")

#phase 2
init_time_start = time.time()
formula = Formula(path)
init_time = time.time() - init_time_start

#phase 3
solve_time_start = time.time()
result = dpll.search(formula)
solve_time = time.time() - solve_time_start

#phase 4
values = dpll.assigns
propagation = dpll.propagation
decision = dpll.decision

#phase 5
print(result)
if result == "SAT":
    litereal_eval = []
    for i in range(1, dpll.vars + 1):
        if values[i] == Value.TRUE:
            litereal_eval.append(i)
        if values[i] == Value.FALSE:
            litereal_eval.append(-i)
    print(litereal_eval)
else:
    print("")

print(init_time)
print(solve_time)
print(propagation)
print(decision)

