
import os
import json
import pprint as pp

from PySide2 import QtCore, QtGui, QtWidgets

from .ui import _dialog
from .utility import _assets
from .utility import _constants
from .utility import _jsonutils
from .utility import _project

import bepipe.core.path as path
import bepipe.core.qt.style as style
import bepipe.core.qt.widgets as bepWidgets

"""
turn this into an API TODO
basic asset creation
NEEDS:
    name,
    type,
    elements,
    path,
    project

"""


class CAT(object):
    """API for creating assets in BēP
    """
    def __init__(self):
        pass

    # create element

    def createAsset(name, type, elements, path, project):
        """ Create an asset on disk

        Creates the correct directories for the asset and all its elements,
        copies the base files to each of the elements, and adds the info to
        the project file

        args:
            name (str): Name of the asset
            type (str): Type of asset (env, char, prop, etc.)
            elements ([str]): Elements used by this asset (mesh, maps, rig, etc.)
            path (str): Path to the asset's base folder
            project (str): Path to the project JSON folder

        """