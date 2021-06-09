from PySide2 import QtCore, QtGui, QtWidgets

class SimpleTree(QtWidgets.QTreeView):
    """ Two column tree view with basic settings for CAT """

    COLONE, COLTWO = range(2)

    def __init__(self, columnOne, columnTwo, movable=False):
        super(SimpleTree, self).__init__()
        self.columnOne = columnOne
        self.columnTwo = columnTwo
        self.movable = movable
        self.model = self._model(self)

        self._setupTreeView()

    def _setupTreeView(self):
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setAllColumnsShowFocus(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setModel(self.model)
        self.header().setSectionsMovable(self.movable)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)

    def _model(self, parent):
        model = QtGui.QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.COLONE, QtCore.Qt.Horizontal, " {}".format(self.columnOne))
        model.setHeaderData(self.COLTWO, QtCore.Qt.Horizontal, " {}".format(self.columnTwo))

        return model

    """
    # implement this in child class
    def _addElementToTree(self, model, element):
        # assetName = QtGui.QStandardItem(asset.get("NAME"))
        # assetType = QtGui.QStandardItem(asset.get("TYPE"))
        # assetType.setIcon(QtGui.QIcon(_constants.ASSET_ICONS.get(asset.get("TYPE"))))

        elementName = "maps"
        status = "Local"

        model.appendRow([elementName, status])
    """
    