
import os
import shutil
import pprint as pprint

from . import _constants
from . import _jsonutils

import bepipe.core.path as path


_PREFERENCES_PATH = os.path.join(os.path.expanduser('~'), "bepipe/cat")
_GAMEREADY_ELEMENTS = ["animation", "cache", "maps", "mesh", "rig"]
_ASSET_CHANGELIST_DESCRIPTION = "Added template files for {}"
_PROJECT_CHANGELIST_DESCRIPTION = "Added new project file: {}"


class CAT(object):
    """API for creating assets in Cat
    """
    def __init__(self):
        pass

    #####################
    ## PROJECT METHODS ##
    #####################

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

        # TODO change extension to .cat?

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
        project = projectData[0]["PROJECT"]["PROJECT_NAME"]

        return (projectDirectory, project)

    def createConfig(self, projectDirectory, project):
        """Create a config json in the user's home

        Args:
            projectPath (str): Path to asset json data
            projectName (str): Name of the project

        Returns:
            dict

        """

        # NOTE (bevans)
        # This feels redundant, but there needs to be a local
        # mapping for each project outside of qsetting and perforce
        # this will allow for separate configs per project

        config = {
            "PROJECT": project,
            "PROJECT_NAME": os.path.splitext(project)[0],
            "PROJECT_PATH": projectDirectory
        }

        if not os.path.isdir(_PREFERENCES_PATH):
            os.makedirs(_PREFERENCES_PATH)
        
        prefFile = os.path.join(_PREFERENCES_PATH, project)
        _jsonutils.writeJson(prefFile, config)
        return config

    def getConfig(self, projectDirectory, project):
        """Get the existing config for the project
        
        Args:
            project (str): Project file name, e.g. test-project.json

        Returns:
            dict
        
        """

        print("SEARCHING CONFIG FOR: {}".format(project))
        configFile = os.path.join(_PREFERENCES_PATH, project)
        if not os.path.isfile(configFile):
            print("NO CONFIG FILE, CREATING...")
            self.createConfig(projectDirectory, project)
        return _jsonutils.readJsonFile(configFile)

    ###################
    ## ASSET METHODS ##
    ###################

    def createAsset(self, assetName, assetType, assetElements, assetPath, depotPath, projectPath, project):
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
            projectPath (str): Path to the project's parent directory

        """

        projectDirectory = os.path.dirname(projectPath)

        asset = self.createAssetDict(
            assetName,
            assetType,
            assetPath,
            assetElements,
            project,
            depotPath
            )

        self.createAssetDirectories(projectPath, asset)
        self.writeAssetToFile(projectPath, asset)
        self.createTemplateProjects(projectDirectory, asset)
        return asset

    def deleteAsset(self, projectFile, asset):
        """ Delete an existing asset

            args:
                path (str): path to directory
        """
        self._removeAssetEntry(projectFile, asset)
        assetPath = os.path.join(projectFile, asset['PATH'])
        shutil.rmtree(assetPath)

    def getProjectAssets(self, projectFile):
        """ Get all entries in the project file

            args:
                projectFile (str): Path to local project file
            
            returns:
                dict (str): Project contents
        """

        try:
            assets = _jsonutils.readJsonFile(projectFile)[1].get("ASSETS")
        except IndexError:
            # no assets
            return None
        return assets

    def _createAssetDict(self, assetName, assetType, assetPath, elements, project, depotPath=None):
        """Organize asset data into a dict

            args:
                assetName (str): Name for the asset
                assetType (str): Type of asset
                assetPath (str): Path to asset
                elements (str list): Which elements to create
                project (str): Project name
                depotPath (str): Perforce depot path

            returns:
                dict

        """

        relPath = assetPath.split(project)[1]

        # TODO make sure it's a unix style path
        if relPath.startswith("/"):
            relPath = relPath[1:]

        return {
            "NAME": assetName,
            "TYPE": assetType,
            "ELEMENTS": elements,
            "PATH": relPath,
            "DEPOT_PATH": depotPath
        }

    def _createAssetDirectories(self, projectPath, asset):
        """ Create the folders on disk for the asset

            args:
                projectDirect (str): path to project base folder
                asset (dict): asset and all its info

            returns:
                bool
        """

        projectDirectory = os.path.split(projectPath)[0]
        # Check for the asset type folder, if it doesn't exist, make it
        assetTypeDir = os.path.join(projectDirectory, asset.get("TYPE"))

        if not os.path.isdir(assetTypeDir):
            os.mkdir(assetTypeDir)

        fullAssetPath = os.path.join(projectDirectory, asset["PATH"])
        os.mkdir(fullAssetPath)

        templateDirs = self._getTemplateDirectories()

        for element in asset.get("ELEMENTS"):
            for directory in templateDirs:
                if directory.get("ElementType") == element.lower():
                    # relative path for asset type folder
                    relPath = directory.get("Path")
                    newFolder = os.path.join(fullAssetPath, relPath)
                    newFolder = path.toLinuxPath(newFolder)
                    try:
                        os.makedirs(newFolder)
                        print("Created: {}".format(newFolder))
                    except FileExistsError:
                        continue
        return True

    def _createTemplateProjects(self, projectDirectory, asset):
        """ Move the template projects to their element folders

        Args:
            projectDirectory (str): Path to project dir from config
            asset (dict): Asset info

        """

        # Get the config disk path
        diskPath = os.path.join(projectDirectory, asset.get("PATH"))
        elements = asset.get("ELEMENTS")

        files = []
        
        for element in elements:
            # skip cache and render
            if element == 'cache' or element == 'render':
                continue

            templates = _constants.TEMPLATE_PROJECTS.get(element)
            for template in templates:
                copyFile = os.path.join(diskPath, element, os.path.basename(template))
                files.append(copyFile)
                shutil.copy(template, copyFile)

                # Rename the template file
                newFileName = "{}-{}".format(asset.get("NAME"), os.path.basename(template))
                renameFile = os.path.join(diskPath, element, newFileName)
                os.rename(copyFile, renameFile)

                # NOTE bevans
                # Make a 'gameready' folder, the assets in this folder will follow the game engine conventions (Unity vs Unreal vs other)
                # eg. Unreal - FPSArms, Player, Wall, etc.
                # Unity - fpsarms,  player, wall, etc.

                if element in _GAMEREADY_ELEMENTS:
                    gameReadyDir = os.path.join(diskPath, element, "gameready")
                    if not os.path.isdir(os.path.join(diskPath, element, "gameready")):
                        os.mkdir(gameReadyDir)

            # TODO perforce check in
            # Add to perforce
            # BP4.addNewFiles([files])
            # BP4.submit(_ASSET_CHANGELIST_DESCRIPTION.format(asset.get("NAME")))

    def _getTemplateDirectories(self):
        """ Get the folder structure from the template directory
            json file in the resources folder
        """

        templateData = _jsonutils.readJsonFile(_constants.ASSET_TREE)
        tempDirs = [i for i in templateData if i.get("Type") == "Directory"]
        return tempDirs

    def _removeAssetEntry(self, projectFile, asset):
        """ Remove entry from project file

            args:
                projectFile (str): path to project json
                asset (dict): psset to remove
        """

        projectData = _jsonutils.readJsonFile(projectFile)
        assets = projectData[1].get("ASSETS")
        modifiedAssets = [a for a in assets if a != asset]
        projectData[1]["ASSETS"] = modifiedAssets
        _jsonutils.writeJson(projectFile, projectData)

    def _writeAssetToFile(self, projectFile, asset):
        """ Add a json entry for a new asset

            args:
                projectFile (str): Path to json project file
                asset (str dict): Asset, type, and elements
            
            returns:
                bool
        """

        try:
            projectData = _jsonutils.readJsonFile(projectFile)
        except FileNotFoundError:
            projectData=[]
        
        projectData[1].get('ASSETS').append(asset)
        return _jsonutils.writeJson(projectFile, projectData)


## UTILITY FUNCTIONS ##
# TODO move into cat class

# move to path module
def getListOfFiles(dirName):
    files = []
    for file in os.walk(dirName):
        files.append(file[0])
    return files

def modifyAssetElements():
    """
    """

# TODO move to path module
def openOnDisk(path):
    """ Open the asset in explorer/finder

        args:
            path (str): path to directory
    """
    if os.path.isdir(path):
        os.startfile(path)