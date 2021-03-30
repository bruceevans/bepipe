from PySide2 import QtWidgets, QtGui

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