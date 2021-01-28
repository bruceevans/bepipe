
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
    print("NEED MAC SOLUTION")
    print(_PLATFORM)
