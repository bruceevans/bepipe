import os
import shutil
import bpy

SAVE_VERSIONS = ".versions.blend"
PUBLISH_FOLDER = "_published"

def getCurrentVersion(path):
    """ Return the base name of the asset

        Args:
            path (str): path of the current blender file
    """

    blendFiles = [f for f in os.listdir(path) if f.endswith('.blend')]
    # blendFiles = blendFiles.sort()
    
    if len(blendFiles) > 1:
        return int(blendFiles[-1][-9:-6])
    elif len(blendFiles) == 1:
        return int(blendFiles[0][-9:-6])
    else:
        # print("Nothing in the versions folder")
        return 0

def getProjectDirectory():
    """ Get the directory containing the open .blend file
    """

    return os.path.dirname(getProjectPath())

def getProjectPath():
    """ Get the current filepath of the open .blend file
    """

    return bpy.data.filepath

def incrementVersion(previousVersion):
    """ Return the next version as a string i.e. 006

        Args:
            previousVersion (int): last version int
    """

    newVersion = previousVersion + 1
    newVersion = str(newVersion).zfill(3)  # 3 leading zeroes
    return newVersion

def saveBlenderFile(path):
    """ Saves the open blender project to the given path, include project name.blend

        Args:
            path (str): Save destination path
    """
    try:
        bpy.ops.wm.save_as_mainfile(filepath = path)  # save to a .blend file
        return True
    except OSError:
        # print("Couldn't save the file. Manually save your project")
        return False

def versionFolderExists(path):
    """ Check if the version folder exists

        Args:
            path (str): path to versions folder
    """
    return os.path.isdir(path)