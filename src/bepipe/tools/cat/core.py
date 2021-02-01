
import os
import json
import pprint as pp

from P4 import P4Exception
from PySide2 import QtCore, QtGui, QtWidgets

from . import ui
import bepipe.core.utility.helpers as utils
import bepipe.core.utility.bepipeP4 as bepipeP4

_ELEMENTS = ["anim", "maps", "mesh", "output", "ref", "rig", "sculpt"] # TODO "lighting",
_NO_ASSET = "Select asset..."

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
        self.mode = None
        self.p4 = None

        self._ui = ui.CATWindow()
        self._connectWidgets()
        self._ui.show()

    def _connectWidgets(self):
        self._ui.newAssetLineEdit.textChanged.connect(self._updateAsset)
        self._ui.btnCreate.clicked.connect(self._createAsset)
        self._ui.newProjectAction.triggered.connect(self._createProject)
        self._ui.openProjectAction.triggered.connect(self._openProject)
        self._ui.newAssetLineEdit.textChanged.connect(self.detectMode)
        self._ui.close.connect(self.submitChangelist)

    def _cleanUp(self):
        """ Reset the app
        """
        self._refresh()
        self._ui.newAssetLineEdit.setText("")
        for element in self._ui.elements:
            element.setChecked(True)

    def _createAsset(self):
        """ Create a new asset within a project
        """

        elements = []

        for i in self._getElements():
            elements.append(self._ui.elements[i].text())

        assetName = self._ui.newAssetLineEdit.text()

        if os.path.exists(os.path.join(self.projectDirectory, assetName)):
            self._ui.catMessageBox("Uh oh!", "Asset already exists!", self._cleanUp, cancelButton=True)
            return

        asset = self._createAssetDirectories(self._getElements())

        # main project path joined to asset name folder
        assetPath = utils.toLinuxPath(os.path.join(self.projectDirectory, assetName))

        assetDict = {
            "NAME": assetName,
            "ELEMENTS": elements,
            "PATH": assetPath
            }

        self._writeAssetToFile(self.projectFile, assetDict)

        if asset:
            self._ui.catMessageBox("Asset Created", "Successfully created asset {}!".format(assetName), self._cleanUp)

    def _createAssetDirectories(self, elements):
        """ Create folders for each element

        Args:
            elements (str list): elements from UI checkboxes
        """

        templateDirs = self._getTemplateDirectories()
        assetPath = os.path.join(self.projectDirectory, self._ui.newAssetLineEdit.text())
        os.mkdir(assetPath)

        for element in elements:  # element is an index
            for directory in templateDirs:
                if directory.get("Path").find(_ELEMENTS[element]) != -1:
                    relPath = directory.get("Path")
                    newFolder = os.path.join(assetPath, relPath)
                    newFolder = utils.toLinuxPath(newFolder)
                    try:
                        os.makedirs(newFolder)  # TODO exception?
                    except FileExistsError:
                        continue

        return True

    def _createProject(self):
        """ Create a standard project (directory file and json),
            can be an existing directory or a new one via fild dialog
        """

        # TODO deliberately name the json file

        qfd = QtWidgets.QFileDialog()        
        projectDirectory = QtWidgets.QFileDialog.getExistingDirectory(
            qfd, ("Choose a project folder or create one ..."))

        if not projectDirectory:
            return

        self.projectDirectory = projectDirectory

        projectName = os.path.split(projectDirectory)[1]
        self.projectFile = projectDirectory + "/" + projectName + ".json"

        if os.path.exists(self.projectFile):
            # File already exists, no need for a new one
            self._ui.catMessageBox("Uh oh!", "Project already exists!")
            return

        # format project file contents
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

    def _deleteAsset(self, asset):
        """ Delete existing asset
        """

        if not self._ui.catMessageBox("Hold up!", "Do you really want to delete {}?" % asset, cancelButton=True):
            return

        # TODO remove directory and JSON Entry
        fileInfo = self._getProjectFileContents(self.projectFile)
        assets = fileInfo.get("ASSETS")
        print(assets)

    def _getAsset(self):
        return self._ui.newAssetLineEdit.text()

    def _getElements(self):
        """ Return a list of element to create as an index of ints
        """

        elements = []
        for i, element in enumerate(self._ui.elements):
            if element.isChecked():
                elements.append(i)
        return elements

    def _getExistingAssets(self, projectFile):
        """ Get a list of all assets from the project file

            args:
                projectFile (str) path to json project file

            returns:
                str list: asset names
        """
        assetList = []
        projectData = self._getProjectFileContents(projectFile)

        assets = projectData[1].get("ASSETS")

        for asset in assets:
            assetList.append(asset.get("NAME"))

        return assetList

    def _getProjectFileContents(self, projectFile):
        """ Quickly grab the contents of the JSON project file
        """

        with open(projectFile, 'r') as p:
            projectData = json.load(p)

        return projectData

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
        """Link to online documentation
        """
        # TODO

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

        # Perforce stuff
        if self._ui.usingP4.isChecked():
            self.p4 = bepipeP4.createP4Instance(client='bevans') # TODO setting
            # sync latest
            print("syncing!")
            try:
                bepipeP4.syncFile(self.p4, self.projectFile)
                bepipeP4.createNewChangelist(self.p4, "Adding assets to project json")
            except P4Exception as e:
                print(e)

        self.projectDirectory = os.path.dirname(project)
        projectName = os.path.splitext(os.path.basename(project))[0]
        self._ui.projectLineEdit.setText(projectName)

        # TODO refresh method
        self._refresh()

        self._ui.mode = ui.Mode.ExistingAsset

    def _refresh(self):
        assets = self._getExistingAssets(self.projectFile)
        self._ui.existingAssetCombo.clear()
        self._ui.existingAssetCombo.addItem(_NO_ASSET)
        self._ui.existingAssetCombo.addItems(assets)

        # TODO init checkboxes

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

    def submitChangelist(self):
        # window with lineedit
        print("in changelist")
        if self._ui.usingP4.isChecked():
            if self.p4:
                # create description
                print("submitting")
                desc = "Added new assets to project file"
                bepipeP4.submitChangelist(self.p4, self.projectFile, desc)


    def detectMode(self):

        asset = self._ui.newAssetLineEdit.text()
        if len(asset) > 0:
            self.newAssetMode()
        else:
            self.existingAssetMode()

    def newAssetMode(self):
        """ Disables asset combos if there are values in the lineedit
        """
        self._ui.existingAssetLabel.setDisabled(True)
        self._ui.existingAssetCombo.setDisabled(True)
        self._ui.existingAssetLabel.setStyleSheet(ui.GRAY_TEXT)
        self._ui.existingAssetCombo.setStyleSheet(ui.GRAY_TEXT)
        self._ui.btnCreate.setText("Create Asset")
        self.mode = ui.Mode.NewAsset

    def existingAssetMode(self):
        """ If nothing is in the lineedit and an asset exists
        """
        self._ui.existingAssetLabel.setDisabled(False)
        self._ui.existingAssetCombo.setDisabled(False)
        self._ui.existingAssetLabel.setStyleSheet(ui.WHITE_TEXT)
        self._ui.existingAssetCombo.setStyleSheet(ui.WHITE_TEXT)
        self._ui.btnCreate.setText("Modify Asset")
        self.mode = ui.Mode.ExistingAsset
        # TODO populate check boxes

    # TODO On close, if using perforce, prompt a changelog comment