
from PySide2 import QtCore, QtGui, QtWidgets

from .. utility import _constants


class CreateAssetDialog(QtWidgets.QDialog):

    def __init__(self):
        super(CreateAssetDialog, self).__init__()

        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)
        self._setupUi()
        self._connectSignals()

    def _setupUi(self):
        """ UI Init
        """
        layout = QtWidgets.QVBoxLayout()

        nameLabel = QtWidgets.QLabel("Name: ")
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setPlaceholderText("Enter a name for your asset.")
        layout.addWidget(nameLabel)
        layout.addWidget(self.nameLineEdit)

        assetTypeLabel = QtWidgets.QLabel("Asset type: ")
        self.assetTypeDrop = QtWidgets.QComboBox()
        for assetType in _constants.ASSET_TYPES:
            self.assetTypeDrop.addItem(
                QtGui.QIcon(_constants.ASSET_ICONS.get(assetType)), assetType)
        layout.addWidget(assetTypeLabel)
        layout.addWidget(self.assetTypeDrop)

        checkboxGroup = QtWidgets.QGroupBox("Elements")
        elementLayout = QtWidgets.QVBoxLayout()
        elementLabel = QtWidgets.QLabel("Choose asset elements:")
        elementLayout.addWidget(elementLabel)
        self.elements = []
        for element in _constants.ELEMENTS:
            checkBox = QtWidgets.QCheckBox(element)
            checkBox.setChecked(True)
            checkBox.setStatusTip("Create a {} folder relative to the project.".format(element))
            self.elements.append(checkBox)
            elementLayout.addWidget(checkBox)
        checkboxGroup.setLayout(elementLayout)
        layout.addWidget(checkboxGroup)

        self.createButton = QtWidgets.QPushButton("Create Asset")
        self.createButton.setFixedHeight(40)
        self.createButton.setEnabled(False)
        layout.addWidget(self.createButton)
        
        self.setLayout(layout)
        self.setFixedWidth(300)
        self.setWindowTitle("Create a New Asset")
        self.setWindowIcon(QtGui.QIcon(_constants.WINDOW_ICON))

    def _connectSignals(self):
        self.nameLineEdit.textChanged.connect(self._enableCreateButton)

    def _enableCreateButton(self):
        if len(self.nameLineEdit.text()) > 3:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def reset(self):
        """ Reset all widgets
        """

        # name label
        # elements
        # disable button
        # hide