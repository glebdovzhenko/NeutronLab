import numpy as np
from matplotlib import pyplot as plt
from mcinterface import McArray, McColumns


if __name__ == '__main__':
    sans2d = McArray().fill('PSDMonitor.dat')
    sans1d = McColumns().fill('QDetector.dat')
    tas_scan = McColumns(xcolumn='an_angle', ycolumn='befanL_I', yerrcolumn='befanL_ERR',
                         title='Angle scan', xlabel='An angle [deg]', ylabel='Integral intensity')
    diff_res = McColumns().fill('detector.dat')
    tas_scan.fill('mccode.dat')

    plt.figure()
    plt.subplot(121)
    plt.title('Log ' + sans2d.title)
    plt.xlabel(sans2d.xlabel)
    plt.ylabel(sans2d.ylabel)
    plt.imshow(np.log(sans2d.data), extent=sans2d.extent)

    plt.subplot(122)
    plt.title(sans2d.title + ' Err')
    plt.xlabel(sans2d.xlabel)
    plt.ylabel(sans2d.ylabel)
    plt.imshow(sans2d.err, extent=sans2d.extent)

    plt.tight_layout()

    plt.figure()
    plt.subplot(121)
    plt.title(sans1d.title)
    plt.xlabel(sans1d.xlabel)
    plt.ylabel(sans1d.ylabel)
    plt.errorbar(sans1d.xdata, sans1d.ydata, yerr=sans1d.yerrdata)
    ax = plt.subplot(122)
    plt.title(sans1d.title)
    plt.xlabel(sans1d.xlabel)
    plt.ylabel(sans1d.ylabel)
    plt.errorbar(sans1d.xdata, sans1d.ydata, yerr=sans1d.yerrdata)
    ax.set_yscale('log', nonposy='clip')

    plt.tight_layout()

    plt.figure()
    plt.subplot(111)
    plt.title(tas_scan.title)
    plt.xlabel(tas_scan.xlabel)
    plt.ylabel(tas_scan.ylabel)
    plt.errorbar(tas_scan.xdata, tas_scan.ydata, yerr=tas_scan.yerrdata)

    plt.figure()
    plt.subplot(111)
    plt.title(diff_res.title)
    plt.xlabel(diff_res.xlabel)
    plt.ylabel(diff_res.ylabel)
    plt.errorbar(diff_res.xdata, diff_res.ydata, yerr=diff_res.yerrdata)

    plt.show()