
import os
import json
import pprint as pp

from PySide2 import QtCore, QtGui, QtWidgets

from . import _assets
from . import _constants
from . import _jsonutils
from . import _project

import bepipe.core.path as path
import bepipe.core.qt.style as style
import bepipe.core.qt.widgets as bepWidgets


_PREFERENCES_PATH = os.path.join(os.path.expanduser('~'), "bepipe/cat")


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
        # empty dict to hold config
        self.config = {}

    ## PROJECT METHODS ##

    def createProject(self, projectPath, projectName):
        """ Create a project json file

            args:
                projectPath (str): path to new project

            returns:
                bool

        """

        projectDict = [
            { "PROJECT": {
                "PROJECT_NAME": projectName,
                "DESCRIPTION": "TODO"
            } 
            },
            {
                "ASSETS": []
            }
        ]

        _jsonutils.writeJson(projectPath, projectDict)

        # BP4.addNewFiles([projectPath])
        # BP4.submit(_PROJECT_CHANGELIST_DESCRIPTION.format(projectPath))

    def openProject(self, projectPath):
        """Open an existing project

        Args:
            projectPath (str): Path to a json project or folder

        Returns:
            tuple

        """

        projectDirectory = os.path.dirname(projectPath)
        projectData = _jsonutils.readJsonFile(projectPath)
        project = projectData["PROJECT"]["PROJECT_NAME"]

        return (projectDirectory, project)

    def createConfig(self, projectDirectory, project):
        """Create a config json in the user's home

        Args:
            projectPath (str): Path to asset json data
            projectName (str): Name of the project

        Returns:
            dict

        """

        config = {
            "PROJECT": project,
            "PROJECT_NAME": os.path.splitext(project),
            "PROJECT_PATH": projectDirectory
        }

        if not os.path.isdir(_PREFERENCES_PATH):
            os.makedirs(_PREFERENCES_PATH)
        
        prefFile = os.path.join(_PREFERENCES_PATH, project)
        _jsonutils.writeJson(prefFile, config)
        return config

    def getConfig(self, project):
        """Get the existing config for the project
        
        Args:
            project (str): Project file name, e.g. test-project.json

        Returns:
            dict
        
        """

        print("SEARCHING CONFIG FOR: {}".format(project))

        configFile = os.path.join(_PREFERENCES_PATH, project)
        return _jsonutils.readJsonFile(configFile)

    ## ASSET METHODS ##

    def createAsset(self, assetName, assetType, assetElements, assetPath, depotPath, project):
        """ Create an asset on disk

        Creates the correct directories for the asset and all its elements,
        copies the base files to each of the elements, and adds the info to
        the project file

        Args:
            name (str): Name of the asset
            type (str): Type of asset (env, char, prop, etc.)
            elements ([str]): Elements used by this asset (mesh, maps, rig, etc.)
            path (str): Path to the asset's base folder
            depotPath (str): Path to asset in perforce depot
            project (str): Path to the project's parent directory

        """

        projectDirectory = os.path.dirname(project)

        asset = _assets.createAssetDict(
            assetName,
            assetType,
            assetElements,
            assetPath,
            depotPath
            )
        _assets.createAssetDirectories(projectDirectory, asset)
        _assets.writeAssetToFile(project, asset)
        _assets.createTemplateProjects(asset)
        return asset


