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

    # _WRITE_JSON = QtCore.Signal(str, str)
    _WRITE_JSON = QtCore.Signal(object)


    def __init__(self):
        super(BeLauncherUI, self).__init__()

        # Blank inits
        self.trayIcon = None
        self.addAppMenu = None
        self.prefsMenu = None

        # Add app vars
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
        # set width?
        self.launchMenu.setFixedWidth(150)

        '''
        self.launchMenu.setStyleSheet(
        """
        QMenu {
        margin: 2px;
        }

        QMenu::item::selected {
            background-color: rgb(42, 130, 218);
        }
        """
        )
        '''

        # formatting leftovers

        """
        border: 2px solid;
        background-color: rgb(49,49,49);
        color: rgb(255,255,255);
        height: 2px;
        margin-left: 10px;
        margin-right: 5px; 
        background: rgb(35, 35, 35);
        """

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

    """
    def appMenu(self, apps):
        menu = QtWidgets.QMenu()
        # for each app, make a button
        print("Made the launch menu")
        for app in apps:
            button = LauncherAction(app.get("directory"), app.get('tag'), name = app.get("name"))
            menu.addAction(button)
        return menu
    """

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

    def path2app(self, path):
        return os.path.split(path)[1]

    def preferencesContextMenu(self):
        menu = QtWidgets.QMenu()

        addApplicationAction = menu.addAction("Add Application")
        addApplicationAction.triggered.connect(self._chooseApplication)

        settingsAction = menu.addAction("Settings")

        aboutAction = menu.addAction("About")

        closeAction = menu.addAction("Close Launcher")
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
        # self.newAppPath = appPath

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

        # launchAction = LauncherAction(appPath, self.newTag)
        # launchAction.name = lineName.text()
        print("APP PATH IS {}".format(appPath))
        launcher = {
            "name": "",
            "directory": appPath,
            # "exe": "",
            # "icon": "",
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

    def _emitAppTag(self, launcher):
        # update the launcher info
        launcher['name'] = self.appName
        launcher['tag'] = self.newTag

        print(launcher.get("directory"))

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
