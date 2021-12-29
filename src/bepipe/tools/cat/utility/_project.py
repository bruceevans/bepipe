# Project file reading and writing

import os
from pprint import pprint

from . import _jsonutils
from bepipe.core import bepeefour as BP4


_PROJECT_CHANGELIST_DESCRIPTION = "Added new project file: {}"


def createProject(projectPath, projectName):
    """ Create a project json file

        args:
            projectPath (str): path to new project

        returns:
            bool
    """

    projectDict = [
        { "PROJECT": {
            "PATH": os.path.dirname(projectPath)
        } 
        },
        {
            "ASSETS": []
        }
    ]

    _jsonutils.writeJson(projectPath, projectDict)
    # BP4.addNewFiles([projectPath])
    # BP4.submit(_PROJECT_CHANGELIST_DESCRIPTION.format(projectPath))
    return True

def getProjectAssets(projectFile):
    """ Get all entries in the project file

        args:
            projectFile (str): path to json project file
        
        returns:
            dict (str): project contens
    """

    try:
        assets = _jsonutils.readJsonFile(projectFile)[1].get("ASSETS")
    except IndexError:
        # no assets
        return None
    return assets

def openExistingProject():
    """ Open existing project json
    """

def removeAssetEntry(projectFile, asset):
    """ Remove entry from project file

        args:
            projectFile (str): path to project
            asset (dict): psset to remove
    """

    projectData = _jsonutils.readJsonFile(projectFile)
    assets = projectData[1].get("ASSETS")
    modifiedAssets = [a for a in assets if a != asset]
    projectData[1]["ASSETS"] = modifiedAssets
    _jsonutils.writeJson(projectFile, projectData)

def renameAssetEntry(newName):
    """
        Change the "NAME" key to the given value

        args:
            newName (str): new name
    """

def writeProjectFile():
    """
    """