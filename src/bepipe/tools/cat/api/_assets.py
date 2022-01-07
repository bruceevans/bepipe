# anything that involves reading/writing asset to json files, directories, or template files

import os
import shutil
from pprint import pprint

import bepipe.core.path as path
from bepipe.core import bepeefour as BP4

from .import _jsonutils
from . import _constants


_ASSET_TREE = "resources/asset_tree.json"
_ASSET_CHANGELIST_DESCRIPTION = "Added template files for {}"
_GAMEREADY_ELEMENTS = ["animation", "cache", "maps", "mesh", "rig"]


# TODO store only relative paths in the json
# so we can do os.path.join(PROJECT_PATH, element-relative-path)
# PROJECT_PATH SET IN _project.py

def createAssetDict(assetName, assetType, elements, assetPath, depotPath):
    """ Organize asset data into a dict

        args:
            assetName (str): name for the asset
            assetType (str): type of asset
            elements (str list): which element to create
            assetPath (str): path to asset

        returns:
            dict
    """

    assetDict = {
        "NAME": assetName,
        "TYPE": assetType,
        "ELEMENTS": elements,
        "PATH": assetPath, # TODO make this relative
        "DEPOT_PATH": depotPath
    }

    return assetDict

def createAssetDirectories(projectDirectory, asset):
    """ Create the folders on disk for the asset

        args:
            projectDirect (str): path to project base folder
            asset (dict): asset and all its info

        returns:
            bool
    """

    # Check for the asset type folder, if it doesn't exist, make it
    assetTypeDir = os.path.join(projectDirectory, asset.get("TYPE"))
    if not os.path.isdir(assetTypeDir):
        os.mkdir(assetTypeDir)

    os.mkdir(asset.get("PATH"))
    templateDirs = _getTemplateDirectories()

    for element in asset.get("ELEMENTS"):
        for directory in templateDirs:
            if directory.get("ElementType") == element.lower():
                relPath = directory.get("Path")
                newFolder = os.path.join(asset.get("PATH"), relPath)
                newFolder = path.toLinuxPath(newFolder)
                try:
                    os.makedirs(newFolder)
                    print("Created: {}".format(newFolder))
                except FileExistsError:
                    continue
    return True

def createTemplateProjects(asset):
    """ Move the template projects to their element folders
    """
    diskPath = asset.get("PATH")
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

def deleteAssetDirectory(path):
    """ Delete an existing asset

        args:
            path (str): path to directory
    """
    shutil.rmtree(path)

def getElements(asset):
    return asset.get('ELEMENTS')

def _getListOfFiles(dirName):
    files = []
    for file in os.walk(dirName):
        files.append(file[0])
    return files

def _getTemplateDirectories():
    """ Get the folder structure from the template directory
        json file in the resources folder
    """

    templateData = _jsonutils.readJsonFile(_constants.ASSET_TREE)
    tempDirs = [i for i in templateData if i.get("Type") == "Directory"]
    return tempDirs

def modifyAssetElements():
    """
    """

def openOnDisk(path):
    """ Open the asset in explorer/finder

        args:
            path (str): path to directory
    """
    if os.path.isdir(path):
        os.startfile(path)

def renameAsset(assetPath, oldName, newName):
    """ Rename all dirs and files in the tree

        args:
            newName (str): new name
    """

    # TODO illegal names

    # walk through the dirs and files
    for file in _getListOfFiles(assetPath):
        if oldName in file:
            print("Changing:")
            print(file)
            file.replace(oldName, newName)
            print(file)

    # get the old name and new name
    # walk the tree, any file or directory with that name, replace it

def writeAssetToFile(projectFile, asset):
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
