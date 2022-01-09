###############################################################################
# THIS CODE IS PART OF BEPIPE, A FREE DIGITAL ART PIPELINE FOR GAMES AND
# ANIMATION. IF YOU BOUGHT THIS SOMEWHERE, OUCH. THIS CODE IS NOT FOR SALE.
# ALL QUESTION AND COMMENTS GO TO BRUCEIN3D@GMAIL.COM. GITHUB REPOSITORY:
###############################################################################


from PySide2 import QtCore, QtGui, QtWidgets
from .resources import resources


__all__ = [
    'BepListWidgetItem',
    'CollapsableGroupBox',
    'bepMessageBox'
    ]


_COLLAPSE_STYLE = """
QGroupBox::indicator:unchecked {
    image: url(:/icons/right.png);
}

QGroupBox::indicator:checked {
    image: url(:/icons/down.png);
}
"""

class BepListWidgetItem(QtWidgets.QListWidgetItem):
    """ List widget item with an addition dict to store asset info
    """

    def __init__(self, assetData):
        super(BepListWidgetItem, self).__init__()
        self.assetData = assetData


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


# TODO don't need this really, just use standard message boxes
def bepMessageBox(title, msg, icon=None, func=None, cancelButton=False):
        """ Base message box to display text and confirm button,
            follow up with an optional function call

            args:
                title (str) : Window title
                msg (str) : body of the message box
                icon (str) : Path to an icon
                func (function) : optional function to call after running
                cancel (bool) : use a cancel button or not
        """

        msgBox = QtWidgets.QMessageBox()
        if icon:
            msgBox.setIcon(QtGui.QIcon(icon))
        else:
            msgBox.setIcon(QtWidgets.QMessageBox.NoIcon)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)

        if cancelButton:
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        else:
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

        result = msgBox.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            if func:
                func()  # TODO may need to pass args as well
            else:
                return True
        else:
            # Hit cancel, don't run the func
            return False
