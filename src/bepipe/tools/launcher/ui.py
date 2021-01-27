

import bepipe.core.utility.helpers as utils
from PySide2 import QtCore, QtGui, QtWidgets


class BeLauncherTrayIcon(QtWidgets.QSystemTrayIcon):
    """ Tray icon for launcher gui
    """

    _APPLICATION_PATH = utils.getApplicationPath()

    def __init__(self):
        super(BeLauncherTrayIcon, self).__inti__()

        self.apps = []
        self.appMenu = self.contextMenu()
        self.prefsMenu = None
        self.icon = QtGui.QIcon(self._APPLICATION_PATH + "\\resources\\icons\\launcher_icon.png")

    def _setupUI(self):
        """ Setup menus for options
        """

    def _connectWidgets(self):
        """ Connect the sigs
        """

    def contextMenu(self):
        menu = QtWidgets.QMenu()
        # for each app, make a button
        return menu

    def preferencesContextMenu(self):
        menu = QtWidgets.QMenu()
        # for each app, make a button
        return menu
