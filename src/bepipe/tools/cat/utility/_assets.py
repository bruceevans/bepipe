# anything that involves reading/writing asset to json files

import os
import shutil
from pprint import pprint

import bepipe.core.path as path
from bepipe.core import bepeefour as BP4

from .import _jsonutils
from . import _constants


_ASSET_TREE = "resources/asset_tree.json"

_ASSET_CHANGELIST_DESCRIPTION = "Added template files for {}"


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
        "PATH": assetPath,
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

    # assetPath = os.path.join(projectDirectory, asset.get("assetType"), asset.get("NAME"))
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
        # print(os.path.join(diskPath, element))
        # print(_constants.TEMPLATE_PROJECTS.get(element))

        # skip cache and render
        if element == 'cache' or element == 'render':
            continue

        # TODO make these work the same
        # TODO rename to "NameElement" eg. PlayerMesh, FPSArmsMesh

        # copy unless it maps
        if element == 'maps':
            mapTemplates = _constants.TEMPLATE_PROJECTS.get(element)
            for mapTemplate in mapTemplates:
                copyFile = os.path.join(diskPath, element, os.path.basename(mapTemplate))
                files.append(copyFile)
                shutil.copy(mapTemplate, copyFile)
        else:
            # move the file to the location
            templateFilePath = _constants.TEMPLATE_PROJECTS.get(element)
            templateFile = os.path.basename(templateFilePath)
            copyFile = os.path.join(diskPath, element, templateFile)
            files.append(copyFile)
            shutil.copy(templateFilePath, copyFile)

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
    pprint(files)
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

    # TODO what if there aren't any assets?
    
    projectData[1].get('ASSETS').append(asset)
    return _jsonutils.writeJson(projectFile, projectData)
