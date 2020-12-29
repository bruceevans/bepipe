
import os
import json
import pprint as pp

from . import ui

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.utility.utils as utils

_ELEMENTS = ["anim", "maps", "mesh", "output", "ref", "rig", "sculpt"]


class CAT(QtCore.QObject):
    """ Main control
    """

    _doWork = QtCore.Signal()

    def __init__(self):
        super(CAT, self).__init__()

        self._worker = None
        self._thread = None

        self.projectDirectory = None
        self.projectFile = None

        self._ui = ui.CATWindow()
        self._connectWidgets()
        self._ui.show()

    def _connectWidgets(self):
        self._ui.assetLineEdit.textChanged.connect(self._updateAsset)
        self._ui.btnCreate.clicked.connect(self._createAsset)
        self._ui.newProjectAction.triggered.connect(self._createProject)
        self._ui.openProjectAction.triggered.connect(self._openProject)

    def _addElementToProject(self, project, asset):
        """ Write an asset to the project file
        """

    def _createAsset(self):
        elements = []
        for i in self._getElements():
            elements.append(self._ui.elements[i].text())
        asset = self._createAssetDirectories(self._getElements())

        assetName = self._ui.assetLineEdit.text()
        # main project path joined to asset name folder
        assetPath = utils.toLinuxPath(os.path.join(self.projectDirectory, assetName))

        assetDict = {
            "NAME": assetName,
            "ELEMENTS": elements,
            "PATH": assetPath
            }

        # TODO add to project json
        self._writeAssetToFile(self.projectFile, assetDict)

        # TODO confirm creation or not
        if asset:
            self._ui.catMessageBox("Asset created!", self._cleanUp) # TODO pass clean up function
        # TODO self._cleanUp

    def _confirmAssetCreation(self):
        """ Return true if asset was made, else false
        """

    def _createAssetDirectories(self, elements):
        templateDirs = self._getTemplateDirectories()

        leftovers = []

        assetPath = os.path.join(self.projectDirectory, self._ui.assetLineEdit.text())
        os.mkdir(assetPath)

        for element in elements:  # element is an index
            for directory in templateDirs:
                if directory.get("Path").find(_ELEMENTS[element]) != -1:
                    relPath = directory.get("Path")
                    newFolder = os.path.join(assetPath, relPath)
                    newFolder = utils.toLinuxPath(newFolder)
                    try:
                        os.mkdir(newFolder)
                    except FileNotFoundError:
                        leftovers.append(newFolder)

        # TODO this needs work

        for leftover in leftovers:
            try:
                os.mkdir(leftover)
            except FileExistsError:
                continue 

        return True

    def _cleanUp(self):
        """ Reset the app
        """
        print("Cleaning up!")

    def _createProject(self):
        """ Create a standard project (directory file and json),
            can be an existing directory or a new one via fild dialog
        """

        # TODO check for a project that already exists

        qfd = QtWidgets.QFileDialog()        
        projectDirectory = QtWidgets.QFileDialog.getExistingDirectory(
            qfd, ("Choose a project folder or create one ..."))

        if not projectDirectory:
            return

        self.projectDirectory = projectDirectory

        projectName = os.path.split(projectDirectory)[1]
        self.projectFile = projectDirectory + "/" + projectName + ".json"

        # format project dictionary
        projectDict = [
            { "PROJECT": {
                "PATH": self.projectDirectory
                # TODO project type
            } },
            {
                "ASSETS": []
            }
        ]

        self._writeProjectFile(self.projectFile, projectDict)
        self._ui.projectLineEdit.setText(projectName)
        return projectName

    def _deleteAsset(self):
        """ Delete existing asset
        """

        # TODO remove directory
        # TODO remove JSON entry

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
        self.projectFile = project
        self.projectDirectory = os.path.dirname(project)
        projectName = os.path.splitext(os.path.basename(project))[0]
        self._ui.projectLineEdit.setText(projectName)

    def _getAsset(self):
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

    def _writeAssetToFile(self, projectFile, asset):

        data = None
        with open(projectFile, "r") as o:
            data = json.load(o)
        # get assetList and append a new one
        assetList = data[1].get("ASSETS")
        assetList.append(asset)
        jsonObject = json.dumps(data, indent=4)
        with open(projectFile, "w") as w:
            w.write(jsonObject)

    def _writeProjectFile(self, projectName, data):
        """ Create a new json file to store project info
        """

        jsonObject = json.dumps(data, indent=4)

        with open(projectName, "w") as o:
            o.write(jsonObject)
        