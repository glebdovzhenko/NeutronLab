import sys
from PyQt5.QtWidgets import QApplication
from mcinterface import H1SansApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = H1SansApp(dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
