import os
import sys
import enum

from PySide2 import QtWidgets, QtCore, QtGui

from bepipe.core.qt.collapsableGroupBox import CollapsableGroupBox

# TODO move some of this to Qt module
# TODO think of some sort of setting system

NO_PROJECT = "Open a project or create a new one."
GRAY_TEXT = "color: rgb(150, 150, 150)"
WHITE_TEXT = "color: rgb(255, 255, 255)"

# TODO make relative/move to resources
ICON = os.path.join(os.path.dirname(__file__), "resources/icons/icon_CAT.png")

# TODO icons
_ASSET_TYPES = ['char', 'environment', 'prop', 'vfx']

# TODO get starter files for different projects


class Mode(enum.Enum):
    NewAsset = 1
    ExistingAsset = 2


class CATWindow(QtWidgets.QMainWindow):
    """ Main window wrapper for CAT
    """

    close = QtCore.Signal()

    def __init__(self):
        super(CATWindow, self).__init__()

        self.icon = QtGui.QIcon(ICON)

        self.elements = []

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

        assetLayout = QtWidgets.QVBoxLayout()
        assetLayout.addWidget(self.assetList)
        self.assetGroup.setLayout(assetLayout)

        ## BOTTOM CREATE ASSET MENU ##

        newAssetLabel = QtWidgets.QLabel("New asset: ")
        self.newAssetLineEdit = QtWidgets.QLineEdit()
        newAssetLayout = QtWidgets.QHBoxLayout()
        newAssetLayout.addWidget(newAssetLabel)
        newAssetLayout.addWidget(self.newAssetLineEdit)

        assetType = QtWidgets.QLabel("Asset type: ")
        self.assetTypeDropDown = QtWidgets.QComboBox()
        for type in _ASSET_TYPES:
            self.assetTypeDropDown.addItem(type)
        assetTypeLayout = QtWidgets.QHBoxLayout()
        assetTypeLayout.addWidget(assetType)
        assetTypeLayout.addWidget(self.assetTypeDropDown)

        elementLayout = QtWidgets.QVBoxLayout()
        elementLabel = QtWidgets.QLabel("Choose asset elements:")
        animationCheckBox = QtWidgets.QCheckBox("Animation")
        animationCheckBox.setChecked(True)
        animationCheckBox.setStatusTip("Create an 'anim' folder to hold individual animations, IDLE, Walk, etc.")
        self.elements.append(animationCheckBox)
        mapsCheckBox = QtWidgets.QCheckBox("Maps")
        mapsCheckBox.setChecked(True)
        mapsCheckBox.setStatusTip("Create a 'maps' folder to hold a textures, PSD, and Sub. projects")
        self.elements.append(mapsCheckBox)
        meshCheckBox = QtWidgets.QCheckBox("Mesh")
        meshCheckBox.setChecked(True)
        meshCheckBox.setStatusTip("Create a 'mesh' folder to hold all Blender projects and versions")
        self.elements.append(meshCheckBox)
        outputCheckBox = QtWidgets.QCheckBox("Output")
        outputCheckBox.setChecked(True)
        outputCheckBox.setStatusTip("Create an 'output' folder for all renders")
        self.elements.append(outputCheckBox)
        refCheckBox = QtWidgets.QCheckBox("Reference")
        refCheckBox.setChecked(True)
        refCheckBox.setStatusTip("Create a 'ref' folder for all PureRef and other reference files.")
        self.elements.append(refCheckBox)
        rigCheckBox = QtWidgets.QCheckBox("Rig")
        rigCheckBox.setChecked(True)
        rigCheckBox.setStatusTip("Create a 'rig' folder to hold all Blender rig projects and versions")
        self.elements.append(rigCheckBox)
        sculptCheckBox = QtWidgets.QCheckBox("Sculpt")
        sculptCheckBox.setChecked(True)
        sculptCheckBox.setStatusTip("Create a 'sculpt' folder to hold all sculpting projects and versions")
        self.elements.append(sculptCheckBox)

        elementLayout.addWidget(elementLabel)
        elementLayout.addWidget(animationCheckBox)
        elementLayout.addWidget(mapsCheckBox)
        elementLayout.addWidget(meshCheckBox)
        elementLayout.addWidget(outputCheckBox)
        elementLayout.addWidget(refCheckBox)
        elementLayout.addWidget(rigCheckBox)
        elementLayout.addWidget(sculptCheckBox)

        self.btnCreate = QtWidgets.QPushButton("Create Asset")
        self.btnCreate.setEnabled(False)
        self.btnCreate.setStyleSheet(GRAY_TEXT)
        self.btnCreate.setFixedHeight(40)

        self.createAssetGroup = CollapsableGroupBox("Create New Asset")
        createAssetLayout = QtWidgets.QVBoxLayout()
        createAssetLayout.addLayout(newAssetLayout)
        createAssetLayout.addLayout(assetTypeLayout)
        createAssetLayout.addLayout(elementLayout)
        createAssetLayout.addWidget(self.btnCreate)

        self.createAssetGroup.setLayout(createAssetLayout)
        # get collapsed window size TODO
        self.createAssetGroup.toggleGroup()

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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setFixedWidth(350)
        self.show()

    def _connectSignals(self):
        self.assetList.customContextMenuRequested.connect(self.assetContextMenu)

    def closeEvent(self, event):
        # connect close signal
        self.close.emit()
        event.accept()

    def assetContextMenu(self, point):
        """ Context menu actions for created assets
        """

        asset = self.assetList.indexAt(point)
        print(asset)

        if not asset:
            return

        menu = QtWidgets.QMenu()
        openOnDisk = QtWidgets.QAction("Open on Disk")
        modifyElements = QtWidgets.QAction("Modify Elements")
        rename = QtWidgets.QAction("Rename Asset") # more involved than you think
        delete = QtWidgets.QAction("Delete Asset")

        menu.addAction(openOnDisk)
        menu.addAction(modifyElements)
        menu.addAction(rename)
        menu.addAction(delete)

        menu.exec_(self.assetList.mapToGlobal(point))
