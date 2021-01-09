from . import bep_utils
import os
import bpy

def saveWorkingfile(asset, path):

    # path to directory
    path = os.path.dirname(path)

    #  Is this a valid path and asset?
    if asset != None and validAssetPath(asset, path):
        blendPath = path + "\\" + asset + "_mesh_main.blend"
        bep_utils.saveBlenderFile(blendPath)
        return True
    else:
        return False

def validAssetPath(asset, directory):
    return directory.endswith(asset)
