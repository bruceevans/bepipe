""" Launch CAT
"""

import os
import sys
sys.path.append("D:\\Projects\\dev\\packages\\bepipe\\src\\")

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


"""
IDEAS:
1. Thumbnails on hover (right-click, 'Create Thumbnail')
    - If using blender preference
2. Startup files (empty project files)
3. When existing asset is selected, asset subpalette becomes 'view more info' palette
5. Link to docs

QOL:
- Open Recent Project
"""