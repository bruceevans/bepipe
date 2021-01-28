
import os
import sys
import shutil

from PIL import Image

import bepipe.core.utility.helpers as utils

_PLATFORM = utils.getPlatform()

if _PLATFORM == 'WINDOWS':
    import win32ui
    import win32gui
    import win32api
    import win32con

    def getIcon(appPath, iconName):

        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

        large, small = win32gui.ExtractIconEx(appPath, 0)
        win32gui.DestroyIcon(large[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), small[0])

        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr,
            'raw',
            'BGRA', 0, 1
        )
        img.save(iconName)

elif _PLATFORM == 'OSX':

    def findIcns(directory):
        """ Search a folder for any icns files

        Args:
            directory (str): Path of the folder to search
            
        Returns:
            List (str) of icns files (absolut paths)
        """

        return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1]=='.icns']

    def getAppropriateIcon(icons, appName):
        """ Attempt to narrow down the icon possibilities

        Args:
            icons (str list): List of possible icon paths
            appName (str): Name of the application in question
        """

        if not icons:
            print("Couldn't locate and icon, manually search for it in the resources folder")
            return None

        if len(icons) == 1:
            return icons[0]
        else:
            for icon in icons:
                iconName = os.path.splitext(icon)[0]
                if iconName.lower() == appName.lower():
                    return icon
            print("Couldn't locate and icon, manually search for it in the resources folder")
            return None
    
    def createTempIconPng(icon, destination):
        """ Move the icns file to the resources folder and rename to .png
        """
        shutil.copyfile(icon, destination)
        return destination

    def resizeIcon(icon, targetSize = 64):
        """ Use PIL to resize the icon png
        """

        img = Image.open(icon)
        width, height = img.size

        if width == height:
            # get scale factor
            scalar = width / targetSize
            newDimensions = targetSize * scalar
            newSize = (newDimensions, newDimensions)
            img = img.resize(newSize)
            img.save(icon)

    def getIcon(appDirectory, appName, iconDestination):
        """ Run the icon process on mac

        Args:
            appDirectory (str): Path of the app folder to search
            appName (str): Name of the app used in the launcher
            iconDestination (str): Full path of the final icon
            iconSize: Icon size in pixels
        """

        resourcesFolder = "{}/Contents/Resources".format(appDirectory)
        icons = findIcns(resourcesFolder)
        icon = getAppropriateIcon(icons, appName)
        if icon:
            icon = createTempIconPng(icon, iconDestination)
            resizeIcon(icon)
