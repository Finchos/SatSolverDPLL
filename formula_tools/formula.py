import re

from formula_tools.clause import Clause
from formula_tools.literal import Literal
from formula_tools.utils import FormulaFormatError

pattern = re.compile(r"^p\s+cnf\s+([0-9]+)\s+([0-9]+)$")

class Formula:

    def __init__(self, file_path):

        Literal.clear_pool()

        self._variables_count = 0
        self._clauses_count = 0
        self._clauses = []

        with open(file_path, 'r', encoding="utf-8") as file:
            check = 0
            contains_head = False

            for line in file:
                line = line.strip()

                if not line or line.startswith('c'):
                    continue

                if contains_head:
                    clause = Clause(line, self._variables_count)
                    self._clauses.append(clause)
                    check += 1
                else:
                    match = pattern.fullmatch(line)

                    if match:
                        self._variables_count = int(match.group(1))
                        self._clauses_count = int(match.group(2))
                        contains_head = True
                    else:
                        raise FormulaFormatError("invalid format of formula")

            if check != self._clauses_count:
                raise FormulaFormatError("number of clauses exceeds maximum number of clauses")

    @property
    def variables_count(self):
        return self._variables_count

    @property
    def clauses_count(self):
        return self._clauses_count

    @property
    def clauses(self):
        return self._clauses

