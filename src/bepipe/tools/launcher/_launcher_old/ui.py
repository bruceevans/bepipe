import os
import sys
import json
import psutil
import subprocess

import bepipe.core.extracticon as extracticon
from PySide2 import QtCore, QtGui, QtWidgets

def getApplicationPath(pyFile):
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(pyFile)

_APPLICATION_PATH = getApplicationPath(__file__)
_DEFAULT_TAGS = ["Art", "Code", "Games", "Game Dev", "Media", "Productivity", "Utilities", "Web", "zBeP"]


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
        self.apps = []
        self.appName = None
        self.newAppPath = None
        self.newTag = None
        self.newNameAccept = None

        self.appListWidget = None
        self.tagListWidget = None

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
            ("Choose an application or batch script to add"),
            "C:\\",
            "Applications or Batch Script *.exe *.bat")[0]
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
        settingsAction.triggered.connect(self._settingsDialog)

        closeAction = menu.addAction("Close Launcher")
        closeAction.setIcon(QtGui.QIcon("{}\\resources\\icons\\icon_close.png".format(_APPLICATION_PATH)))
        closeAction.triggered.connect(self._closeApp)

        return menu

    ## -- Menus -- ##

    def _addApplicationMenu(self, appPath):
        self.addAppMenu = None
        self.launcherDict = None
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

    def _cancelDialog(self, dialog):
        dialog.reject()

    def _settingsDialog(self):
        self.settingsMenu = QtWidgets.QDialog()
        self.settingsMenu.setWindowTitle("Settings")
        self.settingsMenu.setWindowIcon(self.icon)

        labelApps = QtWidgets.QLabel("Modify Apps")
        self.appListWidget = QtWidgets.QListWidget()
        for app in self.apps:
            newItem = QtWidgets.QListWidgetItem(app.get('name'))
            self.appListWidget.addItem(newItem)

        btnRenameApp = QtWidgets.QPushButton("Rename App")
        # btnRenameApp.clicked.connect(lambda : self._renameApplicationMenu(self.appListWidget))
        btnDeleteApp = QtWidgets.QPushButton("Delete App")
        # btnDeleteApp.clicked.connect(lambda : self._removeApplication(self.appListWidget))

        layoutAppButtons = QtWidgets.QHBoxLayout()
        layoutAppButtons.addWidget(btnRenameApp)
        layoutAppButtons.addWidget(btnDeleteApp)

        labelTags = QtWidgets.QLabel("Modify Tags")
        self.tagListWidget = QtWidgets.QListWidget()
        for tag in self.tags:
            newItem = QtWidgets.QListWidgetItem(tag)
            self.tagListWidget.addItem(newItem)

        btnRenameTag = QtWidgets.QPushButton("Rename Tag")
        # btnRenameTag.clicked.connect(lambda : self._renameTagMenu(self.tagListWidget))
        btnDeleteTag = QtWidgets.QPushButton("Delete Tag")
        # btnDeleteTag.clicked.connect(lambda : self._removeTag(self.tagListWidget))

        layoutTagButtons = QtWidgets.QHBoxLayout()
        layoutTagButtons.addWidget(btnRenameTag)
        layoutTagButtons.addWidget(btnDeleteTag)

        listLayout = QtWidgets.QVBoxLayout()
        listLayout.addWidget(labelApps)
        listLayout.addWidget(self.appListWidget)
        listLayout.addLayout(layoutAppButtons)
        listLayout.addWidget(labelTags)
        listLayout.addWidget(self.tagListWidget)
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

    def _renameApplicationMenu(self, listWidget):

        # clear menu
        del self.renameAppMenu

        self.renameAppMenu = QtWidgets.QDialog()
        self.renameAppMenu.setWindowTitle("Rename an App")
        self.renameAppMenu.setWindowIcon(self.mainIcon)

        labelNewName = QtWidgets.QLabel("New Name: ")
        lineEditName = QtWidgets.QLineEdit()

        layoutNewName = QtWidgets.QHBoxLayout()
        layoutNewName.addWidget(labelNewName)
        layoutNewName.addWidget(lineEditName)

        btnAccept = QtWidgets.QPushButton("Accept")
        btnCancel = QtWidgets.QPushButton("Cancel")

        btnAccept.clicked.connect(lambda : self._renameApplication(self.renameAppMenu, listWidget, lineEditName.text()))
        btnCancel.clicked.connect(lambda : self._cancelDialog(self.renameAppMenu))

        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(btnAccept)
        btnLayout.addWidget(btnCancel)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(layoutNewName)
        mainLayout.addLayout(btnLayout)
        self.renameAppMenu.setLayout(mainLayout)

        self.renameAppMenu.show()

    def _renameApplication(self, dialog, listWidget, newName):
        # update the apps name in the json file and list widget
        selection = listWidget.currentItem()
        if not selection:
            return

        appName = selection.text()
        appList = self._readAppsFromJson()
        for entry in appList:
            if entry.get("name") == appName:
                entry["name"] = newName
        self._writeAppList(appList, self.applicationPath + "\\resources\\apps.json")

        selection.setText(newName)

        # initLaunchButtons
        self._initLauncherButtons()
        dialog.accept()

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
