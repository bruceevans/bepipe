
import os
import sys

def toLinuxPath(path):
    return path.replace("\\", "/")

def toWindowsPath(path):
    return path.replace("/", "\\")

def getPlatform():
    if sys.platform == 'win32':
        return 'WINDOWS'
    elif sys.platform == 'darwin':
        return 'OSX'
    elif sys.platform == 'linux':
        return 'LINUX'

def getApplicationPath(pyFile):
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(pyFile)