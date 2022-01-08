
import os
from pprint import pprint

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.qt.style as style

from .api import cat
from .api import _settings
from .api import _constants
from .dialog import _assetTree
from .dialog import _elementWidget
from .dialog import _createAssetDialog


# TODO move to widgets module
_SPACER = QtWidgets.QSpacerItem(0, 10)


class CATWindow(QtWidgets.QMainWindow):
    """ Main gui for CAT
    """

    def __init__(self):
        super(CATWindow, self).__init__()

        self._CAT_API = cat.CAT()
        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)

        # Name of the project
        self.project = None
        # Name of the project file
        self.projectFile = None
        # Path to the local project file
        self.projectPath = None
        # Path to the project folder
        self.projectDirectory = None
        # Config dictionary
        self.config = {}

        self.selectedAsset = None
        self.selectedElement = None
        self.createAssetWindow = _createAssetDialog.CreateAssetDialog()

        self._setupUi()
        self._connectWidgets()

    def _setupUi(self):
        """ UI initialization
        """

        # Menu bar #

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        createMenu = menuBar.addMenu("&Create")
        perforceMenu = menuBar.addMenu('&Perforce')
        # prefsMenu = menuBar.addMenu("&Preferences")
        helpMenu = menuBar.addMenu("&Help")

        # Menu actions #

        self.newProject = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProject)
        self.openProject = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProject)
        self.openRecentProjects = QtWidgets.QAction('Open Recent', self)
        fileMenu.addAction(self.openRecentProjects)

        self.createNewAsset = QtWidgets.QAction('Create New Asset', self)
        createMenu.addAction(self.createNewAsset)

        self.perforceInfo = QtWidgets.QAction('View Connection', self)
        perforceMenu.addAction(self.perforceInfo)

        self.readDocs = QtWidgets.QAction('Read the Docs', self)
        helpMenu.addAction(self.readDocs)
        self.about = QtWidgets.QAction('About', self)
        helpMenu.addAction(self.about)

        # Status Bar #

        self.statusBar()

        # Project info #

        projectLabel = QtWidgets.QLabel("Current Project: ")
        self.projectLineEdit = QtWidgets.QLineEdit()
        self.projectLineEdit.setReadOnly(True)
        self.projectLineEdit.setText(_constants.NO_PROJECT)
        self.projectLineEdit.setStyleSheet(style.GRAY_TEXT)
        self.projectLineEdit.setStatusTip("Use 'File' > 'New' to create a new project or 'File' > 'Open' to open")
        projectTitleLayout = QtWidgets.QHBoxLayout()
        projectTitleLayout.addWidget(projectLabel)
        projectTitleLayout.addWidget(self.projectLineEdit)

        # Asset List #

        self.assetGroup = QtWidgets.QGroupBox("Existing Assets")
        assetLayout = QtWidgets.QVBoxLayout()
        self.assetTree = _assetTree.AssetTree()
        self.assetTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        assetLayout.addWidget(self.assetTree)
        self.assetGroup.setLayout(assetLayout)

        self.elementWidget = _elementWidget.ElementWidget()
        self.elementWidget.show()

        versionLayout = QtWidgets.QHBoxLayout()
        self.versionDropDown = QtWidgets.QComboBox()
        self.versionDropDown.setFixedHeight(30)
        self.historyButton = QtWidgets.QPushButton("View History")
        self.historyButton.setFixedHeight(30)
        versionLayout.addWidget(self.versionDropDown)
        versionLayout.addWidget(self.historyButton)

        perforceButtonLayout = QtWidgets.QHBoxLayout()
        self.getLatestButton = QtWidgets.QPushButton("Get Latest Element")
        # TODO tooltips
        self.getLatestButton.setFixedHeight(40)
        perforceButtonLayout.addWidget(self.getLatestButton)
        self.checkOutButton = QtWidgets.QPushButton("Check Out Element")
        self.checkOutButton.setFixedHeight(40)
        perforceButtonLayout.addWidget(self.checkOutButton)
        self.checkInButton = QtWidgets.QPushButton("Check In Element")
        self.checkInButton.setFixedHeight(40)
        perforceButtonLayout.addWidget(self.checkInButton)

        self.openButtonText = "Open Element in {}".format("DCC")
        self.openButton = QtWidgets.QPushButton(self.openButtonText)  # hide until element is selected
        self.openButton.setFixedHeight(40)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addLayout(projectTitleLayout)
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addWidget(self.assetGroup)
        self.mainLayout.addWidget(self.elementWidget)
        self.mainLayout.addLayout(versionLayout)
        self.mainLayout.addLayout(perforceButtonLayout)
        self.mainLayout.addWidget(self.openButton)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("CAT by Be")
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(600)
        self.setMinimumHeight(650)

    def _connectWidgets(self):
        """ Connect slots and signals
        """

        # Menus

        self.newProject.triggered.connect(self._createNewProject)
        self.openProject.triggered.connect(self._openExistingProject)
        self.createNewAsset.triggered.connect(self._showCreateAssetWindow)
        # viewConnection
        # readDocs
        self.assetTree.customContextMenuRequested.connect(self._contextMenu)
        self.assetTree.clicked.connect(self._onAssetChanged)
        self.elementWidget.elementTree.clicked.connect(self._onElementChanged)

        self.createAssetWindow.createButton.clicked.connect(self._createAsset)

    ##### UI Functions #####

    def _contextMenu(self, point):
        """ Context menu for main tree view
        """

        # make this a parameter?
        asset = self.assetTree.indexAt(point)  # gives a qmodelindex (-1, -1), (0, 1), etc.

        if asset.column() == -1 or asset.row() == -1:
            return
        
        # TODO lambdas to tie things together
        menu = QtWidgets.QMenu()

        openOnDisk = QtWidgets.QAction("Open on Disk")
        openOnDisk.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("disk")))
        menu.addAction(openOnDisk)

        modifyElements = QtWidgets.QAction("Modify Elements")
        modifyElements.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("modify")))
        menu.addAction(modifyElements)

        renameAsset = QtWidgets.QAction("Rename Asset")
        renameAsset.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("rename")))
        menu.addAction(renameAsset)

        deleteAsset = QtWidgets.QAction("Delete Asset")
        deleteAsset.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("delete")))
        menu.addAction(deleteAsset)
        
        menu.exec_(self.assetTree.mapToGlobal(point))

    def _createNewProject(self):
        """ Create a standard project (directory file and json),
            can be an existing directory or a new one via fild dialog
        """

        qfd = QtWidgets.QFileDialog()
        self.projectPath = QtWidgets.QFileDialog.getSaveFileName(
            qfd,
            ("Create a .JSON project file..."),
            filter="JSON Files (*.json *.JSON)")[0]

        if not self.projectPath:
            return
        
        self.projectDirectory = os.path.dirname(self.projectPath)
        self.projectFile = os.path.split(self.projectPath)[1]
        self.project = os.path.splitext(self.projectFile)[0]
        self._CAT_API.createProject(self.projectPath, self.projectFile)
        self.config = self._CAT_API.createConfig(self.projectDirectory, self.projectFile)

        # update form
        self.projectLineEdit.setText(self.project)

    def _onAssetChanged(self, index):
        """ Logic to run when the user clicks a new asset in the main asset tree view """
        self.selectedElement = None

        # clear the element view
        self.elementWidget.elementTree.model.removeRows(
            0, self.elementWidget.elementTree.model.rowCount())

        asset = self.assetTree.model.item(index.row(), 0).data()
        assetPath = asset.get("PATH")
        elements = asset.get("ELEMENTS")
        for element in elements:
            # add a new row in the elements tree
            # TODO p4 status
            elementPath = os.path.join(assetPath, element.lower())
            self.elementWidget.elementTree.addElementToTree(element, "LOCAL_UP_TO_DATE", elementPath)

        self.selectedAsset = asset
        print(self.selectedAsset)
        self._updateElementWidget()

    def _onElementChanged(self, index):
        self.selectedElement = self.elementWidget.elementTree.model.item(index.row(), 0).text().capitalize()
        self._updateElementWidget()

    def _openExistingProject(self):
        """ Open an existing json project
        """

        qfd = QtWidgets.QFileDialog()
        self.projectPath = QtWidgets.QFileDialog.getOpenFileName(
            qfd,
            ("Select a project (JSON)"),
            os.getenv('HOME'),
            # os.environ['USERPROFILE'],
            # TODO open to previous dir, store in config
            "JSON File *.json")[0]

        if not self.projectPath:
            return

        self.projectDirectory, self.projectFile = self._CAT_API.openProject(self.projectPath)
        self.project = os.path.splitext(self.projectFile)[0]
        self.config = self._CAT_API.getConfig(self.projectDirectory, self.projectFile)
        self.projectLineEdit.setText(self.project)
        self._refresh(init=True)

    def _refresh(self, init=False, newAsset=None):
        """ Init list items, append, and sort the list widget items

            args:
                init (bool): initialize the list
                newAsset (dict): asset to be appended
        """

        # TODO separate this into two functions, onOpen and onAddAsset or something

        print("GETTING ASSETS FROM:")
        print(self.projectPath)
        existingAssets = self._CAT_API.getProjectAssets(self.projectPath)

        if init and existingAssets:
            # opening a new project
            # can't clear because that kills the columns
            self.assetTree.model.removeRows(0, self.assetTree.model.rowCount())
            for asset in existingAssets:
                # TODO get perforce status
                self.assetTree.addAssetToTree(self.assetTree.model, asset)

        if newAsset:
            self.assetTree.addAssetToTree(self.assetTree.model, newAsset)

        # TODO self.assetList.sortItems()

    def _showCreateAssetWindow(self):
        if not self.project:
            self._showStatusMessage('WARN', "Open a project first!")
            return

        self.createAssetWindow.show()

    def _createAsset(self):

        assetName = self.createAssetWindow.nameLineEdit.text()
        assetType = _constants.ASSET_TYPES[self.createAssetWindow.assetTypeDrop.currentIndex()]
        elements = []

        for element in self.createAssetWindow.elements:
            if element.isChecked():
                elements.append(element.text())

        # TODO add asset type to the path
        path = os.path.join(self.projectDirectory, assetType, assetName)
        depotPath = os.path.join(_settings.PERFORCE_DEPOT_PATH, assetName)

        newAsset = self._CAT_API.createAsset(
            assetName,
            assetType,
            elements,
            path,
            depotPath,
            self.projectPath,
            self.project
        )

        # TODO confirmation box, create another or close?
        self.createAssetWindow.reset()
        self.createAssetWindow.hide()
        self._refresh(newAsset=newAsset)

    def _showStatusMessage(self, level, msg):
        """ Show a status message at a given level (INFO, WARN, ERROR)

        Args:
            level (str): Message severity
            msg (str): Message to show
        """
        self.statusBar().setStyleSheet(_constants.MESSAGE_SEVERITY.get(level))
        self.statusBar().showMessage(msg)

    def _updateElementWidget(self):
        self.elementWidget.refresh(self.selectedAsset, self.selectedElement)
