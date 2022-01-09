# Never changing stuff used all over

import os
from bepipe.core.qt import style

# TODO maybe get this from a env var?
FILE_DIRECTORY = os.path.join(os.path.dirname(__file__)).split("api")[0]

ASSET_TYPES = ["char", "env", "material", "prop", "trim", "utility", "vfx"]

ASSET_TOOLTIPS = {
    "char": "Players, NPCs, critters, etc.",
    "env": "Buildings, trees, terrain, etc.",
    "material": "Tileable and/or other versatile material (pack your maps!)",
    "prop": "Weapons, items, non-character specific things",
    "trim": "Trim textures",
    "utility": "Design and helper assets, uberkit, locators, markers, debug design assets, etc.",
    "vfx": "Boom! Pow! Zappies!"
}

ASSET_ICONS = {
    "char": os.path.join(FILE_DIRECTORY, "resources/icons/char.png"),
    "env": os.path.join(FILE_DIRECTORY, "resources/icons/environment.png"),
    "material": os.path.join(FILE_DIRECTORY, "resources/icons/icon_mat.png"),
    "prop": os.path.join(FILE_DIRECTORY, "resources/icons/prop.png"),
    "trim": os.path.join(FILE_DIRECTORY, "resources/icons/icon_trim.png"),
    "utility": os.path.join(FILE_DIRECTORY, "resources/icons/icon_utility.png"),
    "vfx": os.path.join(FILE_DIRECTORY, "resources/icons/vfx.png")
}

ELEMENTS = [
    "animation",    # Blender
    "bake",         # Marmo
    "cache",        # Exports from Blender
    "lighting",     # Marmo, Blender, or UE4
    "maps",         # Designer, Photoshop, Painter
    "mesh",         # Blender
    "reference",    # Open to images, vids, pure ref, docs
    "render",       # Render outputs
    "rig",          # Blender
    "sculpt"        # ZBrush
    ]

ELEMENT_ICONS = {
    "animation": os.path.join(FILE_DIRECTORY, "resources/icons/icon_anim.png"),
    "cache": os.path.join(FILE_DIRECTORY, "resources/icons/icon_cache.png"),
    "lighting": os.path.join(FILE_DIRECTORY, "resources/icons/icon_light.png"),
    "maps": os.path.join(FILE_DIRECTORY, "resources/icons/icon_maps.png"),
    "mesh": os.path.join(FILE_DIRECTORY, "resources/icons/icon_mesh.png"),
    "reference": os.path.join(FILE_DIRECTORY, "resources/icons/icon_ref.png"),
    "render": os.path.join(FILE_DIRECTORY, "resources/icons/icon_render.png"),
    "rig": os.path.join(FILE_DIRECTORY, "resources/icons/icon_rig.png"),
    "sculpt": os.path.join(FILE_DIRECTORY, "resources/icons/icon_sculpt.png")
}

MENU_ICONS = {
    "disk": os.path.join(FILE_DIRECTORY, "resources/icons/disk.png"),
    "modify": os.path.join(FILE_DIRECTORY, "resources/icons/modify.png"),
    "rename": os.path.join(FILE_DIRECTORY, "resources/icons/rename.png"),
    "delete": os.path.join(FILE_DIRECTORY, "resources/icons/delete.png")
}

MESSAGE_SEVERITY = {
    "INFO": style.WHITE_TEXT,
    "WARN": style.ORANGE_TEXT,
    "ERROR": style.RED_TEXT
}

P4_ICONS = {
    "LOCAL_UP_TO_DATE": os.path.join(FILE_DIRECTORY, "resources/icons/p4_local_up_to_date.png"),
    "LOCAL_OUT_OUT_DATE": os.path.join(FILE_DIRECTORY, "resources/icons/p4_local_up_to_date.png"),
    "OFFLINE": os.path.join(FILE_DIRECTORY, "resources/icons/p4_local_up_to_date.png"),
    "CHECKED_OUT": os.path.join(FILE_DIRECTORY, "resources/icons/p4_local_up_to_date.png")
}

P4_TOOLTIPS = {
    "LOCAL_UP_TO_DATE": "Asset is up to date",
    "LOCAL_OUT_OUT_DATE": "Asset is out of date, get latest",
    "OFFLINE": "Asset does not exist locally, get latest",
    "CHECKED_OUT": "Asset is checked out"
}

# Templates to copy to elements folder, copies the entire folder contents
TEMPLATE_PROJECTS = {
    "animation": [os.path.join(FILE_DIRECTORY, "resources/project-files/animation/anim-work.blend")],
    "bake": [os.path.join(FILE_DIRECTORY, "resources/project-files/bake/bake-work.tbscene")],
    "lighting": [os.path.join(FILE_DIRECTORY, "resources/project-files/lighting/lighting-work.blend")],
    "maps": [
        os.path.join(FILE_DIRECTORY, "resources/project-files/maps/psd/maps-work.psd"),
        os.path.join(FILE_DIRECTORY, "resources/project-files/maps/sd/maps-work.sbs"),
        os.path.join(FILE_DIRECTORY, "resources/project-files/maps/sp/maps-work.spp"),
        ],
    "mesh": [os.path.join(FILE_DIRECTORY, "resources/project-files/mesh/mesh-work.blend")],
    "reference": [os.path.join(FILE_DIRECTORY, "resources/project-files/reference/ref-work.pur")],
    "rig": [os.path.join(FILE_DIRECTORY, "resources/project-files/rig/rig-work.blend")],
    "sculpt": [os.path.join(FILE_DIRECTORY, "resources/project-files/sculpt/sculpt-work.ztl")]
}

ASSET_TREE = os.path.join(FILE_DIRECTORY, "resources/asset_tree.json")

RESOURCES_FOLDER = os.path.join(FILE_DIRECTORY, "resources")

CAT_THUMBNAIL = os.path.join(FILE_DIRECTORY, "resources/thumbnails/thumbnail_CAT.png")

WINDOW_ICON = os.path.join(FILE_DIRECTORY, "resources/icons/icon_CAT.png")

NO_PROJECT = "Open a project or create a new one."