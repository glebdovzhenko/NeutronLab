from mcinterface import H8StressApp
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pinhole_sans_app = H8StressApp(dummy=False)
    pinhole_sans_app.show()
    sys.exit(app.exec_())
