from PySide2 import QtCore, QtGui, QtWidgets
from .resources import resources


# This was compiled via qrc
_COLLAPSE_STYLE = """
QGroupBox::indicator:unchecked {
    image: url(:/icons/right.png);
} 

QGroupBox::indicator:checked {
    image: url(:/icons/down.png);
}
"""

class CollapsableGroupBox(QtWidgets.QGroupBox):
    """ Group box widget with collapseable toggle
    """

    def __init__(self, title=None, func=None):
        super(CollapsableGroupBox, self).__init__()

        self.setTitle(title)
        self.func=func

        self.setStyleSheet(_COLLAPSE_STYLE)
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.toggleGroup)
        
    def toggleGroup(self):
        if self.isChecked():
            self.setFixedHeight(self.sizeHint().height())
        else:
            self.setFixedHeight(25)
        if self.func:
            self.func()
