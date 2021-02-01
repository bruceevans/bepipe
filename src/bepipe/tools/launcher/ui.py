import os
import sys
import json
import psutil
import subprocess

import bepipe.core.utility.helpers as utils
import bepipe.core.utility.extracticon as extracticon
from PySide2 import QtCore, QtGui, QtWidgets

_APPLICATION_PATH = utils.getApplicationPath(__file__)
_DEFAULT_TAGS = ["Art", "Code", "Games", "Game Dev", "Media", "Productivity", "Utilities", "Web"]


class BeLauncherUI(QtCore.QObject):
    """ Tray icon and windows for Be Launcher
    """

    _WRITE_JSON = QtCore.Signal(object)


    def __init__(self):
        super(BeLauncherUI, self).__init__()

        # Blank inits
        self.trayIcon = None
        self.addAppMenu = None
        self.settingsMenu = None

        # Add app vars
        self.apps = []
        self.appName = None
        self.newAppPath = None
        self.newTag = None

        self.icon = QtGui.QIcon("{}\\resources\\icons\\launcher_icon.png".format(_APPLICATION_PATH))
        self.tags = _DEFAULT_TAGS

        self._setupUI()
        self._connectWidgets()

    def _setupUI(self):
        """ Setup menus for options
        """
        ## Tray icon setup
        self.trayIcon = QtWidgets.QSystemTrayIcon()
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setContextMenu(self.preferencesContextMenu())
        self.trayIcon.show()

        self.launchMenu = QtWidgets.QMenu()
        self.launchMenu.setStyleSheet(r"QMenu::separator { height: 2px; background: rgb(35, 35, 35); }")
        self.launchMenu.setFixedWidth(150)

    def _connectWidgets(self):
        """ Connect the sigs
        """
        self.trayIcon.activated.connect(self._onTrayActivated)

    def _chooseApplication(self):

        fileDialog = QtWidgets.QFileDialog()
        appPath = fileDialog.getOpenFileName(
            fileDialog,
            ("Choose an application to add"),
            "C:\\",
            "Applications (*.exe)")[0]
        if appPath:
            self._addApplicationMenu(appPath)

    def _closeApp(self):
        QtCore.QCoreApplication.exit()

    def _onTrayActivated(self, reason):
        """ If the tray icon is clicked on
        """

        if reason == self.trayIcon.Trigger:
            self.launchMenu.show()

            trayGeometry = self.trayIcon.geometry()
            launcherMenuGeometry = self.launchMenu.frameGeometry()
            centerPoint = trayGeometry.center()

            launcherMenuGeometry.moveBottomLeft(centerPoint)
            self.launchMenu.move(launcherMenuGeometry.topLeft())
            self.launchMenu.show()

    def preferencesContextMenu(self):
        menu = QtWidgets.QMenu()

        addApplicationAction = menu.addAction("Add Application")
        addApplicationAction.setIcon(QtGui.QIcon("{}\\resources\\icons\\icon_add.png".format(_APPLICATION_PATH)))
        addApplicationAction.triggered.connect(self._chooseApplication)

        settingsAction = menu.addAction("Settings")
        settingsAction.setIcon(QtGui.QIcon("{}\\resources\\icons\\icon_settings.png".format(_APPLICATION_PATH)))
        settingsAction.triggered.connect(self._settingsMenu)

        aboutAction = menu.addAction("About")
        aboutAction.setIcon(QtGui.QIcon("{}\\resources\\icons\\icon_info.png".format(_APPLICATION_PATH)))
        aboutAction.triggered.connect(self._aboutMenu)

        closeAction = menu.addAction("Close Launcher")
        closeAction.setIcon(QtGui.QIcon("{}\\resources\\icons\\icon_close.png".format(_APPLICATION_PATH)))
        closeAction.triggered.connect(self._closeApp)

        return menu

    ## -- Menus -- ##

    def _addApplicationMenu(self, appPath):
        self.addAppMenu = None
        self.addAppMenu = QtWidgets.QDialog()
        self.addAppMenu.setWindowTitle("Add an application")
        self.addAppMenu.setWindowIcon(self.icon)

        mainLayout = QtWidgets.QVBoxLayout()

        labelName = QtWidgets.QLabel("Name:")
        lineName = QtWidgets.QLineEdit()
        lineName.textChanged[str].connect(self._setNameFromLineEdit)
        
        self.appName = os.path.splitext(os.path.split(appPath)[1])[0]

        lineName.setText(self.appName)
        layoutName = QtWidgets.QHBoxLayout()
        layoutName.addWidget(labelName)
        layoutName.addWidget(lineName)

        labelTag = QtWidgets.QLabel("Tag:")
        tagCombo = QtWidgets.QComboBox()

        for tag in self.tags:
            tagCombo.addItem(tag)

        self.newTag = self.tags[tagCombo.currentIndex()]
        tagCombo.currentIndexChanged.connect(self._setTagFromComboBox)

        layoutTag = QtWidgets.QHBoxLayout()
        layoutTag.addWidget(labelTag)
        layoutTag.addWidget(tagCombo)

        labelTag = QtWidgets.QLabel("New tag:")
        lineEditTag = QtWidgets.QLineEdit()
        lineEditTag.textChanged[str].connect(self._setTagFromLineEdit)

        layoutNewTag = QtWidgets.QHBoxLayout()
        layoutNewTag.addWidget(labelTag)
        layoutNewTag.addWidget(lineEditTag)

        launcher = {
            "name": "",
            "directory": appPath,
            "tag": ""
        }

        btnLayout = QtWidgets.QHBoxLayout()
        btnAccept = QtWidgets.QPushButton("Ok")
        btnAccept.clicked.connect(lambda:self._emitAppTag(launcher))
        btnCancel = QtWidgets.QPushButton("Cancel")
        btnCancel.clicked.connect(self.addAppMenu.close)

        btnLayout.addWidget(btnAccept)
        btnLayout.addWidget(btnCancel)

        mainLayout.addLayout(layoutName)
        mainLayout.addLayout(layoutTag)
        mainLayout.addLayout(layoutNewTag)
        mainLayout.addLayout(btnLayout)

        self.addAppMenu.setFixedWidth(250)
        self.addAppMenu.setLayout(mainLayout)
        self.addAppMenu.show()

    def _settingsMenu(self):
        print("Clicked on settings button")

        self.settingsMenu = QtWidgets.QDialog()
        self.settingsMenu.setWindowTitle("Settings")
        self.settingsMenu.setWindowIcon(self.icon)

        labelApps = QtWidgets.QLabel("Modify Apps")

        appList = QtWidgets.QListWidget()

        for app in self.apps:
            newItem = QtWidgets.QListWidgetItem(app.get('name'))
            appList.addItem(newItem)

        # TODO connect, no lambda
        btnRenameApp = QtWidgets.QPushButton("Rename App")
        # btnRenameApp.clicked.connect(lambda : self._renameApplicationMenu(appList))
        btnDeleteApp = QtWidgets.QPushButton("Delete App")
        # btnDeleteApp.clicked.connect(lambda : self._removeApplication(appList))

        layoutAppButtons = QtWidgets.QHBoxLayout()
        layoutAppButtons.addWidget(btnRenameApp)
        layoutAppButtons.addWidget(btnDeleteApp)
        
        labelTags = QtWidgets.QLabel("Modify Tags")
        listTags = QtWidgets.QListWidget()
        for tag in self.tags:
            newItem = QtWidgets.QListWidgetItem(tag)
            listTags.addItem(newItem)

        # TODO connect, no lambda
        btnRenameTag = QtWidgets.QPushButton("Rename Tag")
        # btnRenameTag.clicked.connect(lambda : self._renameTagMenu(listTags))
        btnDeleteTag = QtWidgets.QPushButton("Delete Tag")
        # btnDeleteTag.clicked.connect(lambda : self._removeTag(listTags))

        layoutTagButtons = QtWidgets.QHBoxLayout()
        layoutTagButtons.addWidget(btnRenameTag)
        layoutTagButtons.addWidget(btnDeleteTag)

        listLayout = QtWidgets.QVBoxLayout()
        listLayout.addWidget(labelApps)
        listLayout.addWidget(appList)
        listLayout.addLayout(layoutAppButtons)
        listLayout.addWidget(labelTags)
        listLayout.addWidget(listTags)
        listLayout.addLayout(layoutTagButtons)

        btnAccept = QtWidgets.QPushButton("OK")
        # btnAccept.clicked.connect(lambda : self._acceptDialog(self.settingsMenu))

        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(btnAccept)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(listLayout)
        mainLayout.addLayout(btnLayout)

        self.settingsMenu.setLayout(mainLayout)
        self.settingsMenu.show()

    def _aboutMenu(self):
        print("Clicked on about menu")

    def _emitAppTag(self, launcher):
        # update the launcher info
        launcher['name'] = self.appName
        launcher['tag'] = self.newTag

        # check if tag exists, if not append it
        if self.newTag not in self.tags:
            self.tags.append(self.newTag)

        self._WRITE_JSON.emit(launcher)
        self.addAppMenu.close()

    def _setNameFromLineEdit(self, name):
        self.appName = name

    def _setTagFromComboBox(self, index):
        self.newTag = self.tags[index]

    def _setTagFromLineEdit(self, tag):
        self.newTag = tag
