
from PySide2 import QtCore, QtGui, QtWidgets

from .import _simpleTreeView
from ..api import _constants

class AssetTree(_simpleTreeView.SimpleTree):
    """ Tree view for the project's assets
    """

    # TODO onSelected Signal for the element list

    def __init__(self):
        super(AssetTree, self).__init__("Name", "Type", movable=True)
        self._resizeColumns()
        self.selectedAsset = None

    def _resizeColumns(self):
        """ Helper function to resize columns
        """
        # colOneWidth = self.frameGeometry().width() - 100
        #self.setColumnWidth(0, colOneWidth)
        self.setColumnWidth(1, 150)
        # self.setColumnWidth(2, 100)

    def addAssetToTree(self, model, asset):
        """ Add an asset to the tree

        Args:
            model (QtGui.QStandardItemModel): Tree's model
            asset (dict): Dict from the project's json file
            status (str): Asset's current P4 status
        """

        # TODO wrap standard item with some extra info that can populate the elements widget

        assetName = QtGui.QStandardItem(asset.get("NAME"))
        # data will be stored in the asset name
        assetName.setData(asset)
        assetType = QtGui.QStandardItem(asset.get("TYPE"))
        assetType.setIcon(QtGui.QIcon(_constants.ASSET_ICONS.get(asset.get("TYPE"))))
        # TODO tooltip
        model.appendRow([assetName, assetType])
        
        self._resizeColumns()

    def getTableItem(self, row, column):
        return self.model.item(row, column)

    # TODO remove row?
    def removeAssetFromTree(self, row):
        """Remove the row from the asset tree"""
