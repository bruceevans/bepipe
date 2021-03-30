import os
import sys
sys.path.append("D:\\Projects\\dev\\packages\\bepipe\\src\\")

from PySide2 import QtWidgets
import bepipe.core.qt.style as style
import bepipe.tools.cat.cat as cat

_CAT = None

def run():
    """ Main entry point for CAT
    """
    global _CAT
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(style.setDark())
    _CAT = cat.CAT()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()