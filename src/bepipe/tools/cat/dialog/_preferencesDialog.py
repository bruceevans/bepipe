
import os

from PySide2 import QtCore, QtGui, QtWidgets

from bepipe.core.qt.widgets import CollapsableGroupBox
from ..api import _constants


_SKIP_LAUNCHER_ELEMENTS = ["cache"]


class PreferencesDialog(QtWidgets.QDialog):
    """Settings dialog to customize and edit CAT
    """

    savePreferences = QtCore.Signal()

    def __init__(self, settings, parent=None):
        """Dialog to manage app preferences
        
        Args:
            settings (QSettings): QSettings instance
        """
        super(PreferencesDialog, self).__init__(parent=parent)

        self.settings = settings

        # TODO 'app' will hold the theme once that's made
        self.icon = QtGui.QIcon(_constants.WINDOW_ICON)
        self._setupUi()


    def _setupUi(self):
        """UI Init
        """

        layout = QtWidgets.QVBoxLayout()

        # Perforce section
        perforceSection = QtWidgets.QGroupBox("Perforce: ")
        perforceLayout = QtWidgets.QVBoxLayout()

        workspaceLabel = QtWidgets.QLabel("P4 Workspace: ")
        self.workspaceLineEdit = QtWidgets.QLineEdit()
        self.workspaceLineEdit.setToolTip("Copy/paste your perforce workspace")
        perforceLayout.addWidget(workspaceLabel)
        perforceLayout.addWidget(self.workspaceLineEdit)

        serverLabel = QtWidgets.QLabel("P4 Server: ")
        serverLineEdit = QtWidgets.QLineEdit()
        perforceLayout.addWidget(serverLabel)
        perforceLayout.addWidget(serverLineEdit)

        perforceSection.setLayout(perforceLayout)
        layout.addWidget(perforceSection)

        # DCC section
        # dccSection = QtWidgets.QGroupBox("DCC Applications: ")
        # dccLayout = QtWidgets.QVBoxLayout()

        # self.apps = []
        # appLayout = QtWidgets.QVBoxLayout()

        # reset the settings
        # self.settings.setValue("application", [])

        """
        for i, element in enumerate(_constants.ELEMENTS):

            if element in _SKIP_LAUNCHER_ELEMENTS:
                continue

            appWidget = ChooseAppWidget(element.capitalize(), parent=self)
            appWidget.button.setProperty("Index", i)
            appWidget.button.clicked.connect(self._chooseApp)
            # appLayout.addWidget(appWidget)
            self.apps.append(appWidget)

            # dccLayout.addLayout(appLayout)

        appPaths = self.settings.value("applications")

        if appPaths:
            # pre-fill the form
            self._getSettings(appPaths)

        """
        
        # dccSection.setLayout(dccLayout)
        # layout.addWidget(dccSection)

        saveButton = QtWidgets.QPushButton("Save Preferences")
        saveButton.setFixedHeight(40)
        saveButton.clicked.connect(self.close)
        layout.addWidget(saveButton)

        self.setLayout(layout)

        self.setWindowTitle("CAT Settings")
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(500)

    def _getSettings(self, appPaths):
        """Get the user's preferred apps from the settings instance
        
        Returns:
            layout (QLayout)
        """
        # TODO fill the form

        print("RETRIEVING APP SETTINGS: ")
        for i, app in enumerate(appPaths):
            print(app)

    # TODO fuck this
    def _chooseApp(self):
        """Open a file dialog to choose and application"""

        button = self.sender()
        i = button.property("Index")

        # TODO give an index to set the corresponding line edit
        qfd = QtWidgets.QFileDialog()
        applicationPath = QtWidgets.QFileDialog.getOpenFileName(
            qfd,
            ("Choose an application file..."),
            "/Applications",
            filter="APP Files (*.app)"
        )[0]
        if not applicationPath:
            return
        self.apps[i].pathLineEdit.setText(applicationPath)

    # TODO on close, set settings instance (in parent UI)        
    def closeEvent(self, event):
        # TODO save settings
        print("SAVING AND CLOSING")

        """
        appSettings = []
        for app in self.apps:
            if not app.pathLineEdit.text():
                continue
            appSetting = {
                "element": app.element,
                "application": app.pathLineEdit.text()
            }
            print(appSetting)
            appSettings.append(appSetting)

        self.settings.setValue("applications", appSettings)
        """
        self.settings.setValue("perforceWorkspace", self.workspaceLineEdit.text())
        self.savePreferences.emit()
        event.accept()

class ChooseAppWidget(QtWidgets.QWidget):
    """Custom widget to hold a label, lineedit, and button
    """
    def __init__(self, element, parent=None):
        super(ChooseAppWidget, self).__init__(parent=parent)

        self.element = element

        layout = QtWidgets.QHBoxLayout()

        elementLabel = QtWidgets.QLabel(element)
        elementLabel.setFixedWidth(65)
        layout.addWidget(elementLabel)

        self.pathLineEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.pathLineEdit)

        self.button = QtWidgets.QPushButton("Choose App")
        layout.addWidget(self.button)
        self.setLayout(layout)
