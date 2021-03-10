
import os
import json
import pprint as pp

from PySide2 import QtCore, QtGui, QtWidgets

import ui
import assets
import project
import jsonUtilities
import bepipe.core.utility.path as path

from bepipe.core.qt.assetList import AssetModel
from bepipe.core.qt.bepMessageBox import bepMessageBox

# TODO when existing asset is selected, check the existing elements and set it all to read only

_ELEMENTS = ["anim", "maps", "mesh", "output", "ref", "rig", "sculpt"] # TODO "lighting",
_NO_ASSET = "Select asset..."
_FILE_DIRECTORY = os.path.dirname(__file__)
_ASSET_ICONS = {
    'char': os.path.join(_FILE_DIRECTORY, 'resources/icons/char.png'),
    'environment': os.path.join(_FILE_DIRECTORY, 'resources/icons/environment.png'),
    'prop': os.path.join(_FILE_DIRECTORY, 'resources/icons/prop.png'),
    'vfx': os.path.join(_FILE_DIRECTORY, 'resources/icons/vfx.png')
}


class CAT(QtCore.QObject):
    """ Main control
    """

    _doWork = QtCore.Signal()

    def __init__(self):
        super(CAT, self).__init__()

        self.projectDirectory = None
        self.projectPath = None
        self.projectName = None

        self._ui = ui.CATWindow()
        self._connectWidgets()
        self._ui.show()

    def _connectWidgets(self):
        self._ui.btnCreate.clicked.connect(self._createNewAsset)
        self._ui.newProjectAction.triggered.connect(self._createNewProject)
        self._ui.openProjectAction.triggered.connect(self._openExistingProject)
        self._ui.newAssetLineEdit.textChanged.connect(self._enableCreateButton)

    def _cleanUp(self):
        """ Reset the app
        """
        self._refresh()
        self._ui.newAssetLineEdit.setText("")
        # TODO maybe select the recently created asset?
        for element in self._ui.elements:
            element.setChecked(True)

    def _createNewAsset(self):
        
        assetName = self._ui.newAssetLineEdit.text()
        assetType = self._ui.assetTypeDropDown.currentText()
        elements = [self._ui.elements[i].text() for i in self._getCheckedElementsFromUI()]
        assetPath = path.toLinuxPath(os.path.join(self.projectDirectory, assetName))

        if os.path.exists(assetPath):
            bepMessageBox("Oh no...", "Asset already exists!", self._cleanUp)
            return

        asset = assets.createAssetDict(assetName, assetType, elements, assetPath)
        assets.createAssetDirectories(self.projectDirectory, asset)

        if assets.writeAssetToFile(self.projectPath, asset):
            # TODO new asset clean up specific function? Select asset in table, read only checkboxes
            bepMessageBox("Asset Created!", "Created {}!".format(assetName), func=self._cleanUp)

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
        self.projectName = os.path.split(self.projectPath)[1]

        if not project.createProject(self.projectPath, self.projectName):
            return

        self._ui.projectLineEdit.setText(self.projectName)
        existingAssets = assets.getExistingAssets(self.projectPath)

        if existingAssets:
            self._refreshTableView(assets)

    def _enableCreateButton(self):
        if len(self._ui.newAssetLineEdit.text()) > 2:
            self._ui.btnCreate.setStyleSheet(ui.WHITE_TEXT)
            self._ui.btnCreate.setEnabled(True)
        else:
            self._ui.btnCreate.setStyleSheet(ui.GRAY_TEXT)
            self._ui.btnCreate.setEnabled(False)

    def _getCheckedElementsFromUI(self):
        """ Return a list of element to create as an index of ints
        """

        elements = []
        for i, element in enumerate(self._ui.elements):
            if element.isChecked():
                elements.append(i)
        return elements

    def _help(self):
        """Link to online documentation
        """
        # TODO

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
        self.projectName = os.path.splitext(os.path.basename(self.projectPath))[0]
        self._ui.projectLineEdit.setText(self.projectName)

        self._refresh(init=True)

    def _refresh(self, init=False, newAsset=None):
        existingAssets = assets.getExistingAssets(self.projectPath)
        if init:
            # clear listwidget
            for asset in existingAssets:
                assetItem = QtWidgets.QListWidgetItem()
                assetItem.setText(asset.get("NAME"))
                assetItem.setIcon(QtGui.QIcon(_ASSET_ICONS.get(asset.get("TYPE"))))
                # context menu
                self._ui.assetList.addItem(assetItem)

        if newAsset:
            print("Adding new asset: {}".format(newAsset))
