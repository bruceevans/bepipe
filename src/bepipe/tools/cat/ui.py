
import sys
from PySide2 import QtWidgets, QtCore, QtGui


NO_PROJECT = "Open a project or create a new one."
GRAY_TEXT = "color: rgb(150, 150, 150)"
WHITE_TEXT = "color: rgb(255, 255, 255)"

class CATWindow(QtWidgets.QMainWindow):
    """ Main window wrapper for CAT
    """

    def __init__(self):
        super(CATWindow, self).__init__()

        self.elements = []

        self._setupUi()
        self._connecteSignals()

    def _setupUi(self):
        """ UI Initialization
        """

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        prefsMenu = menuBar.addMenu("&Preferences")
        helpMenu = menuBar.addMenu("&Help")
        self.statusBar()

        # Menu actions
        # project is more of an asset database
        self.newProjectAction = QtWidgets.QAction('New Project', self)
        fileMenu.addAction(self.newProjectAction)
        self.openProjectAction = QtWidgets.QAction('Open Project', self)
        fileMenu.addAction(self.openProjectAction)

        # prefs
        self.projectMode = QtWidgets.QAction('Project Mode', self)
        self.projectMode.setCheckable(True)
        prefsMenu.addAction(self.projectMode)

        # help
        self.docs = QtWidgets.QAction('Read the Docs', self)
        helpMenu.addAction(self.docs)

        projectLabel = QtWidgets.QLabel("Current Project: ")
        self.projectLineEdit = QtWidgets.QLineEdit()
        self.projectLineEdit.setReadOnly(True)
        self.projectLineEdit.setText(NO_PROJECT)
        self.projectLineEdit.setStyleSheet(GRAY_TEXT)
        self.projectLineEdit.setStatusTip("Use 'File' > 'New' to create a new project or 'File' > 'Open' to open")
        projectTitleLayout = QtWidgets.QHBoxLayout()
        projectTitleLayout.addWidget(projectLabel)
        projectTitleLayout.addWidget(self.projectLineEdit)

        assetLabel = QtWidgets.QLabel("Asset Name: ")
        self.assetLineEdit = QtWidgets.QLineEdit()
        assetLayout = QtWidgets.QHBoxLayout()
        assetLayout.addWidget(assetLabel)
        assetLayout.addWidget(self.assetLineEdit)

        elementGroup = QtWidgets.QGroupBox("Elements")
        elementLayout = QtWidgets.QVBoxLayout()

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

        elementLayout.addWidget(animationCheckBox)
        elementLayout.addWidget(mapsCheckBox)
        elementLayout.addWidget(meshCheckBox)
        elementLayout.addWidget(outputCheckBox)
        elementLayout.addWidget(refCheckBox)
        elementLayout.addWidget(rigCheckBox)
        elementLayout.addWidget(sculptCheckBox)
        elementGroup.setLayout(elementLayout)

        self.btnCreate = QtWidgets.QPushButton("Create Asset")
        self.btnCreate.setEnabled(False)
        self.btnCreate.setStyleSheet(GRAY_TEXT)
        self.btnCreate.setFixedHeight(40)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(projectTitleLayout)
        mainLayout.addLayout(assetLayout)
        mainLayout.addWidget(elementGroup)
        mainLayout.addWidget(self.btnCreate)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("CAT by Be")
        self.setFixedWidth(400)
        self.show()

    def _connecteSignals(self):
        pass

    def catMessageBox(self, msg, func = None):

        """ Base message box to display text and confirm button
        """

        msgBox = QtWidgets.QMessageBox()
        # TODO Icon
        # TODO title
        msgBox.setText(msg)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

        result = msgBox.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            if func:
                func()  # TODO may need to pass args as well
            else:
                return

