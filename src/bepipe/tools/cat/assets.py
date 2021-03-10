# anything that involves reading/writing asset to json files

import os
from pprint import pprint

import jsonUtilities
import bepipe.core.utility.path as path

_ASSET_TREE = "resources/asset_tree.json"

def createAssetDict(assetName, assetType, elements, assetPath):
    """ Organize asset data into a dict
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
            # TODO may need to rethink this, maybe add an element key to each asset dir in template file
            if directory.get("Path").find(element.lower()) != -1:
                relPath = directory.get("Path")
                newFolder = os.path.join(assetPath, relPath)
                newFolder = path.toLinuxPath(newFolder)
                try:
                    os.makedirs(newFolder)
                    print("Created: {}".format(newFolder))
                except FileExistsError:
                    continue
    return True

def deleteAsset():
    """ Delete an existing asset
    """

def getExistingAssets(projectFile):
    """ Return a list of assets in a project

        args:
            projectFile (str) path to json project file
            type (bool) return asset type in the list

        returns:
            dict list: asset names (and type)
    """

    # All assets are in an "ASSETS" key in the project file
    projectData = jsonUtilities.readJsonFile(projectFile)
    assets = projectData[1].get("ASSETS")
    return assets

def modifyAssetName():
    """
    """

def modifyAssetElements():
    """
    """

def openOnDisk():
    """
    """

def writeAssetToFile(projectFile, asset):
    """ Add a json entry for a new asset

        args:
            projectFile (str): Path to json project file
            asset (str dict): Asset, type, and elements
        
        returns:
            bool
    """

    projectData = jsonUtilities.readJsonFile(projectFile)
    pprint(projectData)
    pprint(projectData[1])
    projectData[1].get('ASSETS').append(asset)
    return jsonUtilities.writeJson(projectFile, projectData)

def _getTemplateDirectories():
    """ Get the folder structure from the template directory
        json file in the resources folder
    """
    baseDirectory = os.path.dirname(__file__)
    templateFile = os.path.join(baseDirectory, _ASSET_TREE)

    templateData = jsonUtilities.readJsonFile(templateFile)

    templateDirs = []
    for obj in templateData:
        if obj.get("Type") == "Directory":
            templateDirs.append(obj)
    return templateDirs

