import os
import sys
import enum
from collections import OrderedDict

from PySide2 import QtWidgets, QtCore, QtGui

import bepipe.core.qt.style as style
from bepipe.core.qt.bepListWidgetItem import BepListWidgetItem
from bepipe.core.qt.collapsableGroupBox import CollapsableGroupBox

# TODO think of some sort of setting system
# TODO icon factory


_FILE_DIRECTORY = os.path.join(os.path.dirname(__file__))
_WINDOW_ICON = os.path.join(_FILE_DIRECTORY, "resources/icons/icon_CAT.png")
_MENU_ICONS = {
    'disk': os.path.join(_FILE_DIRECTORY, "resources/icons/disk.png"),
    'modify': os.path.join(_FILE_DIRECTORY, "resources/icons/modify.png"),
    'rename': os.path.join(_FILE_DIRECTORY, "resources/icons/rename.png"),
    'delete': os.path.join(_FILE_DIRECTORY, "resources/icons/delete.png")
}
_SPACER = QtWidgets.QSpacerItem(0, 10)
_ELEMENTS = ["Animation", "Lighting", "Maps", "Mesh", "Output", "Reference", "Rig", "Sculpt"]

ASSET_ICONS = {
    'char': os.path.join(_FILE_DIRECTORY, 'resources/icons/char.png'),
    'environment': os.path.join(_FILE_DIRECTORY, 'resources/icons/environment.png'),
    'prop': os.path.join(_FILE_DIRECTORY, 'resources/icons/prop.png'),
    'vfx': os.path.join(_FILE_DIRECTORY, 'resources/icons/vfx.png')
}

ASSET_TYPES = ['char', 'environment', 'prop', 'vfx']

NO_PROJECT = "Open a project or create a new one."

# TODO get starter files for different projects


class Mode(enum.Enum):
    Create = 1
    Edit = 2


class CATWindow(QtWidgets.QMainWindow):
    """ Main window wrapper for CAT
    """

    close = QtCore.Signal()

    def __init__(self):
        super(CATWindow, self).__init__()

        self.icon = QtGui.QIcon(_WINDOW_ICON)
        self.elements = []
        self.selectedAsset = None

        self._setupUi()
        self._connectSignals()

    def _setupUi(self):
        """ UI Initialization
        """

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        createMenu = menuBar.addMenu("&Create")
        prefsMenu = menuBar.addMenu("&Preferences")
        helpMenu = menuBar.addMenu("&Help")
        self.statusBar()

        # Menu actions
        self.newProjectAction = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProjectAction)
        self.openProjectAction = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProjectAction)

        # create an asset, show create menu
        self.createNewAssetAction = QtWidgets.QAction('Create New Asset', self)
        self.createNewAssetAction.triggered.connect(self.createAssetWindow)
        createMenu.addAction(self.createNewAssetAction)

        # prefs
        self.usingP4 = QtWidgets.QAction('Use Perforce', self)
        self.usingP4.setCheckable(True)
        prefsMenu.addAction(self.usingP4)

        # help
        self.docs = QtWidgets.QAction('Read the Docs', self)
        helpMenu.addAction(self.docs)

        # context menu, logic below
        self.openOnDisk = QtWidgets.QAction("Open on Disk")
        self.openOnDisk.setIcon(QtGui.QIcon(_MENU_ICONS.get("disk")))
        self.modifyElements = QtWidgets.QAction("Modify Elements")
        self.modifyElements.setIcon(QtGui.QIcon(_MENU_ICONS.get("modify")))
        self.rename = QtWidgets.QAction("Rename Asset") # more involved than you think
        self.rename.setIcon(QtGui.QIcon(_MENU_ICONS.get("rename")))
        self.delete = QtWidgets.QAction("Delete Asset")
        self.delete.setIcon(QtGui.QIcon(_MENU_ICONS.get("delete")))

        # project info
        projectLabel = QtWidgets.QLabel("Current Project: ")
        self.projectLineEdit = QtWidgets.QLineEdit()
        self.projectLineEdit.setReadOnly(True)
        self.projectLineEdit.setText(NO_PROJECT)
        self.projectLineEdit.setStyleSheet(style.GRAY_TEXT)
        self.projectLineEdit.setStatusTip("Use 'File' > 'New' to create a new project or 'File' > 'Open' to open")
        projectTitleLayout = QtWidgets.QHBoxLayout()
        projectTitleLayout.addWidget(projectLabel)
        projectTitleLayout.addWidget(self.projectLineEdit)

        self.assetGroup = QtWidgets.QGroupBox("Existing Assets:")

        self.assetList = QtWidgets.QListWidget()
        self.assetList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.assetList.setIconSize(QtCore.QSize(16, 16))
        self.assetList.setSortingEnabled(True)
        self.assetList.setAlternatingRowColors(True)
        self.assetList.setSelectionMode(QtWidgets.QListWidget.SingleSelection)

        assetLayout = QtWidgets.QVBoxLayout()
        assetLayout.addWidget(self.assetList)
        self.assetGroup.setLayout(assetLayout)

        self.assetInfoGroup = CollapsableGroupBox("Asset Info: ", func=self.resizeWindow)
        
        # Init with no aset
        self.assetInfoLayout = QtWidgets.QVBoxLayout()

        titleLayout = QtWidgets.QHBoxLayout()
        self.assetTitle = QtWidgets.QLabel("Asset: {}".format("Select an asset"))
        self.assetType = QtWidgets.QLabel("Type: {}".format(" "))
        titleLayout.addWidget(self.assetTitle)
        titleLayout.addWidget(self.assetType)

        elementLabel = QtWidgets.QLabel("Elements: ")
        self.assetElements = QtWidgets.QListWidget()
        self.modifyButton = QtWidgets.QPushButton("Modify Asset")
        self.modifyButton.setFixedHeight(40)
        # TODO gray unless asset is selected

        self.assetInfoLayout.addLayout(titleLayout)
        self.assetInfoLayout.addWidget(elementLabel)
        self.assetInfoLayout.addWidget(self.assetElements)
        self.assetInfoLayout.addWidget(self.modifyButton)

        self.assetInfoGroup.setLayout(self.assetInfoLayout)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addLayout(projectTitleLayout)
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addWidget(self.assetGroup)
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addWidget(self.assetInfoGroup)
        self.mainLayout.addItem(_SPACER)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("CAT by Be")
        self.setWindowIcon(self.icon)
        self.setFixedWidth(400)
        self.setFixedHeight(450)

        self.mode = Mode.Create
        self.assetInfoGroup.toggleGroup()

        self.show()

    def _connectSignals(self):
        self.assetList.customContextMenuRequested.connect(self.assetContextMenu)

    def _customElementReadOnly(self):
        if self.customElement.isChecked():
            self.customElementLineEdit.setReadOnly(False)
            self.customElementLineEdit.setStyleSheet(style.WHITE_TEXT)
            self.customElementLabel.setStyleSheet(style.WHITE_TEXT)
        else:
            self.customElementLineEdit.setReadOnly(True)
            self.customElementLineEdit.setStyleSheet(style.GRAY_TEXT)
            self.customElementLabel.setStyleSheet(style.GRAY_TEXT)

    def assetContextMenu(self, point):
        """ Context menu actions for created assets
        """

        asset = self.assetList.indexAt(point)
        if not asset:
            return

        # make it available to core
        self.contextAssetIndex = asset
        menu = QtWidgets.QMenu()

        menu.addAction(self.openOnDisk)
        menu.addAction(self.modifyElements)
        menu.addAction(self.rename)
        menu.addAction(self.delete)

        menu.exec_(self.assetList.mapToGlobal(point))

    def createAssetWindow(self):
        """ Dialog for creating a new asset
        """

        # TODO probably don't need all the selfs
        # Force on top
        # Window icon
        # Element icon?

        self.createMenu = QtWidgets.QDialog()
        self.createMenu.setWindowTitle("Create a New Asset")
        self.createMenu.setWindowIcon(QtGui.QIcon(_WINDOW_ICON))
        mainLayout = QtWidgets.QVBoxLayout()

        self.newAssetLabel = QtWidgets.QLabel("Asset Name: ")
        self.newAssetLineEdit = QtWidgets.QLineEdit()
        newAssetLayout = QtWidgets.QHBoxLayout()
        newAssetLayout.addWidget(self.newAssetLabel)
        newAssetLayout.addWidget(self.newAssetLineEdit)
        newAssetLayout.addItem(_SPACER)

        assetTypeLabel = QtWidgets.QLabel("Asset type: ")
        self.assetTypeDropDown = QtWidgets.QComboBox()
        for type in ASSET_TYPES:
            self.assetTypeDropDown.addItem(QtGui.QIcon(ASSET_ICONS.get(type)), type)
        assetTypeLayout = QtWidgets.QHBoxLayout()
        assetTypeLayout.addWidget(assetTypeLabel)
        assetTypeLayout.addWidget(self.assetTypeDropDown)
        assetTypeLayout.addItem(_SPACER)

        elementLayout = QtWidgets.QVBoxLayout()
        elementLayout.addItem(_SPACER)
        elementLabel = QtWidgets.QLabel("Choose asset elements:")

        for element in _ELEMENTS:
            checkbox = QtWidgets.QCheckBox(element)
            checkbox.setChecked(True)
            self.elements.append(checkbox)

        elementLayout.addWidget(elementLabel)
        elementLayout.addItem(_SPACER)

        for element in self.elements:
            elementLayout.addWidget(element)

        self.btnCreate = QtWidgets.QPushButton("Create Asset")
        self.btnCreate.setEnabled(False)
        self.btnCreate.setStyleSheet(style.GRAY_TEXT)
        self.btnCreate.setFixedHeight(40)

        # self.createAssetGroup = CollapsableGroupBox("Create New Asset", func=self.resizeWindow)
        self.createAssetGroup = QtWidgets.QGroupBox("Create New Asset: ")
        createAssetLayout = QtWidgets.QVBoxLayout()
        createAssetLayout.addLayout(newAssetLayout)
        createAssetLayout.addLayout(assetTypeLayout)
        createAssetLayout.addLayout(elementLayout)
        createAssetLayout.addWidget(self.btnCreate)

        self.createAssetGroup.setLayout(createAssetLayout)
        mainLayout.addWidget(self.createAssetGroup)

        self.createMenu.setLayout(mainLayout)
        self.createMenu.show()

        # TODO pack this data into a dict and return on create

    def createElementsWidget(self):

        elementLayout = QtWidgets.QVBoxLayout()
        elementLabel = QtWidgets.QLabel("Choose asset elements:")
        elementLayout.addWidget(elementLabel)

        for element in _ELEMENTS:
            checkBox = QtWidgets.QCheckBox(element)
            checkBox.setChecked(True)
            checkBox.setStatusTip("Create a {} folder relative to the project.".format(element))
            self.elements.append(checkBox)
            elementLayout.addWidget(checkBox)

        self.customElement = QtWidgets.QCheckBox("custom element")
        self.customElement.stateChanged.connect(self._customElementReadOnly)
        self.customElement.setChecked(False)
        customElementLayout = QtWidgets.QHBoxLayout()
        self.customElementLabel = QtWidgets.QLabel("Element name: ")
        # custom line edit won't be included in the index, 
        # but can be edited directly
        self.customElementLineEdit = QtWidgets.QLineEdit()
        customElementLayout.addWidget(self.customElementLabel)
        customElementLayout.addWidget(self.customElementLineEdit)
        elementLayout.addWidget(self.customElement)
        elementLayout.addLayout(customElementLayout)

        # init the custom box
        self._customElementReadOnly()

        return elementLayout

    def resizeWindow(self):
        """ Resize window if asset twirl down is selected
        """
        if self.assetInfoGroup.isChecked():
            # TODO calculate window size
            self.setFixedHeight(700)
        else:
            self.setFixedHeight(450)

    def closeEvent(self, event):
        # connect close signal
        self.close.emit()
        event.accept()
