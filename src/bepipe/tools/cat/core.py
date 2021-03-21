
import os
import json
import pprint as pp

from PySide2 import QtCore, QtGui, QtWidgets

import ui
import assets
import project
import jsonUtilities
import bepipe.core.qt.style as style
import bepipe.core.utility.path as path

from bepipe.core.qt.bepMessageBox import bepMessageBox
from bepipe.core.qt.bepListWidgetItem import BepListWidgetItem


_NO_ASSET = "Select asset..."


class CAT(QtCore.QObject):
    """ Main control
    """

    _doWork = QtCore.Signal()

    def __init__(self):
        super(CAT, self).__init__()

        self.projectDirectory = None
        self.projectPath = None
        self.projectName = None

        self.assetElements = None

        self._ui = ui.CATWindow()
        self._connectWidgets()
        self._ui.show()

    def _connectWidgets(self):
        # self._ui.btnCreate.clicked.connect(self._createNewAsset)
        self._ui.newProjectAction.triggered.connect(self._createNewProject)
        self._ui.openProjectAction.triggered.connect(self._openExistingProject)
        self._ui.assetList.currentItemChanged.connect(self._getSelectedAssetInList)

        self._ui.openOnDisk.triggered.connect(self._openAssetDirectory)
        # self._ui.modifyElements.triggered.connect(self._modifyAssetElements)
        self._ui.rename.triggered.connect(self._renameAsset)
        self._ui.delete.triggered.connect(self._deleteAsset)

    def _createNewAsset(self):
        
        assetName = self._ui.newAssetLineEdit.text()
        assetType = self._ui.assetTypeDropDown.currentText()
        elements = self._getCheckedElementsFromUI()
        assetPath = path.toLinuxPath(os.path.join(self.projectDirectory, assetName))

        if os.path.exists(assetPath):
            bepMessageBox("Oh no...", "Asset already exists!", self._cleanUp)
            return

        asset = assets.createAssetDict(assetName, assetType, elements, assetPath)
        assets.createAssetDirectories(self.projectDirectory, asset)

        if not assets.writeAssetToFile(self.projectPath, asset):
            print("Failed to write {}".format(assetName))
            return

        # TODO actual cleaning func
        # TODO if has custom elemt, readonly, etc.
        self._ui.newAssetLineEdit.setText("")
        self._refresh(newAsset=asset)
        bepMessageBox("Asset Created!", "Created {}!".format(assetName))
        self._selectCreatedAsset(asset)

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

        self._ui.projectLineEdit.setText(os.path.splitext(self.projectName)[0])
        existingAssets = project.getProjectAssets(self.projectPath)

        if existingAssets:
            self._refreshTableView(assets)

    def _createMode(self):
        """ Mode for creating new objects
        """
        self._ui.mode = ui.Mode.Create
        # deselect
        # self._ui.assetList.
        self._toggleLabels(self._ui.mode)
        self._toggleElementCheckboxes(self._ui.mode)

    def _deleteAsset(self):
        """ Delete a selected asset
            
            returns:
                bool
        """

        if not self._ui.contextAssetIndex:
            bepMessageBox("Oops", "Couldn't find an asset to delete, make a selection and try again.")
            return
        asset = self._ui.assetList.itemFromIndex(self._ui.contextAssetIndex)
        if not bepMessageBox("Are you sure?", "This will delete {} forever, are you sure?".format(asset.assetData.get("NAME")),cancelButton=True):
            return

        assets.deleteAssetDirectory(asset.assetData.get("PATH"))
        project.removeAssetEntry(self.projectPath, asset.assetData)
        self._removeListWidgetItem(self._ui.contextAssetIndex)
        return True

    def _getCheckedElementsFromUI(self):
        """ Return a list of element to create as an index of ints
        """

        elements = []
        for element in self._ui.elements:
            if element.isChecked():
                elements.append(element.text())

        if self._ui.customElement.isChecked():
            elements.append(self._ui.customElementLineEdit.text())

        return elements

    def _getSelectedAssetInList(self):
        """ Get the selected asset
        """

        if not self._ui.assetList.currentItem():
            self._createMode()
            self._ui.assetInfoLayout = self._ui._noAsset()
            return

        asset = self._ui.assetList.currentItem()

        print("TODO update the asset info")

        return asset

    def _help(self):
        """Link to online documentation
        """
        # TODO

    def _openAssetDirectory(self):
        """ Open the explorer window to the given path
        """

        if not self._ui.contextAssetIndex:
            return

        path = self._ui.assetList.itemFromIndex(self._ui.contextAssetIndex).assetData.get("PATH")
        assets.openOnDisk(path)

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
        """ Init list items, append, and sort the list widget items

            args:
                init (bool): initialize the list
                newAsset (dict): asset to be appended
        """

        existingAssets = project.getProjectAssets(self.projectPath)

        if init and existingAssets:
            # TODO clear list widget items
            for asset in existingAssets:
                assetItem = BepListWidgetItem(asset)
                assetItem.setIcon(QtGui.QIcon(ui.ASSET_ICONS.get(asset.get("TYPE"))))
                assetItem.setText(asset.get("NAME"))
                self._ui.assetList.addItem(assetItem)

        if newAsset:
            assetItem = BepListWidgetItem(newAsset)
            assetItem.setIcon(QtGui.QIcon(ui.ASSET_ICONS.get(newAsset.get("TYPE"))))
            assetItem.setText(newAsset.get("NAME"))
            self._ui.assetList.addItem(assetItem)

        self._ui.assetList.sortItems()

    def _removeListWidgetItem(self, asset):
        self._ui.assetList.takeItem(asset.row())

    def _renameAsset(self):
        if not self._ui.contextAssetIndex:
            bepMessageBox("Oops", "Couldn't find an asset to rename, make a selection and try again.")
            return
        asset = self._ui.assetList.itemFromIndex(self._ui.contextAssetIndex)
        assets.renameAsset(asset.assetData.get("PATH"))

    def _resetCheckboxes(self):
        for uiElement in self._ui.elements:
            uiElement.setChecked(False)

    def _selectCreatedAsset(self, asset):
        """ After creating a new asset, select it in the list view,
            populate the checkboxes, set the info to read only,
            change some labeling

            args:
                asset (dict): asset and all its info
        """

        listAsset = self._ui.assetList.findItems(asset.get("NAME"), QtCore.Qt.MatchExactly)
        if not listAsset:
            return
        self._editMode(asset)
        self._ui.assetList.setItemSelected(listAsset[0], True)

    def _toggleElementCheckboxes(self, mode, elements=None):
        """ Toggle the checkboxes for given assets
        """

        if mode == ui.Mode.Create:
            for uiElement in self._ui.elements:
                uiElement.setChecked(True)
                uiElement.setEnabled(True)
                uiElement.setStyleSheet(style.WHITE_TEXT)
        else:

            # read only
            # set checked
            # TODO use indices and listcomprehension

            if elements:
                self._resetCheckboxes()
                checked = []
                checkBoxes = []
                for uiElement in self._ui.elements:
                    uiElement.setChecked(True)
                    uiElement.setEnabled(False)
                    uiElement.setStyleSheet(style.GREEN_TEXT)

                for uiElement in self._ui.elements:
                    checkBoxes.append(uiElement)
                    for element in elements:
                        if uiElement.text().lower() == element.lower():
                            checked.append(uiElement)

                unchecked = [x for x in checkBoxes if x not in checked]
                for cb in unchecked:
                    cb.setChecked(False)
                    cb.setStyleSheet(style.GRAY_TEXT)

    def _toggleLabels(self, mode):
        """ If an asset is selected, toggle the labels to match
        """

        if mode == ui.Mode.Create:
            self._ui.btnCreate.setStyleSheet(style.WHITE_TEXT)
            self._ui.btnCreate.setEnabled(True)
            # deselect from the list?

        else:
            self._ui.btnCreate.setStyleSheet(style.GRAY_TEXT)
            self._ui.btnCreate.setEnabled(False)

    def _toggleMode(self):
        if len(self._ui.newAssetLineEdit.text()) > 0:
            self._createMode()

        else:
            self._editMode()
