import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ..declarations import Operators as Ot

import logging

logger = logging.getLogger(__name__)

#


class NA_OT_srm_choose_import_material_dir(T.Operator):
    bl_idname = Ot.CHOOSE_IMPORT_MATERIAL_DIR
    bl_label = 'Choose Import Material Dir'
    bl_description = ''
    bl_options = {'REGISTER'}

    def execute(self, ctx: T.Context):
        return {'FINISHED'}


class NA_OT_srm_import_material(T.Operator):
    bl_idname = Ot.IMPORT_MATERIAL
    bl_label = 'Import Material'
    bl_description = 'Imports and creates a PBR material from the given params'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mat = obj.active_material

        return {'FINISHED'}

    def invoke(self, ctx: T.Context, evt):
        wm = ctx.window_manager
        return wm.invoke_props_dialog(self)

#


class NA_OT_srm_rename_material_textures(T.Operator):
    bl_idname = Ot.RENAME_MATERIAL_TEXTURES
    bl_label = 'Rename Material Textures'
    bl_description = 'Rename image data in a material to match the material\'s name'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mat = obj.active_material
        nodes = mat.node_tree.nodes

        return {'CANCELLED'}

#


classes = [
    NA_OT_srm_import_material,
    NA_OT_srm_choose_import_material_dir,
    NA_OT_srm_rename_material_textures,
]


def register():
    ot_names = [ot.bl_idname for ot in classes]
    logger.info('register operators: %s', ot_names)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
