import bpy
from .get_attributes import vertex_groups_from_obj, attr_name_from_obj_modifiers, attr_name_from_eval_obj


def draw_names_button(layout, names: list[str], icon: str = "NONE"):
    for name in names:
        op = layout.operator('node.nw_add_attr_node', text=name, icon=icon)
        op.attr_name = name


class ASA_MT_add_hide_attr_menu(bpy.types.Menu):
    bl_idname = "ASA_MT_add_hide_attr_menu"
    bl_label = "Hide"

    def draw(self, context):
        layout = self.layout

        attr_names = attr_name_from_eval_obj(context.object)
        attr_names = [name for name in attr_names if name.startswith(".")]

        draw_names_button(layout, attr_names)


class ASA_MT_add_attr_menu(bpy.types.Menu):
    bl_idname = "ASA_MT_add_attr_menu"
    bl_label = "Attributes"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        vg_names = vertex_groups_from_obj(context.object)
        mod_attr_names = attr_name_from_obj_modifiers(context.object)
        attr_names = attr_name_from_eval_obj(context.object)
        normal_attr_names = [name for name in attr_names if not name.startswith(".") and name not in mod_attr_names]
        hidden_attr_names = [name for name in attr_names if name.startswith(".")]

        if len(vg_names) + len(mod_attr_names) + len(attr_names) == 0:
            layout.label(text="No attributes on objects with this material")
            return

        draw_names_button(layout, vg_names, icon="GROUP_VERTEX")
        draw_names_button(layout, mod_attr_names, icon="MODIFIER")
        draw_names_button(layout, normal_attr_names)

        layout.separator()
        if hidden_attr_names:
            layout.menu(ASA_MT_add_hide_attr_menu.bl_idname, text="Hide")


def register():
    bpy.utils.register_class(ASA_MT_add_hide_attr_menu)
    bpy.utils.register_class(ASA_MT_add_attr_menu)


def unregister():
    bpy.utils.unregister_class(ASA_MT_add_attr_menu)
    bpy.utils.unregister_class(ASA_MT_add_hide_attr_menu)
