
# File to hold some general Qt StyleSheet

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor

GRAY_TEXT = "color: rgb(150, 150, 150)"
WHITE_TEXT = "color: rgb(255, 255, 255)"
RED_TEXT = "color: rgc(220, 20, 20)"
GREEN_TEXT = "color: rgb(20, 220, 20)"
BLUE_TEXT = "color: rgb(20, 20, 220)"


def setDark():

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)

    return dark_palette