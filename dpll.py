from collections import deque

from formula_tools.literal import Literal
from formula_tools.utils import Value


vars = 0
clauses = []
assigns = []
level = []
tries = []
activity = []
var_inc = 1.0
var_dec = 0.95
propQ = deque()
trail = []
trail_lim = []
current_level = 0
watches = {}

propagation = 0
decision = 0


def set_globals(formula):
    global vars, clauses, assigns, level, tries, activity, propagation, decision
    global var_inc, var_dec, propQ, trail, trail_lim, current_level, watches

    vars = formula.variables_count
    clauses = formula.clauses

    assigns = [Value.NONE for _ in range(vars + 1)]
    level = [0 for _ in range(vars + 1)]
    tries = [0 for _ in range(vars + 1)]

    activity = [0.0 for _ in range(vars + 1)]
    var_inc = 1.0
    var_dec = 0.95

    propQ = deque()
    trail = []
    trail_lim = []

    current_level = 0

    watches = {}

    for i in range(1, vars + 1):
        watches[i] = []
        watches[-i] = []

    for literal in Literal._pool.values():
        watches[literal].extend(literal.watched_in)

    propagation = 0
    decision = 0


def search(formula):
    set_globals(formula)
    return _search()



def _search():
    while True:
        conflict = propagate()
        if not conflict:
            ok = backtrack()
            if not ok: return "UNSAT"
        else:
            if (len(trail) == vars): return "SAT"
            else:
                p = pick()
                assume(p)


def assume(p):
    global decision
    decision += 1
    trail_lim.append(len(trail))
    global current_level
    current_level += 1
    return enqueue(p)


def enqueue(p):
    val = value(p)

    if val == Value.TRUE:
        return True
    if val == Value.FALSE:
        return False

    v = p.var
    if p.sgn:
        assigns[v] = Value.TRUE
    else:
        assigns[v] = Value.FALSE

    level[v] = len(trail_lim)
    tries[v] += 1
    propQ.append(p)
    trail.append(p)
    return True


def propagate():
    global var_inc
    while propQ:
        p = propQ.popleft()

        tmp = watches[p.neg]
        watches[p.neg] = []

        for i in range(0, len(tmp)):
            ok = propagate_clause(tmp[i], p)
            if not ok:
                for lit in tmp[i]:
                    activity[lit.var] += var_inc
                var_inc /= var_dec
                for k in range(i + 1, len(tmp)):
                    watches[p.neg].append(tmp[k])
                propQ.clear()
                return False
    return True


def value(lit):
    val = assigns[lit.var]
    if val == Value.NONE:
        return Value.NONE
    if (val == Value.TRUE and lit.sgn) or (val == Value.FALSE and not lit.sgn):
        return Value.TRUE
    return Value.FALSE


def propagate_clause(cl, p):
    if cl[1] != p.neg: cl[0], cl[1] = cl[1], cl[0] #swap
    if value(cl[0]) == Value.TRUE:
        watches[p.neg].append(cl)
        return True

    for i in range(2, len(cl)):
        if value(cl[i]) != Value.FALSE:
            cl[i], cl[1] = cl[1], cl[i] #swap
            watches[cl[1]].append(cl)
            return True
    watches[p.neg].append(cl)
    global propagation
    propagation += 1
    return enqueue(cl[0])


def undo_one():
    p = trail.pop()
    v = p.var
    if len(trail) == trail_lim[-1]:
        trail_lim.pop()
        global current_level
        current_level -= 1
    assigns[v] = Value.NONE
    level[v] = -1
    tries[v] = 0


def backtrack():
    while True:
        if len(trail_lim) == 0: return False
        while (len(trail) - 1) > trail_lim[-1]:
            undo_one()
        p = trail[-1]
        if tries[p.var] < 2:
            trail.pop()
            assigns[p.var] = Value.NONE
            if enqueue(p.neg): return True
        else: undo_one()

#heuristic
def pick():
    max_score = -1.0
    best_var = 0
    for i in range(1, vars+1):
        if assigns[i] == Value.NONE:
            if activity[i] > max_score:
                max_score = activity[i]
                best_var = i
    return Literal(best_var)