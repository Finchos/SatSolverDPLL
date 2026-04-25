from enum import Enum


class FormulaFormatError(Exception):
    pass



class Value(Enum):
    FALSE = 0
    TRUE = 1
    NONE= 2

