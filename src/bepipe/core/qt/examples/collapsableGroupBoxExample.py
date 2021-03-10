import sys

sys.path.append("D:\\Projects\\dev\\packages\\bepipe\\src\\")

import bepipe.core.qt.themes as themes
from collapsableGroupBox import CollapsableGroupBox
from PySide2 import QtGui, QtCore, QtWidgets

print(QtGui.__file__)

class Example(QtWidgets.QWidget):

    def __init__(self,):
        super(Example, self).__init__()
        
        self.initUI()

    def initUI(self):

        # formatting
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Example")

        self.controlGroup = CollapseableGroupBox()
        self.controlGroup.setTitle("Group")

        # groupbox layout
        self.groupLayout = QtWidgets.QGridLayout(self.controlGroup)
        self.btn = QtWidgets.QPushButton("FOO")
        self.groupLayout.addWidget(self.btn)
        self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())
        
        # layout
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.addWidget(self.controlGroup)
        self.show()
        # initialize the groupbox
        self.controlGroup.toggleGroup()
            
# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(themes.setDark())
    ex = Example()
    sys.exit(app.exec_())