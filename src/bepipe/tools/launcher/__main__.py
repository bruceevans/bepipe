
import sys

from PySide2 import QtWidgets
from .core import BeLauncher

_LAUNCHER = None
def run(windowed=True):
    """ Main entry point for BeLauncher
    """

    global _LAUNCHER
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    # app.setWindowIcon()

    _LAUNCHER = BeLauncher()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()

