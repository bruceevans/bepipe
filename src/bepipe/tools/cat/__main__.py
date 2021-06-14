import os
import sys
sys.path.append("D:\\dev\\packages\\bepipe\\src\\")

from PySide2 import QtWidgets

import bepipe.core.qt.style as style
import bepipe.tools.cat.ui as ui

_CAT = None

def run():
    """ Main entry point for CAT
    """
    global _CAT
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(style.setDark())
    _CAT = ui.CATWindow()
    _CAT.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()

# TODO
# Create Asset
# Copy starter project files over for each dcc
