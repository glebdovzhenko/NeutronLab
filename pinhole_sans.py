from mcinterface import PinholeSansApp
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = PinholeSansApp(dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())

