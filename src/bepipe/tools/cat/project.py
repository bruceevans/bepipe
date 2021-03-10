# Project file reading and writing

import os

import jsonUtilities

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

    return jsonUtilities.writeJson(projectName, projectDict)

def getProjectContents(projectFile):
    """ Get all entries in the project file

        args:
            projectFile (str) path to json project file
        
        returns:
            dict (str) project contens
    """

def openProject(self):
    """ Open existing project json
    """

def writeProjectFile():
    """
    """