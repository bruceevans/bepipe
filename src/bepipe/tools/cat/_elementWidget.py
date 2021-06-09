
from PySide2 import QtCore, QtGui, QtWidgets

from . utility import _constants
from . dialog import _simpleTreeView

class ElementWidget(QtWidgets.QWidget):
    """ Widget containing an element list and
    info about the file status from perforce
    """

    # TODO use the list view's on selected signal

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.setFixedHeight(100)
        self.layout = None

        # self.selectedElement = None

        # temp for formatting currently
        self.assetName = "ASSET"
        self.perforceStatus = ""
        self.elementName = "Element"
        self.createdBy = "Bevans"
        self.createdDate = "00/00/00"
        self.updatedBy = "Bevans"
        self.updatedDate = "00/00/00"

        self._setupUi()
        self.setFixedHeight(200)

        # self.setEnabled(False)

    def _setupUi(self):

        # Text status info #

        self.layout = QtWidgets.QHBoxLayout()
        self.thumbnail = QtGui.QPixmap(_constants.CAT_THUMBNAIL)
        self.thumbnailLabel = QtWidgets.QLabel("")
        self.thumbnailLabel.setPixmap(self.thumbnail)

        self.nameLabel = QtWidgets.QLabel(self.assetName)  # BIG
        self.nameLabel.setFont(QtGui.QFont('Calibri', 12, QtGui.QFont.Bold))

        self.elementLabel = QtWidgets.QLabel(self.elementName)  # big
        self.elementLabel.setFont(QtGui.QFont('Calibri', 11, QtGui.QFont.Bold))

        self.createdByLabel = QtWidgets.QLabel("Created By: {}".format(self.createdBy))  # small
        self.createDateLabel = QtWidgets.QLabel("Created On: {}".format(self.createdDate))

        self.updatedByLabel = QtWidgets.QLabel("Last Updated By: {}".format(self.updatedBy))
        self.updatedLabel = QtWidgets.QLabel("Last Updated On: {}".format(self.updatedDate))

        textStatus = QtWidgets.QVBoxLayout()
        textStatus.addWidget(self.nameLabel)
        textStatus.addWidget(self.elementLabel)

        textStatus.addWidget(self.updatedByLabel)
        textStatus.addWidget(self.updatedLabel)

        textStatus.addWidget(self.createdByLabel)
        textStatus.addWidget(self.createDateLabel)

        # self.layout.addLayout(textStatus, stretch=0)

        elementListLayout = QtWidgets.QVBoxLayout()
        elementGroup = QtWidgets.QGroupBox("Elements")
        # elementList = QtWidgets.QListView()
        self.elementTree = ElementTree()
        elementListLayout.addWidget(self.elementTree)
        elementGroup.setLayout(elementListLayout)

        self.layout.addWidget(elementGroup)

        statusGroup = QtWidgets.QGroupBox("Element Status")
        statusGroupLayout = QtWidgets.QHBoxLayout()
        statusGroupLayout.addLayout(textStatus)
        statusGroupLayout.addWidget(self.thumbnailLabel)
        statusGroup.setLayout(statusGroupLayout)

        # self.layout.addLayout(textStatus, stretch=0)
        # self.layout.addWidget(self.thumbnailLabel)
        self.layout.addWidget(statusGroup)

        self.setLayout(self.layout)

    # connect

    # refresh


class ElementTree(_simpleTreeView.SimpleTree):

    ELEMENT, STATUS = range(2)

    def __init__(self):
        super(ElementTree, self).__init__("Elements", "Status")

    def addElementToTree(self, element, status, path):

        elementColumn = QtGui.QStandardItem(element)
        # TODO set data as the path
        statusColumn = QtGui.QStandardItem("")
        statusColumn.setIcon(QtGui.QIcon(_constants.P4_ICONS.get(status)))

        self.model.appendRow([elementColumn, statusColumn])