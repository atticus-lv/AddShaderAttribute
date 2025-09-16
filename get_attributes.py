import bpy


def output_sockets_from_geo_nodetree(nt: bpy.types.GeometryNodeTree) -> list[bpy.types.NodeTreeInterfaceSocket]:
    return [item for item in nt.interface.items_tree if item.item_type == 'SOCKET' and item.in_out == 'OUTPUT']


def attr_id_value_from_mod(mod: bpy.types.NodesModifier) -> dict[str, str]:
    if not mod.node_group: return {}
    node_group = mod.node_group

    output_sockets = output_sockets_from_geo_nodetree(node_group)
    return {
        f"{item.identifier}_attribute_name": mod.get(f"{item.identifier}_attribute_name")
        for item in output_sockets if mod.get(f"{item.identifier}_attribute_name", "") != ""
    }


def attr_name_from_eval_obj(obj: bpy.types.Object) -> list[str]:
    eval_obj = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    if not hasattr(eval_obj.data, 'attributes'): return []
    return [attr.name for attr in eval_obj.data.attributes]


def attr_name_from_obj_modifiers(obj: bpy.types.Object) -> list[str]:
    res = []
    if not hasattr(obj, 'modifiers'): return res
    for mod in obj.modifiers:
        if mod.type != 'NODES': continue
        res += attr_id_value_from_mod(mod).values()
    return res


def vertex_groups_from_obj(obj: bpy.types.Object) -> list[str]:
    if not hasattr(obj, 'vertex_groups'): return []
    return [vg.name for vg in obj.vertex_groups]


def attr_name_from_obj_geo_instance(obj: bpy.types.Object) -> list[str]:
    res = []
    geo_types = ["mesh", "curves", "instances_pointcloud", "grease_pencil"]

    depsgraph = bpy.context.view_layer.depsgraph
    eval_obj = depsgraph.id_eval_get(obj)
    geometry = eval_obj.evaluated_geometry()

    # TODO: recursively get attributes from all instance level
    if len(geometry.instance_references()) == 0: return res

    for geo in geometry.instance_references():
        for geo_type in geo_types:
            if not hasattr(geo, geo_type): continue
            geo_data = getattr(geo, geo_type)
            if hasattr(geo_data, 'attributes'):
                res += [attr.name for attr in geo_data.attributes]

    return res
