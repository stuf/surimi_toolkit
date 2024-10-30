import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ...declarations import Operators as Ot


class NA_OT_srm_import_map_materials(T.Operator):
    bl_idname = Ot.EXPERIMENTAL_IMPORT_MAP_MATERIALS
    bl_label = 'Import Map Materials'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):

        return {'CANCELLED'}


#

CLASSES = [
    NA_OT_srm_import_map_materials
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
