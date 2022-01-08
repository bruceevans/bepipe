
# Project file reading and writing, should be small, no asset writing

import os
import getpass

from ..api import _jsonutils
from bepipe.core import bepeefour as BP4


_PROJECT_CHANGELIST_DESCRIPTION = "Added new project file: {}"

# TODO when creating a project, what happens? Auto create a folder?
# Or put a json an existing folder? <- current

# TODO store the project path where? For a single person working in perforce keeping it in a json is fine
# otherwise do we need a config stored somewhere locally? Or maybe keep the json stored locally in documents
# or something, if it's not there, create it?

# TODO migrate project?
# TODO delete project?
# TODO sync and init project? Different machine with different project path?

def createProject(projectPath, projectName):
    """ Create a project json file

        args:
            projectPath (str): path to new project

        returns:
            bool
    """

    # store the project file in user/documents/betools/cat

    

    projectDict = [
        { "PROJECT": {
            "PROJECT_NAME": projectName,
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

# TODO move
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

# TODO move to asset

