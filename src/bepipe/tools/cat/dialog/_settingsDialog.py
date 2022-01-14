
from PySide2 import QtCore, QtGui, QtWidgets

from ..api import _constants


class SettingsDialog(QtWidgets.QDialog):
    """Settings dialog to customize and edit CAT
    """

    def __init__(self, app, parent=None):
        super(SettingsDialog, self).__init__(parent=parent)

        # TODO 'app' will hold the theme once that's made
        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)



    def _setupUi(self):
        """UI Init
        """

        layout = QtWidgets.QVBoxLayout()

        # Tabs? General, Perforce, DCC?

        self.setWindowTitle("CAT Settings")
        self.setWindowIcon(self.icon)

        self._tabWidget = QtWidgets.QTabWidget()


class SettingsTab(QtWidgets.QWidget):
    """Template for a settings tab
    """

    def __init__(self, parent=None):
        super(SettingsTab, self).__init__(parent=parent)
        self.setupUi()

    @property
    def title(self):
        """(str) Tab title"""

    @property
    def description(self):
        """(str) Tab description"""

    def setupUi(self):
        """Initialize the tab's UI"""
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)


class GeneralTab(SettingsTab):
    """General CAT Settings
    """

    def __init__(self, parent=None):
        super(GeneralTab, self).__init__(parent=parent)


class PerforceTab(SettingsTab):
    """General CAT Settings
    """

    def __init__(self, parent=None):
        super(PerforceTab, self).__init__(parent=parent)

    def setupUi(self):
        """Init UI"""

        # P4 Status
        # Current workspace line edit
        # Open P4V

class DCCTab(SettingsTab):
    """User DCC Settings
    """

    # TODO try an autopopulate sorter wizard

    # Wizard button
    # Label, TextEdit, Button widget
    # Mesh: | Path/To/DCC/Software.app |  | Choose App |

        
