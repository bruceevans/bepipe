import os
import sys

# sys.path.append("D:\\dev\\packages\\bepipe\\src\\")
sys.path.append("/Users/bevans/Documents/_dev/git/bepipe/src/")

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
# Check in project file on exit
# Populate the version dropdown
# Add version support to BP4
# Tie perforce status to element icons
# Recent projects
# Open to last opened directory
# Launch element in DCC app
# Add 'Create Animation' to create menu
    # - only on animation elements
    # - duplicate?


# TODO STRETCH GOALS
# Settings for choosing DCC apps
# Settings for perforce
