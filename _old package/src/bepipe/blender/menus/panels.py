# BeP Blender UI

import bpy
from bpy.types import Menu

from . import ops


class BeP_MT_tools(Menu):
    """ Menu UI for saving, versioning, publishing
    """

    bl_idname = "BeP_MT_tools"
    bl_label = "BeP"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.bep_save_working_file")
        layout.separator()
        layout.operator("wm.bep_save_new_version")
        layout.separator()
        layout.operator("wm.bep_create_new_asset")


def bep_menu(self, ctx):
	self.layout.menu("BeP_MT_tools")