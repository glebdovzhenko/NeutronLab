class GUIParameter:
    def __init__(self, gui_name, sim_name, data_type, value=None, values=None, value_names=None, vr_name=''):
        self._gui_name = gui_name
        self._sim_name = sim_name
        self._type = data_type
        self._value = None
        self.vr_name = vr_name

        if (values is not None) and (value_names is not None) and (len(value_names) != len(values)):
            raise ValueError()

        self._values = values
        self._value_names = value_names
        if (values is not None) and (value_names is None):
            self._value_names = tuple(map(str, values))
        self.update(value)

    def check(self, new_value):
        if self._values is not None:
            return new_value in self._values
        else:
            # TODO: implement
            return True

    def update(self, *args):
        new_val = self._type(args[0])
        if self.check(new_val):
            self._value = new_val
            print('# ' + self.gui_name + ' updated to ' + self.__str__())
        else:
            raise ValueError()

    def update_by_name(self, *args):
        if args[0] in self._value_names:
            self.update(self.values[self.value_names.index(args[0])])
        else:
            raise ValueError()

    @property
    def console_repr(self):
        return self._sim_name + '=' + self._value.__str__()

    @property
    def value(self):
        return self._value

    @property
    def values(self):
        return self._values

    @property
    def value_names(self):
        return self._value_names

    @property
    def sim_name(self):
        return self._sim_name

    @property
    def gui_name(self):
        return self._gui_name

    @property
    def dtype(self):
        return self._type

    def __int__(self):
        return self._value.__int__()

    def __float__(self):
        return self._value.__float__()

    def __str__(self):
        if self._value_names is None:
            return self._value.__str__()
        else:
            return self._value_names[self._values.index(self._value)].__str__()