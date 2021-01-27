#---------------------------------------------------------------------#
# Author: Bruce Evans, brucein3d@gmail.com
# Copyright 2021 Bruce Evans
# BeP Launcher
#---------------------------------------------------------------------#

import os
import sys
import json
import psutil
import subprocess
import configparser
import webbrowser

sys.path.append("D:\\Projects\\dev\\packages\\bepipe\\src\\")

import bepipe.core.utility.helpers as utils
import bepipe.core.utility.extracticon as extracticon

from PySide2 import QtCore, QtWidgets

from ui import BeLauncherUI

_APPLICATION_PATH = utils.getApplicationPath(__file__)


class BeLauncher(QtCore.QObject):
    """ Main launcher control
    """

    _launch = QtCore.Signal(str) # contains the path to the app being launched

    def __init__(self):
        super(BeLauncher, self).__init__()

        self._apps = []

        self._ui = BeLauncherUI()
        self._connectWidgets()

    def _connectWidgets(self):
        """ Connect core to ui
        """
        self._ui.trayIcon.activated.connect(self._onTrayActivated)
        self._ui._WRITE_JSON.connect(self._writeAppsToJson)

    def _addApplication(self, appPath):
        """ Shows the 'add application' window and
            adds an app to the JSON settings file
        """
        print("Adding application: {}".format(appPath))

    def _getAppsFromJson(self):
        """ Get apps from json list
        """
        jsonFile = _APPLICATION_PATH + "\\resources\\apps.json"
        with open(jsonFile, 'r') as j:
            apps = json.load(j)
        apps = sorted(apps, key=lambda i: i['tag'])
        return apps

    def _getSettings(self):
        """ Read settings from JSON or Python?
        """

    def _onTrayActivated(self, reason):
        """ If the tray icon is clicked on
        """

        if reason == self._ui.trayIcon.Trigger:

            print("Clicked on icon")

            launchMenu = self._ui.appMenu(self._apps)
            launchMenu.show()

            trayGeometry = self._ui.trayIcon.geometry()
            launcherMenuGeometry = launchMenu.frameGeometry()
            centerPoint = trayGeometry.center()

            launcherMenuGeometry.moveBottomLeft(centerPoint)
            launchMenu.move(launcherMenuGeometry.topLeft())
            launchMenu.show()

    def _writeAppsToJson(self, path, tag):
        """ Save the app list to the resources json file
        """
        print(path)
        print(tag)

        # check if tag exists, if not append it

        # TODO get existing json data
        # Add new entry to it
        # sort by tag

        """
        with open(jsonFile, 'w') as j:
            json.dump(apps, j, indent=4)
        """
