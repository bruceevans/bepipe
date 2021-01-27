import os
import sys
import json

import bepipe.core.utility.helpers as utils
from PySide2 import QtCore, QtGui, QtWidgets

_APPLICATION_PATH = utils.getApplicationPath(__file__)
_DEFAULT_TAGS = ["Art", "Code", "Games", "Media", "Productivity", "Web"]


class BeLauncherUI(QtCore.QObject):
    """ Tray icon and windows for Be Launcher
    """

    _WRITE_JSON = QtCore.Signal(str, str)


    def __init__(self):
        super(BeLauncherUI, self).__init__()

        # Blank inits
        self.trayIcon = None
        self.addAppMenu = None
        self.prefsMenu = None

        # Add app vars
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

    def _connectWidgets(self):
        """ Connect the sigs
        """

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

    def appMenu(self, apps):
        menu = QtWidgets.QMenu()
        # for each app, make a button
        print("Made the launch menu")
        for app in apps:
            button = LauncherAction(app.get("path"), app.get("tag"))
            menu.addAction(button)
        return menu

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

    def refresh(self):
        """ Update the app menu
        """

    def _emitJsonInfo(self):
        self._WRITE_JSON.emit(self.newAppPath, self.newTag)
        self.addAppMenu.close()

    ## -- Menus -- ##

    def _addApplicationMenu(self, appPath):
        self.addAppMenu = None
        self.newAppPath = None
        self.newTag = None

        self.addAppMenu = QtWidgets.QDialog()
        self.addAppMenu.setWindowTitle("Add an application")
        self.addAppMenu.setWindowIcon(self.icon)

        mainLayout = QtWidgets.QVBoxLayout()

        labelName = QtWidgets.QLabel("Name:")
        lineName = QtWidgets.QLineEdit()
        
        appName = os.path.splitext(os.path.split(appPath)[1])[0]
        self.newAppPath = appPath

        lineName.setText(appName)
        layoutName = QtWidgets.QHBoxLayout()
        layoutName.addWidget(labelName)
        layoutName.addWidget(lineName)

        labelTag = QtWidgets.QLabel("Tag:")
        checkBoxTag = QtWidgets.QComboBox()

        # TODO lineedit update and dropbox update via local signal

        for tag in self.tags:
            checkBoxTag.addItem(tag)

        layoutTag = QtWidgets.QHBoxLayout()
        layoutTag.addWidget(labelTag)
        layoutTag.addWidget(checkBoxTag)

        labelTag = QtWidgets.QLabel("New tag:")
        lineEditTag = QtWidgets.QLineEdit()

        layoutNewTag = QtWidgets.QHBoxLayout()
        layoutNewTag.addWidget(labelTag)
        layoutNewTag.addWidget(lineEditTag)

        btnLayout = QtWidgets.QHBoxLayout()

        btnAccept = QtWidgets.QPushButton("Ok")  # instantiate here, add to layout later
        btnAccept.clicked.connect(self._emitJsonInfo)
        btnCancel = QtWidgets.QPushButton("Cancel")

        btnLayout.addWidget(btnAccept)
        btnLayout.addWidget(btnCancel)

        mainLayout.addLayout(layoutName)
        mainLayout.addLayout(layoutTag)
        mainLayout.addLayout(layoutNewTag)
        mainLayout.addLayout(btnLayout)

        self.addAppMenu.setFixedWidth(250)
        self.addAppMenu.setLayout(mainLayout)
        self.addAppMenu.show()


class LauncherAction(QtWidgets.QAction):

    # signal for trayIcon.showMessage("msg")
    _message = QtCore.Signal(str)

    def __init__(self, appPath, tag):
        super(LauncherAction, self).__init__()

        self.appPath = appPath
        
        self._exe = os.path.split(appPath)[1] # TODO what if script?
        self._name = self._exe.replace(".exe", "")
        self._tag = tag

        self.icon = "{}\\resources\\icons\\icon_{}.png".format(_APPLICATION_PATH, self._name)

    @property 
    def exe(self):
        return self._exe

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def path(self):
        return self._path

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    def launch(self):
        """ Launch application or run script
        """
        if self._exe:
            if self._exe not in (p.name() for p in psutil.process_iter()):
                subprocess.run(self.appPath)
            else:
                self._message.emit("Oops! {} is already running".format(self._exe))
