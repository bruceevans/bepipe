from PySide2 import QtCore, QtGui, QtWidgets
from .resources import resources

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

    resized = QtCore.Signal()

    def __init__(self, title=None, func=None):
        super(CollapsableGroupBox, self).__init__()

        self.setTitle(title)
        self.func=func

        self.setStyleSheet(_COLLAPSE_STYLE)
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.toggleGroup)
        
    def toggleGroup(self):
        self.resized.emit()
        if self.isChecked():
            self.setFixedHeight(self.sizeHint().height())
        else:
            self.setFixedHeight(30)
        if self.func:
            self.func()
