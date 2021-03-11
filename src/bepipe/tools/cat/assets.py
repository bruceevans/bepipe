# anything that involves reading/writing asset to json files

import os
import shutil
from pprint import pprint

import jsonUtilities
import bepipe.core.utility.path as path

_ASSET_TREE = "resources/asset_tree.json"

def createAssetDict(assetName, assetType, elements, assetPath):
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
        "NAME":assetName,
        "TYPE":assetType,
        "ELEMENTS":elements,
        "PATH":assetPath
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

    templateDirs = _getTemplateDirectories()
    assetPath = os.path.join(projectDirectory, asset.get("NAME"))
    os.mkdir(assetPath)

    for element in asset.get("ELEMENTS"):  # element is an index
        for directory in templateDirs:
            if directory.get("ElementType") == element.lower():
                relPath = directory.get("Path")
                newFolder = os.path.join(assetPath, relPath)
                newFolder = path.toLinuxPath(newFolder)
                try:
                    os.makedirs(newFolder)
                    print("Created: {}".format(newFolder))
                except FileExistsError:
                    continue
    return True

def deleteAssetDirectory(path):
    """ Delete an existing asset

        args:
            path (str): path to directory
    """
    shutil.rmtree(path)

def _getTemplateDirectories():
    """ Get the folder structure from the template directory
        json file in the resources folder
    """

    baseDirectory = os.path.dirname(__file__)
    templateFile = os.path.join(baseDirectory, _ASSET_TREE)
    templateData = jsonUtilities.readJsonFile(templateFile)
    tempDirs = return [i for i in templateData if i.get("Type") == "Directory"]
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

def renameAsset(newName):
    """ Rename all dirs and files in the tree

        args:
            newName (str): new name
    """

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
        projectData = jsonUtilities.readJsonFile(projectFile)
    except FileNotFoundError:
        projectData=[]

    # TODO what if there aren't any assets?
    
    projectData[1].get('ASSETS').append(asset)
    return jsonUtilities.writeJson(projectFile, projectData)
