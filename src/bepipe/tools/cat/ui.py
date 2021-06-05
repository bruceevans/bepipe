
import os
import sys
from pprint import pprint

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.qt.style as style
import bepipe.core.qt.widgets as widgets

from . utility import _project
from . utility import _constants
from . import _assetTree


_SPACER = QtWidgets.QSpacerItem(0, 10)


class CATWindow(QtWidgets.QMainWindow):
    """ Main gui for CAT
    """

    def __init__(self):
        super(CATWindow, self).__init__()

        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)

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



        # Asset Info Area #

        # TODO class this out

        mainAssetInfoLayout = QtWidgets.QVBoxLayout()

        self.assetInfoGroup = QtWidgets.QGroupBox("Asset Status")
        self.perforceGroup = QtWidgets.QGroupBox("Perforce Tools")

        assetInfoLayout = QtWidgets.QVBoxLayout()

        assetStatusLayout = QtWidgets.QHBoxLayout()
        labelLayout = QtWidgets.QVBoxLayout()
        statusLayout = QtWidgets.QVBoxLayout()

        buttonLayout = QtWidgets.QVBoxLayout()

        versionLabel = QtWidgets.QLabel("Version: ")
        versionLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.version = QtWidgets.QLabel("V00")
        self.version.setAlignment(QtCore.Qt.AlignLeft)
        labelLayout.addWidget(versionLabel)
        statusLayout.addWidget(self.version)

        userLabel = QtWidgets.QLabel("User: ")
        userLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.user = QtWidgets.QLabel("Bevans")
        self.user.setAlignment(QtCore.Qt.AlignLeft)
        labelLayout.addWidget(userLabel)
        statusLayout.addWidget(self.user)

        dateLabel = QtWidgets.QLabel("Date: ")
        dateLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.date = QtWidgets.QLabel("00/00/0000")
        self.date.setAlignment(QtCore.Qt.AlignLeft)
        labelLayout.addWidget(dateLabel)
        statusLayout.addWidget(self.date)

        commentLabel = QtWidgets.QLabel("Comment: ")
        commentLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.comment = QtWidgets.QLabel("This is a really long publish comment")
        self.comment.setWordWrap(True)
        self.comment.setAlignment(QtCore.Qt.AlignLeft)
        labelLayout.addWidget(commentLabel)
        statusLayout.addWidget(self.comment)

        assetStatusLayout.addLayout(labelLayout)
        assetStatusLayout.addLayout(statusLayout)
        assetInfoLayout.addLayout(assetStatusLayout)

        self.assetInfoGroup.setLayout(assetInfoLayout)

        # TODO icon only
        self.getLatestButton = QtWidgets.QPushButton("Get Latest")
        self.getLatestButton.setFixedHeight(40)
        self.checkOutButton = QtWidgets.QPushButton("Check Out")
        self.checkOutButton.setFixedHeight(40)
        self.checkInButton = QtWidgets.QPushButton("Check In")
        self.checkInButton.setFixedHeight(40)
        buttonLayout.addWidget(self.getLatestButton)
        buttonLayout.addWidget(self.checkOutButton)
        buttonLayout.addWidget(self.checkInButton)

        self.perforceGroup.setLayout(buttonLayout)

        mainAssetInfoLayout.addWidget(self.assetInfoGroup)
        mainAssetInfoLayout.addWidget(self.perforceGroup)

        assetArea = QtWidgets.QHBoxLayout()
        assetArea.addWidget(self.assetGroup)
        assetArea.addLayout(mainAssetInfoLayout)




        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addLayout(projectTitleLayout)
        self.mainLayout.addItem(_SPACER)
        self.mainLayout.addLayout(assetArea)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("CAT by Be")
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

    def _connectWidgets(self):
        """ Connect slots and signals
        """

        # Menus

        self.newProject.triggered.connect(self._createNewProject)
        self.openProject.triggered.connect(self._openExistingProject)
        # createNewAsset
        # viewConnection
        # readDocs
        self.assetTree.customContextMenuRequested.connect(self._contextMenu)

    ##### UI Functions #####

    def _contextMenu(self, point):
        """ Context menu for main tree view
        """

        # make this a parameter?
        asset = self.assetTree.indexAt(point)
        if not asset:
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
            self.project = os.path.split(self.projectPath)[1]

            if not _project.createProject(self.projectPath, self.project):
                return

            self.projectLineEdit.setText(os.path.splitext(self.project)[0])
            existingAssets = _project.getProjectAssets(self.projectPath)

            if existingAssets:
                self._refresh(existingAssets)

    def _openExistingProject(self):
        """ Open an existing json project
        """

        qfd = QtWidgets.QFileDialog()
        self.projectPath = QtWidgets.QFileDialog.getOpenFileName(
            qfd,
            ("Select a project (JSON)"),
            os.environ['USERPROFILE'],
            "JSON File *.json")[0]

        if not self.projectPath:
            return

        self.projectDirectory = os.path.dirname(self.projectPath)
        self.project = os.path.splitext(os.path.basename(self.projectPath))[0]
        self.projectLineEdit.setText(self.project)
        self._refresh(init=True)

    def _refresh(self, init=False, newAsset=None):
        """ Init list items, append, and sort the list widget items

            args:
                init (bool): initialize the list
                newAsset (dict): asset to be appended
        """
        # TODO separate this into two functions, onOpen and onAddAsset or something

        existingAssets = _project.getProjectAssets(self.projectPath)

        if init and existingAssets:
            # opening a new project
            self.assetTree.model.removeRows(0, self.assetTree.model.rowCount())
            for asset in existingAssets:
                # TODO get perforce status
                self.assetTree.addAssetToTree(self.assetTree.model, asset, "p4 status todo")

        if newAsset:
            self.assetTree.addAssetToTree(self.assetTree.model, newAsset, "p4 status todo")

        # TODO self.assetList.sortItems()
