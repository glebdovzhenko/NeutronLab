import sys
from PyQt5.QtWidgets import QApplication
from mcinterface import MainApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = MainApp(dummy=True)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
