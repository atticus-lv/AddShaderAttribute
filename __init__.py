bl_info = {
    "name": "Add Shader Attribute",
    "author": "Atticus",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "Shader NodeTree > Side Panel",
    "description": "Add attribute directly in shader nodetree",
    "doc_url": "https://github.com/atticus-lv/AddShaderAttribute",
    "category": "Render",
}

import bpy
from . import ui_menu


def add_menu(self, context):
    if context.space_data.tree_type == 'ShaderNodeTree' and context.space_data.edit_tree:
        self.layout.separator()
        self.layout.menu(ui_menu.ASA_MT_add_attr_menu.bl_idname, icon='MESH_DATA')


def register():
    ui_menu.register()
    bpy.types.NODE_MT_add.append(add_menu)


def unregister():
    ui_menu.unregister()
    bpy.types.NODE_MT_add.remove(add_menu)
