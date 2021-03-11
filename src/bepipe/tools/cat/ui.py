import os
import sys
import enum

from PySide2 import QtWidgets, QtCore, QtGui

from bepipe.core.qt.collapsableGroupBox import CollapsableGroupBox

# TODO move some of this to Qt module
# TODO think of some sort of setting system
# TODO icon factory

NO_PROJECT = "Open a project or create a new one."

GRAY_TEXT = "color: rgb(150, 150, 150)"
WHITE_TEXT = "color: rgb(255, 255, 255)"
GREEN_TEXT = "color: rgb(20, 220, 20)"

_FILE_DIR = os.path.join(os.path.dirname(__file__))
_WINDOW_ICON = os.path.join(_FILE_DIR, "resources/icons/icon_CAT.png")
_MENU_ICONS = {
    'disk': os.path.join(_FILE_DIR, "resources/icons/disk.png"),
    'modify': os.path.join(_FILE_DIR, "resources/icons/modify.png"),
    'rename': os.path.join(_FILE_DIR, "resources/icons/rename.png"),
    'delete': os.path.join(_FILE_DIR, "resources/icons/delete.png")
}
_ASSET_TYPES = ['char', 'environment', 'prop', 'vfx']

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
        self.mode = None

        self._setupUi()
        self._connectSignals()

    def _setupUi(self):
        """ UI Initialization
        """

        spacer = QtWidgets.QSpacerItem(0, 10)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        prefsMenu = menuBar.addMenu("&Preferences")
        helpMenu = menuBar.addMenu("&Help")
        self.statusBar()

        # Menu actions
        self.newProjectAction = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProjectAction)
        self.openProjectAction = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProjectAction)

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
        self.projectLineEdit.setStyleSheet(GRAY_TEXT)
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

        ## BOTTOM CREATE ASSET MENU ##

        self.newAssetLabel = QtWidgets.QLabel("New asset: ")
        self.newAssetLineEdit = QtWidgets.QLineEdit()
        newAssetLayout = QtWidgets.QHBoxLayout()
        newAssetLayout.addWidget(self.newAssetLabel)
        newAssetLayout.addWidget(self.newAssetLineEdit)

        assetTypeLabel = QtWidgets.QLabel("Asset type: ")
        self.assetTypeDropDown = QtWidgets.QComboBox()
        for type in _ASSET_TYPES:
            self.assetTypeDropDown.addItem(type)
        assetTypeLayout = QtWidgets.QHBoxLayout()
        assetTypeLayout.addWidget(assetTypeLabel)
        assetTypeLayout.addWidget(self.assetTypeDropDown)

        elementLayout = QtWidgets.QVBoxLayout()
        elementLabel = QtWidgets.QLabel("Choose asset elements:")

        self.animationCheckBox = QtWidgets.QCheckBox("Animation")
        self.animationCheckBox.setChecked(True)
        self.animationCheckBox.setStatusTip("Create an 'animation' folder to hold individual animations, IDLE, Walk, etc.")
        self.elements.append(self.animationCheckBox)
        self.mapsCheckBox = QtWidgets.QCheckBox("Maps")
        self.mapsCheckBox.setChecked(True)
        self.mapsCheckBox.setStatusTip("Create a 'maps' folder to hold a textures, PSD, and Sub. projects")
        self.elements.append(self.mapsCheckBox)
        self.meshCheckBox = QtWidgets.QCheckBox("Mesh")
        self.meshCheckBox.setChecked(True)
        self.meshCheckBox.setStatusTip("Create a 'mesh' folder to hold all Blender projects and versions")
        self.elements.append(self.meshCheckBox)
        self.outputCheckBox = QtWidgets.QCheckBox("Output")
        self.outputCheckBox.setChecked(True)
        self.outputCheckBox.setStatusTip("Create an 'output' folder for all renders")
        self.elements.append(self.outputCheckBox)
        self.refCheckBox = QtWidgets.QCheckBox("Reference")
        self.refCheckBox.setChecked(True)
        self.refCheckBox.setStatusTip("Create a 'ref' folder for all PureRef and other reference files.")
        self.elements.append(self.refCheckBox)
        self.rigCheckBox = QtWidgets.QCheckBox("Rig")
        self.rigCheckBox.setChecked(True)
        self.rigCheckBox.setStatusTip("Create a 'rig' folder to hold all Blender rig projects and versions")
        self.elements.append(self.rigCheckBox)
        self.sculptCheckBox = QtWidgets.QCheckBox("Sculpt")
        self.sculptCheckBox.setChecked(True)
        self.sculptCheckBox.setStatusTip("Create a 'sculpt' folder to hold all sculpting projects and versions")
        self.elements.append(self.sculptCheckBox)

        elementLayout.addWidget(elementLabel)
        elementLayout.addWidget(self.animationCheckBox)
        elementLayout.addWidget(self.mapsCheckBox)
        elementLayout.addWidget(self.meshCheckBox)
        elementLayout.addWidget(self.outputCheckBox)
        elementLayout.addWidget(self.refCheckBox)
        elementLayout.addWidget(self.rigCheckBox)
        elementLayout.addWidget(self.sculptCheckBox)

        self.btnCreate = QtWidgets.QPushButton("Create Asset")
        self.btnCreate.setEnabled(False)
        self.btnCreate.setStyleSheet(GRAY_TEXT)
        self.btnCreate.setFixedHeight(40)

        self.createAssetGroup = CollapsableGroupBox("Create New Asset", func=self.resizeWindow)
        createAssetLayout = QtWidgets.QVBoxLayout()
        createAssetLayout.addLayout(newAssetLayout)
        createAssetLayout.addLayout(assetTypeLayout)
        createAssetLayout.addLayout(elementLayout)
        createAssetLayout.addWidget(self.btnCreate)

        self.createAssetGroup.setLayout(createAssetLayout)
        # get collapsed window size TODO

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addItem(spacer)
        self.mainLayout.addLayout(projectTitleLayout)
        self.mainLayout.addItem(spacer)
        self.mainLayout.addWidget(self.assetGroup)
        self.mainLayout.addItem(spacer)
        self.mainLayout.addWidget(self.createAssetGroup)
        self.mainLayout.addItem(spacer)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("CAT by Be")
        self.setWindowIcon(self.icon)
        self.setFixedWidth(400)
        self.setFixedHeight(480)

        self.mode = Mode.Create
        self.createAssetGroup.toggleGroup()

        self.show()

    def _connectSignals(self):
        self.assetList.customContextMenuRequested.connect(self.assetContextMenu)

    def assetContextMenu(self, point):
        """ Context menu actions for created assets
        """

        asset = self.assetList.indexAt(point)

        if not asset:
            return

        # make it available to core
        self.contextAssetIndex = asset

        #self.assetList.itemFromIndex(asset) 
        print(self.contextAssetIndex.row())

        menu = QtWidgets.QMenu()

        menu.addAction(self.openOnDisk)
        menu.addAction(self.modifyElements)
        menu.addAction(self.rename)
        menu.addAction(self.delete)

        menu.exec_(self.assetList.mapToGlobal(point))

    def resizeWindow(self):
        """ Resize window if asset twirl down is selected
        """
        if self.createAssetGroup.isChecked():
            self.setFixedHeight(700)
        else:
            self.setFixedHeight(480)

    def closeEvent(self, event):
        # connect close signal
        self.close.emit()
        event.accept()
