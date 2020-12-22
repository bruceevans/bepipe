
import os
import json
from . import ui
from PySide2 import QtCore, QtGui, QtWidgets

import pprint as pp

_ELEMENTS = ["anim", "maps", "mesh", "output", "ref", "rig", "sculpt"]


class CAT(QtCore.QObject):
    """ Main control
    """

    _doWork = QtCore.Signal()

    def __init__(self):
        super(CAT, self).__init__()

        self._worker = None
        self._thread = None

        self._ui = ui.CATWindow()
        self._connectWidgets()
        self._ui.show()

    def _connectWidgets(self):
        self._ui.assetLineEdit.textChanged.connect(self._updateAsset)
        self._ui.btnCreate.clicked.connect(self._createAsset)
        self._ui.newProjectAction.triggered.connect(self._createProject)
        self._ui.openProjectAction.triggered.connect(self._openProject)

    def _createAsset(self):
        # create the folder structure based on selection
        elements = self._getElements()
        print(elements)
        # self._readJson()
        self._createAssetDirectories(elements)

        # TODO add to project json

    def _createAssetDirectories(self, elements):
        templateDirs = self._getTemplateDirectories()

        # comprehension to make a new list
        # resultDirs = [ i for j in elements if template[] ]

        for element in elements:  # element is an index
            for directory in templateDirs:
                if directory.get("Path").find(_ELEMENTS[element]) != -1:
                    # TODO join with project directory
                    # project + asset + directory
                    print(directory)

    def _createProject(self):
        """ Create a standard project (directory file and json),
            can be an existing directory or a new one via fild dialog
        """

        qfd = QtWidgets.QFileDialog()        
        projectDirectory = QtWidgets.QFileDialog.getExistingDirectory(
            qfd, ("Choose a project folder or create one ..."))

        if not projectDirectory:
            return

        projectName = os.path.split(projectDirectory)[1]
        projectFile = projectDirectory + "/" + projectName + ".json"
        self._writeProjectFile(projectFile, {})  # No data yet
        self._ui.projectLineEdit.setText(projectName)
        return projectName

    def _openProject(self):
        """ Open an existing json project
        """

        qfd = QtWidgets.QFileDialog()
        project = QtWidgets.QFileDialog.getOpenFileName(
            qfd,
            ("Select a project (JSON)"),
            os.environ['USERPROFILE'],
            "JSON File *.json")[0]
        if not project:
            return
        projectName = os.path.splitext(os.path.basename(project))[0]
        self._ui.projectLineEdit.setText(projectName)

    def _getAssetName(self):
        return self._ui.assetLineEdit.text()

    def _getElements(self):
        """ Return a list of element to create as an index of ints
        """

        elements = []
        for i, element in enumerate(self._ui.elements):
            if element.isChecked():
                elements.append(i)
        return elements

    def _getProjectPath(self):
        return self._ui.projectLineEdit.text()

    def _getTemplateDirectories(self):
        baseDirectory = os.path.dirname(__file__)
        relPath = "resources\\asset_tree.json"
        dirFile = os.path.join(baseDirectory, relPath)
        with open(dirFile, 'r') as f:
            dirData = json.load(f)
        templateDirectories = []
        for obj in dirData:
            if obj.get("Type") == "Directory":
                templateDirectories.append(obj)
        return templateDirectories

    def _help(self):
        # link to docs or something
        pass

    def _updateAsset(self):
        asset = self._getAsset()
        project = self._getProjectPath()
        if asset == None or project == ui.NO_PROJECT:
            self._ui.btnCreate.setEnabled(False)
            self._ui.btnCreate.setStyleSheet(ui.GRAY_TEXT)
            return None
        else:
            self._ui.btnCreate.setEnabled(True)
            self._ui.btnCreate.setStyleSheet(ui.WHITE_TEXT)
            return asset

    def _writeProjectFile(self, projectName, data):
        """ Create a new json file to store project info
        """

        jsonObject = json.dumps(data, indent=4)

        with open(projectName, "w") as o:
            o.write(jsonObject)
        