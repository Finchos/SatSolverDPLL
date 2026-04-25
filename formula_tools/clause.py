from formula_tools.literal import Literal
from formula_tools.utils import FormulaFormatError, Value


class Clause:

    def __init__(self, line, max_var_count):
        parts = line.split()

        self._vars = []

        for part in parts:
            if part == '0':
                break
            try:
                var = int(part)
                if abs(var) > max_var_count:
                    raise FormulaFormatError("number of variables exceeds maximum number of variables")
                literal = Literal(var)
                self._vars.append(literal)

            except ValueError:
                raise FormulaFormatError("invalid format of clause")

        if len(self._vars) > 0:
            self._vars[0].add_watched_in(self)
        if len(self._vars) > 1:
            self._vars[1].add_watched_in(self)

    def __getitem__(self, index):
        return self._vars[index]

    def __len__(self):
        return len(self._vars)

    def __setitem__(self, key, value):
        self._vars[key] = value

    @property
    def vars(self):
        return self._vars

    def watched(self):
        w1 = self._vars[0] if len(self._vars) > 0 else None
        w2 = self._vars[1] if len(self._vars) > 1 else None
        return w1, w2

