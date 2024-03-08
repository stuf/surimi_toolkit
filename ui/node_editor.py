import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ..declarations import Panels as Pt
from ..operators.node_editor import (
    NA_OT_srm_import_material,
    NA_OT_srm_choose_import_material_dir,
    NA_OT_srm_rename_material_textures,
)

import logging

logger = logging.getLogger(__name__)

#


class NA_PT_srm_node_base(T.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Surimi'


class NA_PT_srm_node_mat_importer(NA_PT_srm_node_base):
    """Proof-of-concept operator for importing a bunch of materials
    """
    bl_idname = Pt.NA_MAT_IMPORTER
    bl_label = 'Material Importer'

    @classmethod
    def poll(cls, ctx: T.Context):
        try:
            return ctx.active_object.active_material
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object
        mat = obj.active_material
        # mat_import = mat.surimi_mat_importer

        # col = layout.column()

        # row = col.column()

        # row.label(text='Current material')
        # row.label(text=ctx.active_object.active_material.name)

        # row = col.row(align=True)
        # row.prop(mat_import, 'search_path', text='Directory')
        # row.operator(NA_OT_srm_choose_import_material_dir.bl_idname,
        #              icon='FILE_FOLDER', text='')

        # row = col.column()
        # row.prop(mat_import, 'recursive')
        # row.prop(mat_import, 'use_material_name')

        # col.separator()
        # row = col.column()
        # row.operator(NA_OT_srm_import_material.bl_idname)


class NA_PT_srm_helpers(NA_PT_srm_node_base):
    bl_idname = Pt.NA_HELPERS
    bl_label = 'Rename Images'

    def draw(self, ctx: T.Context):
        layout = self.layout

        row = layout.column()
        row.operator(NA_OT_srm_rename_material_textures.bl_idname)


classes = [
    NA_PT_srm_node_mat_importer,
    NA_PT_srm_helpers,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
