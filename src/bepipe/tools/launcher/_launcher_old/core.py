#---------------------------------------------------------------------#
# Author: Bruce Evans, brucein3d@gmail.com
# Copyright 2021 Bruce Evans
# BeP Launcher
#---------------------------------------------------------------------#

import os
import sys
import json
import psutil
import ctypes
import subprocess
import configparser
import webbrowser

from PySide2 import QtCore, QtGui, QtWidgets

import bepipe.core.extracticon as extracticon
from ui import BeLauncherUI

def getApplicationPath(pyFile):
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(pyFile)

_APPLICATION_PATH = getApplicationPath(__file__)
_STORED_APPS = _APPLICATION_PATH + "\\resources\\apps.json"
_MODULE_PATH = _APPLICATION_PATH.split('launcher')[0]
_CAT = "{}\\cat\\resources\\runCat.bat".format(_MODULE_PATH)


class BeLauncher(QtCore.QObject):
    """ Main launcher control
    """
    def __init__(self):
        super(BeLauncher, self).__init__()

        self._worker = None
        self._thread = None

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

        # update view data
        self._ui.apps = apps

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

        actionList = []

        for i in range(len(tagLists)):
            actionList.append(None)
            for j in range(len(tagLists[i])):
                action = LauncherAction(tagLists[i][j].get("directory"), tagLists[i][j].get("tag"), name=tagLists[i][j].get("name"))
                self.laucherActions.append(action)
                actionList.append(action)

        for i in range(len(actionList)):
            if actionList[i]:
                # get the file type for exe/bat test
                action = self._ui.launchMenu.addAction(actionList[i].name)
                action.setIcon(QtGui.QIcon(
                    actionList[i].icon
                ))
                action.triggered.connect(actionList[i].launch)
            else:
                self._ui.launchMenu.addSeparator()

        # Add pipeline stuff here?
        self._ui.launchMenu.addSeparator()
        catAction = self._ui.launchMenu.addAction("CAT - BēP")
        catAction.triggered.connect(self._runCAT)
        catAction.setIcon(QtGui.QIcon(_APPLICATION_PATH + "\\resources\\icons\\icon_CAT.png"))

        # Add the folder button
        self._ui.launchMenu.addSeparator()
        folderAction = self._ui.launchMenu.addAction("Explorer Window")
        folderAction.triggered.connect(self._openExplorerWindow)
        folderAction.setIcon(QtGui.QIcon(_APPLICATION_PATH + "\\resources\\icons\\icon_folder.png"))

    def _runCAT(self):
        subprocess.Popen([_CAT])

    def _writeAppToJson(self, launcher):
        """ Save the app list to the resources json file
        """
        self._ui.apps = []

        appDict = {
            "name": launcher.get("name"),
            "directory": launcher.get("directory"),
            "tag": launcher.get("tag")
        }

        jsonFile = _STORED_APPS
        apps = self._getAppsFromJson(jsonFile)
        apps.append(appDict)
        # sort by tag
        self._ui.apps = sorted(apps, key=lambda i: i['tag'])

        # write to json
        with open(jsonFile, 'w') as j:
            json.dump(apps, j, indent=4)

        self._refreshView()


class LauncherAction(QtWidgets.QAction):

    _message = QtCore.Signal(str)
    _FILE_TYPES = [".exe", ".bat"]

    def __init__(self, path, tag, name = None):
        super(LauncherAction, self).__init__()

        self._path = path

        # not actually exe, could be .bat
        self._exe = self.getApplication(self._path)

        if name:
            self._name = name
        else:
            self._name = self._exe.replace(".exe", "")

        self._tag = tag

        if os.path.splitext(self._exe)[1] == '.bat':
            self.icon = self.getIcon(_APPLICATION_PATH, 'Script')
        else:
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
            if os.path.splitext(self._exe)[1] in self._FILE_TYPES:
                if self._exe not in (p.name() for p in psutil.process_iter()):
                    subprocess.Popen([self._path], shell=True)
                else:
                    self._message.emit("Oops! {} is already running".format(self._exe))
            else:
                return


class LaunchApplication(QtCore.QObject):

    def __init__(self, parent = None):
        super(LaunchApplication, self).__init__(parent=parent)

    def run(self, app):
        try:
            subprocess.run(app, shell=True)
        except BaseException as e:
            print(e)
