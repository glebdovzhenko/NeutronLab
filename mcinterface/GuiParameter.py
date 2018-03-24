class GUIParameter:
    def __init__(self, gui_name, sim_name, data_type, value=None):
        self._gui_name = gui_name
        self._sim_name = sim_name
        self._type = data_type
        self._value = None
        self.update(value)

    def check(self, new_value):
        # TODO: implement
        return True

    def update(self, *args):
        new_val = self._type(args[0])
        if self.check(new_val):
            self._value = new_val
            print('# ' + self.gui_name + ' updated to ' + self.__str__())
        else:
            raise ValueError()

    @property
    def console_repr(self):
        return self._sim_name + '=' + self.__str__()

    @property
    def value(self):
        return self._value

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
        return self._value.__str__()