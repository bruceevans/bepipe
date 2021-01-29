#---------------------------------------------------------------------#
# Author: Bruce Evans, brucein3d@gmail.com
# Copyright 2021 Bruce Evans
# BeP Launcher
#---------------------------------------------------------------------#

import os
import json
import psutil
import ctypes
import subprocess
import configparser
import webbrowser

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.utility.helpers as utils
import bepipe.core.utility.extracticon as extracticon
from ui import BeLauncherUI

_APPLICATION_PATH = utils.getApplicationPath(__file__)
_STORED_APPS = _APPLICATION_PATH + "\\resources\\apps.json"


class BeLauncher(QtCore.QObject):
    """ Main launcher control
    """


    def __init__(self):
        super(BeLauncher, self).__init__()
        self.apps = []
        self.laucherActions = []

        self._ui = BeLauncherUI()
        self._connectWidgets()

        self._refreshView()

    def _connectWidgets(self):
        """ Connect core to ui
        """
        self._ui._WRITE_JSON.connect(self._writeAppToJson)

    def _getAppsFromJson(self, jsonFile):
        """ Get apps from json list
        """
        with open(jsonFile, 'r') as j:
            apps = json.load(j)
        if apps:
            apps = sorted(apps, key=lambda i: i['tag'])
        return apps

    def _getSettings(self):
        """ Read settings from JSON or Python?
        """

    def _openExplorerWindow(self):
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        subprocess.Popen('explorer ' + desktop)

    def _refreshView(self):

        # clear old buttons
        self.laucherActions.clear()

        # clear script and folder actions
        for action in self._ui.launchMenu.actions():
            self._ui.launchMenu.removeAction(action)

        apps = self._getAppsFromJson(_STORED_APPS)

        # sort new tags
        self._ui.tags = sorted(self._ui.tags)
        tagLists = []

        for tag in self._ui.tags:
            tagLists.append([])

        for i in range(len(self._ui.tags)):
            for app in apps:
                try:
                    t = app.get("tag")
                    if t == self._ui.tags[i]:
                        tagLists[i].append(app)
                except KeyError:
                    print("No tag for {}".format(app.get("name")))

        # Sort by name

        for i in range(len(tagLists)):
            tagLists[i] = sorted(tagLists[i], key=lambda x: x['name'])

        spacers = []

        for i in range(len(tagLists)):
            spacers.append(-1)
            for j in range(len(tagLists[i])):
                action = LauncherAction(tagLists[i][j].get("directory"), tagLists[i][j].get("tag"), name=tagLists[i][j].get("name"))
                self.laucherActions.append(action)
                spacers.append(action)
        
        for i in range(len(spacers)):
            if spacers[i] == -1:
                self._ui.launchMenu.addSeparator()
            else:
                action = self._ui.launchMenu.addAction(spacers[i].name)
                action.setIcon(QtGui.QIcon(
                    spacers[i].icon
                ))
                action.triggered.connect(spacers[i].launch)

        # TODO add batch files

        # Add the folder button
        self._ui.launchMenu.addSeparator()
        folderAction = self._ui.launchMenu.addAction("Explorer Window")
        folderAction.triggered.connect(self._openExplorerWindow)
        folderAction.setIcon(QtGui.QIcon(_APPLICATION_PATH + "\\resources\\icons\\icon_folder.png"))

        # Add settings and stuff here?

    def _writeAppToJson(self, launcher):
        """ Save the app list to the resources json file
        """
        self.apps = []

        appDict = {
            "name": launcher.get("name"),
            "directory": launcher.get("directory"),
            "tag": launcher.get("tag")
        }

        jsonFile = _STORED_APPS
        apps = self._getAppsFromJson(jsonFile)
        apps.append(appDict)
        # sort by tag
        self.apps = sorted(apps, key=lambda i: i['tag'])

        # write to json
        with open(jsonFile, 'w') as j:
            json.dump(apps, j, indent=4)

        self._refreshView()


class LauncherAction(QtWidgets.QAction):

    _message = QtCore.Signal(str)

    def __init__(self, path, tag, name = None):
        super(LauncherAction, self).__init__()

        self._path = path
        self._exe = self.getApplication(self._path)

        if name:
            self._name = name
        else:
            self._name = self._exe.replace(".exe", "")

        self._tag = tag
        self.icon = self.getIcon(_APPLICATION_PATH, self._name)
        if not os.path.exists(self.icon):
            extracticon.getIcon(self._path, self.icon)

    @staticmethod
    def getIcon(path, iconName):
        return "{}\\resources\\icons\\icon_{}.png".format(path, iconName)

    @staticmethod
    def getApplication(appPath):
        return os.path.basename(appPath)

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
                # TODO new thread
                # subprocess.run(self._path)
                subprocess.Popen([self._path])
            else:
                self._message.emit("Oops! {} is already running".format(self._exe))
