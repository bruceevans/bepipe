from PySide2 import QtWidgets, QtGui, QtCore


class AssetList(QtWidgets.QTableView):
    """ Two column sortable asset viewer
    """

    def __init__(self):
        super(AssetList, self).__init__()


class AssetModel(QtCore.QAbstractTableModel):
    def __init__(self, data, header, *args):
        super(AssetModel, self).__init__()
        self._data = data
        self._header = header

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.colum()]

    def rowCount(self):
        return len(self.dataList)

    def columnCount(self, index):
        return len(self._data[0])