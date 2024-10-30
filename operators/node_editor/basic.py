import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D

from ...declarations import Operators as Ot

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


class NA_OT_surimi_experimental_normalize_image_nodes(T.Operator):
    bl_idname = Ot.EXPERIMENTAL_NORMALIZE_IMAGE_NODES
    bl_label = 'Normalize Image Nodes (EXPERIMENTAL)'
    bl_description = 'Rename images matching the material name and properly set their colorspace/gamma'
    bl_options = {'REGISTER', 'UNDO'}

    gamma = [
        ({'Alb'}, 2.2),
    ]

    def execute(self, ctx: T.Context):
        node_rna_types = {'ShaderNodeOctImageTex', 'OctaneRGBImage'}

        obj = C.active_object
        mat = obj.active_material
        mat_name = mat.name
        nodes = mat.node_tree.nodes

        done_count = 0

        selected: list[T.Node] = \
            [n
             for n in nodes
             if n.select
             and n.bl_rna.identifier in node_rna_types]

        if not len(selected):
            self.report({'ERROR'}, 'No nodes selected to handle')
            return {'CANCELLED'}

        for n in selected:
            img: T.Image = n.image
            img_name = img.name

            if not img_name.startswith(mat_name):
                print(
                    f'Image name `{img_name=}` does not start with `{mat_name=}`, skipping.')
                continue

            tail = img_name.removeprefix(f'{mat_name}_')
            tail = re.match(r'(\w+)', tail)

            if not tail:
                print('Something silly going on')
                print(f' - {img_name=}')
                print(f' - {mat_name=}')
                print(f' - {tail=}')
                continue

            tail = tail.group(1)
            n.image.name = '-'.join([mat_name, tail])
            n.label = tail
            n.name = f'NODE-{n.image.name}'

            # This only works if you have Octane
            # Essentially should change the colorspace if in Cycles/Eevee
            for types, gamma_value in self.gamma:
                socket: T.NodeSocket

                try:
                    socket = n.inputs['Legacy gamma']
                except KeyError:
                    socket = n.inputs['Gamma']

                if tail in types or tail.capitalize() in types:
                    socket.default_value = gamma_value
                else:
                    socket.default_value = 1.0

                done_count += 1

        self.report({'INFO'}, f'Normalized {done_count} node(s).')

        return {'FINISHED'}


classes = [
    NA_OT_srm_add_imagetex,
    NA_OT_srm_add_node,
    NA_OT_surimi_experimental_normalize_image_nodes,
]


def register():
    logger.info('register operators')

    for cls in classes:
        logger.info(' - operator: %s', cls.__name__)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
