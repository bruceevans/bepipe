""" Launch CAT
"""

import os
import sys
sys.path.append("D:\\Projects\\GitHub\\bepipe\\src\\")

from PySide2 import QtWidgets
import bepipe.core.qt.themes as themes
import bepipe.tools.cat.core as core

_CAT = None

def run():
    """ Main entry point for CAT
    """
    global _CAT
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(themes.setDark())
    _CAT = core.CAT()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
