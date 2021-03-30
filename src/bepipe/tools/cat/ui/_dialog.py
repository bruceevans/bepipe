import os
import sys
import enum

import bepipe.core.qt.style as style
import bepipe.core.qt.widgets as bepWidgets

from PySide2 import QtWidgets, QtCore, QtGui

from ..utility import _constants


_SPACER = QtWidgets.QSpacerItem(0, 10)


class CATWindow(QtWidgets.QMainWindow):
    """ Main window wraper for CAT
    """

    def __init__(self):
        super(CATWindow, self).__init__()

        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)

        self.selectedAsset = None
        self.elements = []

        # UI inits
        self.newProject = None
        self.openProject = None
        self.createAsset = None

        self._setupUi()

    def _setupUi(self):
        """ UI initialization
        """

        # top menu
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        createMenu = menuBar.addMenu("&Create")
        prefsMenu = menuBar.addMenu("&Preferences")
        helpMenu = menuBar.addMenu("&Help")

        # menu actions
        self.newProject = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProject)
        self.openProject = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProject)

        # create an asset, show create menu
        self.createNewAsset = QtWidgets.QAction('Create New Asset', self)
        createMenu.addAction(self.createNewAsset)

        # prefs
        #self.usingP4 = QtWidgets.QAction('Use Perforce', self)
        #self.usingP4.setCheckable(True)
        #prefsMenu.addAction(self.usingP4)

        # help
        self.docs = QtWidgets.QAction('Read the Docs', self)
        helpMenu.addAction(self.docs)

        # context menu, logic below
        self.openOnDisk = QtWidgets.QAction("Open on Disk")
        self.openOnDisk.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("disk")))
        self.modifyElements = QtWidgets.QAction("Modify Elements")
        self.modifyElements.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("modify")))
        self.rename = QtWidgets.QAction("Rename Asset") # more involved than you think
        self.rename.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("rename")))
        self.delete = QtWidgets.QAction("Delete Asset")
        self.delete.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("delete")))

        # project info
        projectLabel = QtWidgets.QLabel("Current Project: ")
        self.projectLineEdit = QtWidgets.QLineEdit()
        self.projectLineEdit.setReadOnly(True)
        self.projectLineEdit.setText(_constants.NO_PROJECT)
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

        self.assetInfoGroup = bepWidgets.CollapsableGroupBox("Asset Info: ", func=self.resizeWindow)
        
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

        self.assetInfoGroup.toggleGroup()

    # move to core
    def _connectSignals(self):
        self.assetList.customContextMenuRequested.connect(self.assetContextMenu)

    # move to core
    def _assetContextMenu(self, point):
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

    def resizeWindow(self):
        """ Resize window if asset twirl down is selected
        """
        # TODO This all needs reworked
        if self.assetInfoGroup.isChecked():
            self.setFixedHeight(700)
        else:
            self.setFixedHeight(450)


class CreateAssetWindow(QtWidgets.QDialog):
    """ UI to creat a new asset
    """
    def __init__(self):
        super(CreateAssetWindow, self).__init__()
        self.elements = None
        self._setupUi()

    def _setupUi(self):

        self.setWindowTitle("Create a New Asset")
        self.setWindowIcon(QtGui.QIcon(_constants.WINDOW_ICON))

        mainLayout = QtWidgets.QVBoxLayout()

        newAssetLabel = QtWidgets.QLabel("Asset Name: ")
        self.newAssetLineEdit = QtWidgets.QLineEdit()
        newAssetLayout = QtWidgets.QHBoxLayout()
        newAssetLayout.addWidget(newAssetLabel)
        newAssetLayout.addWidget(self.newAssetLineEdit)
        newAssetLayout.addItem(_SPACER)

        assetTypeLabel = QtWidgets.QLabel("Asset type: ")
        self.assetTypeDropDown = QtWidgets.QComboBox()

        for type in _constants.ASSET_TYPES:
            self.assetTypeDropDown.addItem(QtGui.QIcon(_constants.ASSET_ICONS.get(type)), type)
        assetTypeLayout = QtWidgets.QHBoxLayout()
        assetTypeLayout.addWidget(assetTypeLabel)
        assetTypeLayout.addWidget(self.assetTypeDropDown)
        assetTypeLayout.addItem(_SPACER)

        elementLayout = QtWidgets.QVBoxLayout()
        elementLabel = QtWidgets.QLabel("Choose asset elements:")
        elementLayout.addWidget(elementLabel)

        for element in _constants.ELEMENTS:
            checkBox = QtWidgets.QCheckBox(element)
            checkBox.setChecked(True)
            checkBox.setStatusTip("Create a {} folder relative to the project.".format(element))
            self.elements.append(checkBox)
            elementLayout.addWidget(checkBox)

        self.customElement = QtWidgets.QCheckBox("custom element")
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
        elementLayout.addItem(_SPACER)

        for element in self.elements:
            elementLayout.addWidget(element)

        # TODO connect button in core
        self.btnCreate = QtWidgets.QPushButton("Create Asset")
        self.btnCreate.setEnabled(False)

        self.btnCreate.setStyleSheet(style.GRAY_TEXT)
        self.btnCreate.setFixedHeight(40)

        createAssetGroup = QtWidgets.QGroupBox("Create New Asset: ")
        createAssetLayout = QtWidgets.QVBoxLayout()
        createAssetLayout.addLayout(newAssetLayout)
        createAssetLayout.addLayout(assetTypeLayout)
        createAssetLayout.addLayout(elementLayout)
        createAssetLayout.addWidget(self.btnCreate)

        createAssetGroup.setLayout(createAssetLayout)
        mainLayout.addWidget(createAssetGroup)

        self.setLayout(mainLayout)
        self.setFixedWidth(300)

    def _connectSignals(self):
        self.newAssetLineEdit.textChanged.connect(self._enableCreateButton)
        self.customElement.stateChanged.connect(self._enableCustomElement)

    def _enableCustomElement(self):
        if self.customElement.isChecked():
            self.customElementLineEdit.setReadOnly(False)
            self.customElementLineEdit.setStyleSheet(style.WHITE_TEXT)
            self.customElementLabel.setStyleSheet(style.WHITE_TEXT)
        else:
            self.customElementLineEdit.setReadOnly(True)
            self.customElementLineEdit.setStyleSheet(style.GRAY_TEXT)
            self.customElementLabel.setStyleSheet(style.GRAY_TEXT)

    def _enableCreateButton(self):
        if len(self.newAssetLineEdit.text()) > 3:
            self.btnCreate.setEnabled(True)
        else:
            self.btnCreate.setEnabled(False)
