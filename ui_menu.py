import bpy
from .get_attributes import vertex_groups_from_obj, attr_name_from_obj_modifiers, attr_name_from_eval_obj


def draw_names_button(layout, names: list[str], icon: str = "NONE"):
    for name in names:
        op = layout.operator('node.nw_add_attr_node', text=name, icon=icon)
        op.attr_name = name


class ASA_OT_add_hide_attr_menu(bpy.types.Menu):
    bl_idname = "ASA_OT_add_hide_attr_menu"
    bl_label = "Hide"

    def draw(self, context):
        layout = self.layout

        attr_names = attr_name_from_eval_obj(context.object)
        attr_names = [name for name in attr_names if name.startswith(".")]

        draw_names_button(layout, attr_names)


class ASA_MT_add_attr_menu(bpy.types.Menu):
    bl_idname = "ASA_MT_add_attr_menu"
    bl_label = "Attributes"

    def draw(self, context):
        if not context.object: return
        layout = self.layout
        vg_names = vertex_groups_from_obj(context.object)
        draw_names_button(layout, vg_names, icon="GROUP_VERTEX")

        if vg_names:
            layout.separator()

        mod_attr_names = attr_name_from_obj_modifiers(context.object)
        draw_names_button(layout, mod_attr_names, icon="MODIFIER")
        if mod_attr_names:
            layout.separator()

        attr_names = attr_name_from_eval_obj(context.object)
        attr_names = [name for name in attr_names if not name.startswith(".") and name not in mod_attr_names]
        draw_names_button(layout, attr_names)
        layout.menu(ASA_OT_add_hide_attr_menu.bl_idname, text="Hide")


def register():
    bpy.utils.register_class(ASA_OT_add_hide_attr_menu)
    bpy.utils.register_class(ASA_MT_add_attr_menu)


def unregister():
    bpy.utils.unregister_class(ASA_MT_add_attr_menu)
    bpy.utils.unregister_class(ASA_OT_add_hide_attr_menu)
