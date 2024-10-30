import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ..declarations import Panels as Pt
from ..operators.node_editor.basic import (
    NA_OT_srm_add_imagetex,
    NA_OT_srm_add_node,
    NA_OT_surimi_experimental_normalize_image_nodes,
)
from ..util.helpers import (
    render_engine_is_cycles,
    render_engine_is_octane,
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


buttons = {
    'Textures': [
        ('ImageTex', 'ShaderNodeOctImageTex', None),
        ('RGB', 'OctaneRGBImage', None),
        ('Alpha', 'OctaneAlphaImage', None),
        ('Gray', 'OctaneGreyscaleImage', None),
    ],
    'Projection': [
        ('Spherical', 'OctaneSpherical', 100.0),
        ('Mesh UV', 'OctaneMeshUVProjection', 100.0),
    ],
    'Transform': [
        ('2D', 'Octane2DTransformation', None),
        ('3D', 'Octane3DTransformation', None),
        ('Scale', 'OctaneScale', None),
        ('Rotation', 'OctaneRotation', None),

    ],
    'Operations': [
        ('Mult', 'OctaneMultiplyTexture', 100.0),
        ('Mix', 'OctaneMixTexture', 100.0),
        ('Inv', 'OctaneInvertTexture', 100.0),
    ],
    'Adjust': [
        ('Color Correction', 'OctaneColorCorrection', None),
    ],
    'Emission': [
        ('Black Body', 'OctaneBlackBodyEmission', None),
        ('Texture', 'OctaneTextureEmission', None),
    ]
}


class NA_PT_srm_helpers(NA_PT_srm_node_base):
    bl_idname = Pt.NA_HELPERS
    bl_label = 'Helpers'

    def draw(self, ctx: T.Context):
        pass


class NA_PT_srm_quick_nodes(NA_PT_srm_node_base):
    bl_idname = Pt.NA_QUICK_NODES
    bl_label = 'Helpers (Octane)'
    bl_parent_id = Pt.NA_HELPERS

    @classmethod
    def poll(cls, ctx: T.Context):
        return render_engine_is_octane(ctx)

    def draw(self, ctx: T.Context):
        layout = self.layout

        col = layout.column()

        for label, rows in buttons.items():
            col = layout.column()
            col.label(text=label)

            r = col.row()
            for row_label, node_type, node_width in rows:
                ot = r.operator(NA_OT_srm_add_node.bl_idname, text=row_label)
                ot.node_name = node_type

                if node_width:
                    ot.node_width = node_width


class NA_PT_srm_node_other(NA_PT_srm_node_base):
    bl_idname = Pt.NA_OTHER
    bl_label = 'Other'
    bl_parent_id = Pt.NA_HELPERS

    def draw(self, ctx: T.Context):
        layout = self.layout

        col = layout.column()
        col.operator(NA_OT_surimi_experimental_normalize_image_nodes.bl_idname,
                     text='Normalize images')


#

classes = [
    NA_PT_srm_node_mat_importer,
    NA_PT_srm_helpers,
    NA_PT_srm_quick_nodes,
    NA_PT_srm_node_other,
]


def register():
    logger.info('registering UI')
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
