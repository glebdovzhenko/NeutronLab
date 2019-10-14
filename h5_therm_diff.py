from mcinterface import H5ThermApp
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = H5ThermApp(dummy=True)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
