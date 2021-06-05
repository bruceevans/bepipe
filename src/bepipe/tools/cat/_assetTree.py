

from PySide2 import QtCore, QtGui, QtWidgets

from . utility import _constants

class AssetTree(QtWidgets.QTreeView):
    """ Tree view for the project's assets
    """

    NAME, TYPE, STATUS = range(3)

    def __init__(self):
        super(AssetTree, self).__init__()
        self.model = self._assetModel(self)
        self._setupTreeView()

    def _setupTreeView(self):
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setAllColumnsShowFocus(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.setModel(self.model)
        self._resizeColumns()

        self.header().setStretchLastSection(False)
        self.header().setSectionsMovable(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.header().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)

    def _assetModel(self, parent):
        model = QtGui.QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.NAME, QtCore.Qt.Horizontal, "Name")
        model.setHeaderData(self.TYPE, QtCore.Qt.Horizontal, "Type")
        model.setHeaderData(self.STATUS, QtCore.Qt.Horizontal, "Status")

        return model

    def _resizeColumns(self):
        """ Helper function to resize columns
        """
        colOneWidth = self.frameGeometry().width() - 100
        self.setColumnWidth(0, colOneWidth)
        self.setColumnWidth(1, 75)
        self.setColumnWidth(2, 75)

    def addAssetToTree(self, model, asset, status):
        """ Add an asset to the tree

        Args:
            model (QtGui.QStandardItemModel): Tree's model
            asset (dict): Dict from the project's json file
            status (str): Asset's current P4 status
        """

        # append method
        assetName = QtGui.QStandardItem(asset.get("NAME"))
        assetType = QtGui.QStandardItem(asset.get("TYPE"))
        assetType.setIcon(QtGui.QIcon(_constants.ASSET_ICONS.get(asset.get("TYPE"))))
        assetStatus = QtGui.QStandardItem(asset.get("STATUS") or "NO STATUS")
        model.appendRow([assetName, assetType, assetStatus])
        self._resizeColumns()
