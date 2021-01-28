
import os
import sys

from PySide2 import QtWidgets

modulePath = os.path.dirname(os.path.abspath(__file__)).split('bepipe\\tools')[0]
sys.path.append(modulePath)

import bepipe.core.qt.themes as themes
from core import BeLauncher

_LAUNCHER = None
def run(windowed=True):
    """ Main entry point for BeLauncher
    """

    global _LAUNCHER

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setStyle('Fusion')
    app.setPalette(themes.setDark())
    _LAUNCHER = BeLauncher()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
