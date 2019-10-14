from mcinterface import H2ColdApp
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = H2ColdApp(dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
