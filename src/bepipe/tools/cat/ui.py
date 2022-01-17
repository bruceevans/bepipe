
import os
from pprint import pprint

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.qt.style as style
import bepipe.core.bep4 as bep4

from .api import cat
from .api import _settings
from .api import _constants
from .dialog import _assetTree
from .dialog import _elementWidget
from .dialog import _createAssetDialog
from .dialog import _preferencesDialog


# TODO move to widgets module
_SPACER = QtWidgets.QSpacerItem(0, 10)
_RECENT_PROJECT_LIMIT = 5

# TODO move to config/settings
_SERVER = "ec2-34-219-230-44.us-west-2.compute.amazonaws.com"
_PORT = "1666"
_CLIENT = "bevans_mbp_1988"

# TODO add a filter search bar

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
        # Local app settings
        self.settings = QtCore.QSettings("BeTools", "CAT")
        # self.settings.setValue("recentProjects", [])
        self.recentProjects = []
        self.selectedAsset = None
        self.selectedElement = None
        self.createAssetWindow = _createAssetDialog.CreateAssetDialog()
        self.preferencesDialog = None

        self._setupUi()
        self._connectWidgets()

    def _setupUi(self):
        """ UI initialization
        """

        # Menu bar #

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        createMenu = menuBar.addMenu("&Create")
        helpMenu = menuBar.addMenu("&Help")

        # Menu actions #

        self.newProject = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProject)

        self.openProject = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProject)

        self.recentProjectsMenu = QtWidgets.QMenu('Open Recent', self)
        fileMenu.addMenu(self.recentProjectsMenu)
        self._setRecentProjects()

        self.openPreferences = QtWidgets.QAction('&Preferences')
        fileMenu.addAction(self.openPreferences)

        self.createNewAsset = QtWidgets.QAction('Create New Asset', self)
        createMenu.addAction(self.createNewAsset)

        # TODO preferences window will handle the P4 settings
        # self.perforceInfo = QtWidgets.QAction('View Connection', self)
        # perforceMenu.addAction(self.perforceInfo)

        self.readDocs = QtWidgets.QAction('Read the Docs', self)
        helpMenu.addAction(self.readDocs)
    
        self.about = QtWidgets.QAction('&About', self)
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
        self.openPreferences.triggered.connect(self._showPreferencesDialog)
        self.about.triggered.connect(self._showAboutDialog)
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
        # TODO open a create asset menu with the title read-only with the asset name
        menu.addAction(modifyElements)

        renameAsset = QtWidgets.QAction("Rename Asset")
        renameAsset.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("rename")))
        # TODO open a simple line edit message box
        # updata name, folder, path, etc.
        menu.addAction(renameAsset)

        deleteAsset = QtWidgets.QAction("Delete Asset")
        deleteAsset.setIcon(QtGui.QIcon(_constants.MENU_ICONS.get("delete")))
        # TODO call delete func
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
        self._setRecentProjects()

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
            # TODO make the status string a callback that can be inserted into the addElementToTree func
            self.elementWidget.elementTree.addElementToTree(element, "LOCAL_UP_TO_DATE", elementPath)

        self.selectedAsset = asset
        self._updateElementWidget()

    def _onElementChanged(self, index):
        self.selectedElement = self.elementWidget.elementTree.model.item(index.row(), 0).text().capitalize()
        self._updateElementWidget()

    def _openExistingProject(self):
        """ Open an existing json project
        """

        fileDirectory = self.settings.value("recentProjectDirectory") or os.getenv('HOME')

        qfd = QtWidgets.QFileDialog()
        self.projectPath = QtWidgets.QFileDialog.getOpenFileName(
            qfd,
            ("Select a project (JSON)"),
            fileDirectory,
            "JSON File *.json")[0]

        if not self.projectPath:
            return

        self.projectDirectory, self.projectFile = self._CAT_API.openProject(self.projectPath)
        self.project = os.path.splitext(self.projectFile)[0]
        self.config = self._CAT_API.getConfig(self.projectDirectory, self.projectFile)
        self.projectLineEdit.setText(self.project)

        # Set the settings
        self.settings.setValue("recentProjectDirectory", self.projectDirectory)

        # move the recently opened project to the top of the recent project list
        self._setRecentProjects()
        self._refresh(init=True)

    def _openRecentProject(self):
        """Open a recent project from the menu
        
        Args:
            projectPath (str): Path to project
        
        """
        action = self.sender()
        # Update the project
        self.projectPath = action.data()
        self.projectDirectory, self.projectFile = self._CAT_API.openProject(self.projectPath)
        self.project = os.path.splitext(self.projectFile)[0]
        self.config = self._CAT_API.getConfig(self.projectDirectory, self.projectFile)
        self.projectLineEdit.setText(self.project)

        self._setRecentProjects()
        self._refresh(init=True)

    def _refresh(self, init=False, newAsset=None):
        """ Init list items, append, and sort the list widget items

            args:
                init (bool): initialize the list
                newAsset (dict): asset to be appended
        """

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

    def _setRecentProjects(self):

        recentProjects = self.settings.value("recentProjects")
        currentProject = {
            "project": self.project,
            "path": self.projectPath
        }

        # No project = new CAT session
        if not currentProject["project"] and not recentProjects:
            self._refreshRecentProjects()
            return

        if not currentProject["project"]:
            self._refreshRecentProjects(recentProjects=recentProjects)
            return
        
        if not recentProjects:
            recentProjects = [currentProject]
            self.settings.setValue("recentProjects", recentProjects)
            self._refreshRecentProjects(recentProjects=recentProjects)
            return

        project = [p for p in recentProjects if p.get("project") == self.project]
        
        if project:
            if len(project) > 1:
                print("WARNING! FOUND PROJECTS WITH MATCHING NAMES!")
            project = project[0]
            recentProjects.remove(project)
        else:
            # Project hasn't been added to settings yet
            project = {
                "project": self.project,
                "path": self.projectPath
            }

        if len(recentProjects) > _RECENT_PROJECT_LIMIT:
            recentProjects = recentProjects[:4]

        # Add current project back in the list at the head
        recentProjects.insert(0, project)

        self.settings.setValue("recentProjects", recentProjects)
        self._refreshRecentProjects(recentProjects=recentProjects)

    def _refreshRecentProjects(self, recentProjects=None):
        # clear recent projects menu
        self.recentProjectsMenu.clear()

        if not recentProjects:
            # Add a pass through action
            self.recentProjectsMenu.addAction(QtWidgets.QAction("No recent projects", self))
            return

        # Create actions
        for project in recentProjects:
            projectName = project.get("project")
            projectPath = project.get("path")
            action = QtWidgets.QAction(projectName, self)
            action.setData(projectPath)
            action.triggered.connect(self._openRecentProject)
            self.recentProjectsMenu.addAction(action)
            self.recentProjects.append(project)

    def _applyPreferences(self):
        """Apply new preferences from dialog"""
        print("SAVING PREFS FROM PREFS DIALOG")
        # TODO apply P4 stuff, make public var

        client = self.settings.value("perforceWorkspace")
        self._CAT_API._setupBP4(client=client)

    def _showAboutDialog(self):
        print("Showing about")

    def _showCreateAssetWindow(self):
        if not self.project:
            self._showStatusMessage('WARN', "Open a project first!")
            return

        self.createAssetWindow.show()

    def _showPreferencesDialog(self):
        if not self.preferencesDialog:
            self.preferencesDialog = _preferencesDialog.PreferencesDialog(self.settings)
        self.preferencesDialog.savePreferences.connect(self._applyPreferences)
        self.preferencesDialog.show()

    def _createAsset(self):
        """Create an asset with info from the create asset menu
        """

        assetName = self.createAssetWindow.nameLineEdit.text()
        assetType = _constants.ASSET_TYPES[self.createAssetWindow.assetTypeDrop.currentIndex()]
        elements = []

        for element in self.createAssetWindow.elements:
            if element.isChecked():
                elements.append(element.text())

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
