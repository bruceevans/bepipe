import os
import sys
import json
import psutil
import subprocess

import bepipe.core.utility.helpers as utils
import bepipe.core.utility.extracticon as extracticon
from PySide2 import QtCore, QtGui, QtWidgets

_APPLICATION_PATH = utils.getApplicationPath(__file__)
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
