
# Main ops for Blender menu (blender.menus.panels.py)

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

from . import _version
from . import _save
from . import _utils

_FILE_EXT = ".blend"

class SaveWorkingFile(bpy.types.Operator, ExportHelper):

    bl_idname = "wm.bep_save_working_file"
    bl_label = "Save Working File"
    bl_description = "Save as the current asset working file, 'asset_mesh.blend'"
    
    filter_glob: StringProperty(
        default='*.blend;',
        options={'HIDDEN'} )

    def execute(self, context):
        asset = bep_utils.getAssetName()
        if _save.saveWorkingfile(asset, self.filepath):
            print("Saved " + asset)
        else:
            self.report({'INFO'}, "Couldn't locate the asset name. Are you in the right location?")
        return {'FINISHED'}

class SaveNewVersion(bpy.types.Operator):

    bl_idname = "wm.bep_save_new_version"
    bl_label = "Save New Version"
    bl_description = "Versioning system for Be Pipeline"

    def execute(self, context):
        newVersion = _version.version()
        if newVersion.isValidAsset():
            newVersion.createNewVersion()
        else:
            self.report({'ERROR'}, "Not a valid Be Pipe asset. Publish a new file or save as 'asset_mesh.blend'")
        return {'FINISHED'}

# publish asset
# move latest to official

# TODO won't be an operator but will call a new menu
class CreateNewAsset(bpy.types.Operator):

    bl_idname = "wm.bep_create_new_asset"
    bl_label = "CAT"
    bl_description = "Options for creating new model and rigging assets"

    def execute(self, context):

        print("Show create asset menu")
        return {'FINISHED'}

# export selection as fbx
# export scene as fbx
# export for sculpt