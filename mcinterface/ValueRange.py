class ValueRange:
    def __init__(self, value_type):
        self._type = value_type
        self._values = None

    def __call__(self, arg):
        if isinstance(arg, str):
            arg = arg.replace(' ', '')
            self._values = tuple(map(self._type, arg.split(',')))
        elif isinstance(arg, (tuple, list)):
            self._values = tuple(map(self._type, arg[:2]))
        else:
            raise ValueError
        return self

    @property
    def values(self):
        return self._values

    @property
    def start(self):
        return self._values[0]

    @property
    def end(self):
        return self._values[1]

    def __str__(self):
        return ','.join(map(str, self._values))