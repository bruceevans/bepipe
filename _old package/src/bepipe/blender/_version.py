
import os
import bpy


class Version():

    def __init__(self):
        self.asset = getAssetName()
        self.projectDirectory = getProjectDirectory()
        self.versionFolder = self._getVersionFolder()
        self.nextVersion = self._getNextVersion()
        self.tempVersionFile = self._saveTempFile()

    def createVersion(self):
        """ Increment the current version
        """


def getAssetName():
    """ Return the base name for the asset
    """

def getProjectDirectory():
    """ Return the directory of the mesh file
    """