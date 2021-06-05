
class CAT(QtCore.QObject):
    """ Main control for CAT
    """

    def __init__(self):
        super(CAT, self).__init__()

        self._ui = _dialog.CATWindow()

        self.project = None
        self.projectDirectory = None
        self.projectPath = None
        self.assetElements = None

        self._connectSignals()
        self._ui.show()

    def _connectSignals(self):
        """
        self._ui.assetList.currentItemChanged.connect(self._getSelectedAssetInList)
        self._ui.openOnDisk.triggered.connect(self._openAssetDirectory)
        self._ui.rename.triggered.connect(self._renameAsset)
        self._ui.delete.triggered.connect(self._deleteAsset)
        """
        self._ui.newProject.triggered.connect(self._createNewProject)
        self._ui.openProject.triggered.connect(self._openExistingProject)
        self._ui.createNewAsset.triggered.connect(self._showCreateAssetWindow)

    def _showCreateAssetWindow(self):
        """ Show the create asset window
        """
        if not self.project:
            bepWidgets.bepMessageBox('Project Not Found!', 'Open or create a new project to create assets.')
            return
        self.createAssetWindow = _dialog.CreateAssetWindow()
        self.createAssetWindow.btnCreate.clicked.connect(self._createAsset)
        self.createAssetWindow.show()

    def _createAsset(self):
        """ Write dict to json
        """
        assetName = self.createAssetWindow.newAssetLineEdit.text()
        assetType = self.createAssetWindow.assetTypeDropDown.currentText()
        elements = self._getCheckedElementsFromUI()
        assetPath = path.toLinuxPath(os.path.join(self.projectDirectory, assetName))

        if os.path.exists(assetPath):
            bepWidgets.bepMessageBox("Oh no...", "Asset already exists!", self._cleanUp)
            return

        asset = _assets.createAssetDict(assetName, assetType, elements, assetPath)
        _assets.createAssetDirectories(self.projectDirectory, asset)

        if not _assets.writeAssetToFile(self.projectPath, asset):
            print("Failed to write {}".format(assetName))
            return

        # TODO actual cleaning func
        # TODO if has custom elemt, readonly, etc.
        self._ui.newAssetLineEdit.setText("")
        self._refresh(newAsset=asset)
        bepWidgets.bepMessageBox("Asset Created!", "Created {}!".format(assetName))
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
            self.project = os.path.split(self.projectPath)[1]

            if not _project.createProject(self.projectPath, self.project):
                return

            self._ui.projectLineEdit.setText(os.path.splitext(self.project)[0])
            existingAssets = _project.getProjectAssets(self.projectPath)

            if existingAssets:
                self._refreshTableView(existingAssets)

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
        self._ui.projectLineEdit.setText(self.project)
        self._refresh(init=True)

    def _refresh(self, init=False, newAsset=None):
        """ Init list items, append, and sort the list widget items

            args:
                init (bool): initialize the list
                newAsset (dict): asset to be appended
        """

        existingAssets = _project.getProjectAssets(self.projectPath)

        if init and existingAssets:
            # TODO clear list widget items
            for asset in existingAssets:
                assetItem = bepWidgets.BepListWidgetItem(asset)
                assetItem.setIcon(QtGui.QIcon(_constants.ASSET_ICONS.get(asset.get("TYPE"))))
                assetItem.setText(asset.get("NAME"))
                self._ui.assetList.addItem(assetItem)

        if newAsset:
            assetItem = bepWidgets.BepListWidgetItem(newAsset)
            assetItem.setIcon(QtGui.QIcon(_constants.ASSET_ICONS.get(newAsset.get("TYPE"))))
            assetItem.setText(newAsset.get("NAME"))
            self._ui.assetList.addItem(assetItem)

        self._ui.assetList.sortItems()
