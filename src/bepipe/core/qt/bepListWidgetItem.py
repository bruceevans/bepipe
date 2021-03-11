from PySide2 import QtCore, QtGui, QtWidgets

class BepListWidgetItem(QtWidgets.QListWidgetItem):
    """ List widget item with an addition dict to store asset info
    """

    def __init__(self, assetData):
        super(BepListWidgetItem, self).__init__()
        self.assetData = assetData