from collections import OrderedDict
import re
import pandas as pd
import io
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema
import numpy as np


class McCodeData(OrderedDict):
    # TODO: make better?
    def __init__(self, *args, **kwargs):
        self._protected = kwargs.keys()
        super().__init__(*args, **kwargs)

    def set_item(self, key, value, **kwargs):
        if key in self._protected:
            return
        if key in self:
            if isinstance(self[key], tuple):
                value = self[key] + (value, )
            else:
                value = (self[key], value)
            del self[key]
        super().__setitem__(key, value, **kwargs)

    def locate(self, partial_key):
        for key in self:
            if partial_key in key:
                return self[key]

    def fill(self, f_name):
        comment = re.compile('\s*#\s*(?P<name>[^:]+)\s*:\s*(?P<value>[^:\n]+)*')

        data = ''
        with open(f_name, 'r') as f:
            for line in f.readlines():
                m = comment.match(line)
                if m:
                    if data:
                        if not self[next(reversed(self))]:
                            self[next(reversed(self))] = pd.read_csv(io.StringIO(data), sep='\s+', header=None)
                        else:
                            self[next(reversed(self))] = pd.read_csv(
                                io.StringIO(self[next(reversed(self))] + '\n' + data), sep='\s+', header=0)
                        data = ''
                    self.set_item(m.group('name'), m.group('value'))
                else:
                    data += line
            if data:
                if not self[next(reversed(self))]:
                    self[next(reversed(self))] = pd.read_csv(io.StringIO(data), sep='\s+', header=None)
                else:
                    self[next(reversed(self))] = pd.read_csv(
                        io.StringIO(self[next(reversed(self))] + '\n' + data), sep='\s+', header=0)

        return self

    def clear(self):
        tmp = OrderedDict()
        for k in self:
            if k in self._protected:
                tmp[k] = self[k]
        super().clear()
        self.update(tmp)

    @property
    def title(self):
        return self['title']

    @property
    def xlabel(self):
        return self['xlabel']

    @property
    def ylabel(self):
        return self['ylabel']


class McColumns(McCodeData):
    def __init__(self, *args, **kwargs):
        for k in('xcolumn', 'ycolumn', 'yerrcolumn'):
            if k not in kwargs:
                kwargs[k] = None
        super().__init__(*args, **kwargs)

    @property
    def xdata(self):
        if self['xcolumn']:
            return self['variables'][self['xcolumn']]
        else:
            return self['variables'].iloc[:, 0]

    @property
    def ydata(self):
        if self['ycolumn']:
            return self['variables'][self['ycolumn']]
        else:
            return self['variables'].iloc[:, 1]

    @property
    def yerrdata(self):
        if self['yerrcolumn']:
            return self['variables'][self['yerrcolumn']]
        else:
            return self['variables'].iloc[:, 2]

    def run_gaussian_fit(self, xy):
        def f(x, *args):
            return args[0] * np.exp(-0.5 * ((x - args[1]) / args[2]) ** 2)

        coord_id = ((self.xdata - xy[0]) ** 2 + (self.ydata - xy[1]) ** 2).idxmin()
        id_mxs, = argrelextrema(np.array(self.ydata), np.greater)
        id_mis, = argrelextrema(np.array(self.ydata), np.less_equal)

        id_max = sorted(id_mxs, key=lambda x: abs(x - coord_id))[0]
        lb = sorted(id_mis, key=lambda x: (id_max - x) if x <= id_max else 10000)[0]
        rb = sorted(id_mis, key=lambda x: (x - id_max) if x >= id_max else 10000)[0]

        dxs = np.array(self.xdata[lb:rb])
        dys = np.array(self.ydata[lb:rb])

        popt, pcov = curve_fit(f, dxs, dys, p0=(dys[id_max - lb], dxs[id_max - lb], 0.5 * (dxs[-1] - dxs[0])))
        print('# Peak 2Theta =', popt[1], '+-', np.sqrt(pcov[1][1]), '  I = ', popt[0], )
        return (np.linspace(self.xdata[lb], self.xdata[rb], 100),
                f(np.linspace(self.xdata[lb], self.xdata[rb], 100), *popt)), popt[1], np.sqrt(pcov[1][1])


class McArray(McCodeData):
    def __init__(self, *args, **kwargs):
        for k in('dataname', 'errname'):
            if k not in kwargs:
                kwargs[k] = None
        super().__init__(*args, **kwargs)
        self['extent'] = ()

    @property
    def data(self):
        if self['dataname']:
            return self[self['dataname']]
        else:
            return self.locate('Data')

    @property
    def err(self):
        if self['errname']:
            return self[self['errname']]
        else:
            return self.locate('Errors')

    @property
    def extent(self):
        return self['extent']

    def fill(self, f_name):
        super().fill(f_name)
        self['extent'] = tuple(map(float, self['xylimits'].split(' ')))
        return self