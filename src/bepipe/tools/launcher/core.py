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
import qdarkstyle
import qdarkgraystyle
import bepipe.core.utility.extracticon as extracticon

from PySide2 import QtCore, QtWidgets

from .ui import BeLauncherTrayIcon


class BeLauncher(QtCore.QObject):
    """ Main launcher control
    """

    _launch = QtCore.Signal(str) # contains the path to the app being launched

    def __init__(self):
        super(BeLauncher, self).__init__()

        self._ui = BeLauncherTrayIcon()
