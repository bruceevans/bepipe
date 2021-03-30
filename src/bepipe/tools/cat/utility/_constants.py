import os

FILE_DIRECTORY = os.path.join(os.path.dirname(__file__)).split('utility')[0]
WINDOW_ICON = os.path.join(FILE_DIRECTORY, "resources/icons/icon_CAT.png")
MENU_ICONS = {
    'disk': os.path.join(FILE_DIRECTORY, "resources/icons/disk.png"),
    'modify': os.path.join(FILE_DIRECTORY, "resources/icons/modify.png"),
    'rename': os.path.join(FILE_DIRECTORY, "resources/icons/rename.png"),
    'delete': os.path.join(FILE_DIRECTORY, "resources/icons/delete.png")
}

ELEMENTS = ["Animation", "Lighting", "Maps", "Mesh", "Output", "Reference", "Rig", "Sculpt"]

ASSET_ICONS = {
    'char': os.path.join(FILE_DIRECTORY, 'resources/icons/char.png'),
    'environment': os.path.join(FILE_DIRECTORY, 'resources/icons/environment.png'),
    'prop': os.path.join(FILE_DIRECTORY, 'resources/icons/prop.png'),
    'vfx': os.path.join(FILE_DIRECTORY, 'resources/icons/vfx.png')
}

ASSET_TYPES = ['char', 'environment', 'prop', 'vfx']

NO_PROJECT = "Open a project or create a new one."
