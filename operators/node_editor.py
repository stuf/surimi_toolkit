import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ..declarations import Operators as Ot

import logging
import re

logger = logging.getLogger(__name__)

#


class NA_OT_srm_add_imagetex(T.Operator):
    bl_idname = Ot.ADD_IMAGETEX
    bl_label = 'Add ImageTex Node'
    bl_description = 'Add an OctImageTex node on the currently active material'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mat = obj.active_material
        nodes = mat.node_tree.nodes

        nodes.new('ShaderNodeOctImageTex')

        return {'FINISHED'}


class NA_OT_srm_add_node(T.Operator):
    bl_idname = Ot.ADD_NODE
    bl_label = 'Add Node'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    node_name: P.StringProperty()
    node_width: P.FloatProperty()

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mat = obj.active_material
        nodes = mat.node_tree.nodes

        node = nodes.new(self.node_name)
        if self.node_width:
            node.width = self.node_width

        return {'FINISHED'}

#


class NA_OT_srm_normalize_selected_filenames(T.Operator):
    """Normalize image names and their colorspace-related settings to match
       naming convention with the current active material.

       WARNING: Octane-only right now."""
    bl_idname = Ot.NORMALIZE_SELECTED_FILENAMES
    bl_label = 'Normalize Selectd Filenames'
    bl_description = 'Normalize the asset names used in the selected nodes'
    bl_options = {'REGISTER', 'UNDO'}

    node_rna_types = {'ShaderNodeOctImageTex', 'OctaneRGBImage'}

    gamma_values = [({'alb'}, 2.2),
                    ]

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mat = obj.active_material
        mat_name = mat.name
        nodes = mat.node_tree.nodes

        selected: list[T.Node] = \
            [n
             for n in nodes
             if n.select
             and n.bl_rna.identifier in self.node_rna_types]

        for n in selected:
            print(f'{n=}')
            img: T.Image = n.image
            img_name = img.name

            if not img_name.startswith(mat_name):
                print(f'Image name `{img_name=}` does not '
                      f'start with `{mat_name=}`, skipping.')
                continue

            tail = img_name.removeprefix(f'{mat_name}_')
            tail = re.match(r'(\w+)', tail)

            if not tail:
                print('Something silly going on')
                print(f' - {img_name=}')
                print(f' - {mat_name=}')
                print(f' - {tail=}')
                continue

            tail = tail.group(1).lower()
            n.image.name = '-'.join([mat_name, tail])
            n.label = tail
            n.name = f'NODE-{n.image.name}'

            for types, gamma_value in self.gamma_values:
                socket = n.inputs['Legacy gamma']
                if tail in types or tail.capitalize() in types:
                    socket.default_value = gamma_value
                else:
                    socket.default_value = 1.0

        return {'FINISHED'}

#


classes = [
    NA_OT_srm_add_imagetex,
    NA_OT_srm_add_node,
    NA_OT_srm_normalize_selected_filenames,
]


def register():
    logger.info('register operators')

    for cls in classes:
        logger.info(' - operator: %s', cls.__name__)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
