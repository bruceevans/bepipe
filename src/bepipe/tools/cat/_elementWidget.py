
from PySide2 import QtCore, QtGui, QtWidgets

class ElementWidget(QtWidgets.QWidget):
    """ Widget containing an element list and
    info about the file status from perforce
    """

    # TODO use the list view's on selected signal

    def __init__(self, parent=None):
        super(ElementWidget, self).__init__(parent)

        mainLayout = QtWidgets.QHBoxLayout()

        elementLayout = QtWidgets.QVBoxLayout()
        elementGroup = QtWidgets.QGroupBox("Elements")
        elementList = QtWidgets.QListView()
        elementLayout.addWidget(elementList)
        elementGroup.setLayout(elementLayout)

        infoGroup = QtWidgets.QGroupBox("Status")
        # TODO large icon
        infoLayout = QtWidgets.QHBoxLayout()
        titleLayout = QtWidgets.QVBoxLayout()
        statusLayout = QtWidgets.QVBoxLayout()

        versionLabel = QtWidgets.QLabel("Version: ")
        versionLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.version = QtWidgets.QLabel("V00")
        self.version.setAlignment(QtCore.Qt.AlignLeft)
        titleLayout.addWidget(versionLabel)
        statusLayout.addWidget(self.version)

        userLabel = QtWidgets.QLabel("User: ")
        userLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.user = QtWidgets.QLabel("Bevans")
        self.user.setAlignment(QtCore.Qt.AlignLeft)
        titleLayout.addWidget(userLabel)
        statusLayout.addWidget(self.user)

        dateLabel = QtWidgets.QLabel("Date: ")
        dateLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.date = QtWidgets.QLabel("00/00/0000")
        self.date.setAlignment(QtCore.Qt.AlignLeft)
        titleLayout.addWidget(dateLabel)
        statusLayout.addWidget(self.date)

        infoLayout.addLayout(titleLayout)
        infoLayout.addLayout(statusLayout)
        infoGroup.setLayout(infoLayout)

        mainLayout.addWidget(elementGroup)
        mainLayout.addWidget(infoGroup)

        # hor layout contain listview and info group
