import os

FILE_DIRECTORY = os.path.join(os.path.dirname(__file__)).split('utility')[0]

ASSET_TYPES = ['char', 'env', 'prop', 'vfx']

ASSET_ICONS = {
    'char': os.path.join(FILE_DIRECTORY, 'resources/icons/char.png'),
    'env': os.path.join(FILE_DIRECTORY, 'resources/icons/environment.png'),
    'prop': os.path.join(FILE_DIRECTORY, 'resources/icons/prop.png'),
    'vfx': os.path.join(FILE_DIRECTORY, 'resources/icons/vfx.png')
}

ELEMENTS = [
    "animation",
    "cache",
    "lighting",
    "maps",
    "mesh",
    "reference",
    "render",
    "rig",
    "sculpt"
    ]

ELEMENT_ICONS = {
    'anim': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_anim.png'),
    'cache': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_cache.png'),
    'lighting': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_light.png'),
    'maps': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_maps.png'),
    'mesh': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_mesh.png'),
    'reference': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_ref.png'),
    'render': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_render.png'),
    'rig': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_rig.png'),
    'sculpt': os.path.join(FILE_DIRECTORY, 'resources/icons/icon_sculpt.png')
}

MENU_ICONS = {
    'disk': os.path.join(FILE_DIRECTORY, "resources/icons/disk.png"),
    'modify': os.path.join(FILE_DIRECTORY, "resources/icons/modify.png"),
    'rename': os.path.join(FILE_DIRECTORY, "resources/icons/rename.png"),
    'delete': os.path.join(FILE_DIRECTORY, "resources/icons/delete.png")
}

P4_ICONS = {
    'LOCAL_UP_TO_DATE': os.path.join(FILE_DIRECTORY, 'resources/icons/p4_local_up_to_date.png'),
    'LOCAL_OUT_OUT_DATE': os.path.join(FILE_DIRECTORY, 'resources/icons/p4_local_up_to_date.png'),
    'OFFLINE': os.path.join(FILE_DIRECTORY, 'resources/icons/p4_local_up_to_date.png'),
    'CHECKED_OUT': os.path.join(FILE_DIRECTORY, 'resources/icons/p4_local_up_to_date.png')
}

P4_TOOLTIPS = {
    'LOCAL_UP_TO_DATE': "Asset is up to date",
    'LOCAL_OUT_OUT_DATE': "Asset is out of date, get latest",
    'OFFLINE': "Asset does not exist locally, get latest",
    'CHECKED_OUT': "Asset is checked out"
}

CAT_THUMBNAIL = os.path.join(FILE_DIRECTORY, 'resources/thumbnails/thumbnail_CAT.png')

WINDOW_ICON = os.path.join(FILE_DIRECTORY, 'resources/icons/icon_CAT.png')

NO_PROJECT = "Open a project or create a new one."
