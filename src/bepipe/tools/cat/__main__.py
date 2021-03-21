""" Launch CAT
"""

import os
import sys
sys.path.append("D:\\Projects\\dev\\packages\\bepipe\\src\\")

from PySide2 import QtWidgets
import bepipe.core.qt.style as style
import bepipe.tools.cat.core as core

_CAT = None

def run():
    """ Main entry point for CAT
    """
    global _CAT
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(style.setDark())
    _CAT = core.CAT()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()


"""
IDEAS:
1. Thumbnails on hover (right-click, 'Create Thumbnail')
    - If using blender preference
2. Startup files (empty project files)
5. Link to docs
6. 'Custom' or 'User' element
7. .bep file and icon
8. Creast asset should be a new window
9. Asset info should be a better panel

QOL:
- Open Recent Project
"""