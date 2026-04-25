


class Literal(int):
    _pool = {}

    def __new__(cls, id):
        if id not in cls._pool:
            instance = super().__new__(cls, id)
            instance._watched_in = []

            cls._pool[id] = instance

        return cls._pool[id]

    @classmethod
    def clear_pool(cls):
        cls._pool.clear()

    @property
    def id(self):
        return int(self)

    @property
    def neg(self):
        return Literal(-self)

    @property
    def sgn(self):
        if self < 0:
            return False
        else:
            return True

    @property
    def var(self):
        return abs(self)

    @property
    def watched_in(self):
        return self._watched_in

    def add_watched_in(self, clause):
        if clause not in self._watched_in:
            self._watched_in.append(clause)