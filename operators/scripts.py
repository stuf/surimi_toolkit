from operator import sub
from pathlib import Path
import bpy
import bpy.types as T
import bpy.props as P
from bpy import context as C, data as D
from ..declarations import Operators as Ot

import logging

logger = logging.getLogger(__name__)

#


class SCRIPT_surimi_make_ref_environment(T.Operator):
    bl_idname = Ot.EXPERIMENTAL_SCRIPT_MAKE_REF_ENV
    bl_label = 'Make ref environment'
    bl_options = {'REGISTER'}

    def execute(self, ctx: T.Context):
        WORLD_NAME = 'ENV-reference-sheet'

        HDRI_DIR = r'C:\assets\Light Probes\GSG'
        HDRI_FILE = 'GSG_HC012_A022_GSGProStudiosMetalVol222Env.exr'

        WRL_OUTPUT = 'World Output'
        ENV_INPUT = 'Octane Environment'
        VIS_ENV_INPUT = 'Octane VisibleEnvironment'

        NODE_SPACE = (50, 10)
        space_x, space_y = NODE_SPACE

        if WORLD_NAME in D.worlds:
            D.worlds.remove(D.worlds[WORLD_NAME])

        wrl = D.worlds.new(WORLD_NAME)

        wrl.use_nodes = True
        wrl.use_fake_user = True

        nodes = wrl.node_tree.nodes
        links = wrl.node_tree.links

        if 'Background' in nodes:
            nodes.remove(nodes['Background'])

        ###

        output = nodes[WRL_OUTPUT]
        env_out = output.inputs[ENV_INPUT]
        vis_env_out = output.inputs[VIS_ENV_INPUT]

        wrl_env = nodes.new('OctaneTextureEnvironment')
        vis_env = nodes.new('OctaneTextureEnvironment')

        origin_x, origin_y = output.location

        # Configure environments

        # wrl_env.hide = True
        wrl_env.label = 'Environment'
        wrl_env.location = (origin_x - wrl_env.width - space_x,
                            origin_y)
        wrl_env.inputs['Power'].default_value = 3.0

        wrl_env_x, wrl_env_y = wrl_env.location

        # vis_env.hide = True
        vis_env.label = 'Visible Environment'
        vis_env.location = (origin_x - vis_env.width - space_x,
                            origin_y - wrl_env_y - wrl_env.height - space_y)

        # World Env
        wrl_env_img = nodes.new('OctaneRGBImage')
        wrl_env_img.location = \
            tuple(map(sub,
                      wrl_env.location,
                      (wrl_env_img.width + space_x, 0)))

        wrl_env_img.inputs['Legacy gamma'].default_value = 1.0

        # Load img

        hdri_path = Path(HDRI_DIR, HDRI_FILE)
        hdri_name = f'ENV-IMG-{hdri_path.stem}'

        if hdri_name in D.images:
            D.images.remove(D.images[hdri_name])

        # Yes, that's right, don't ask
        img1 = set(D.images.keys())
        bpy.ops.image.open(filepath=str(hdri_path))
        img2 = set(D.images.keys())

        new_img = (img1 ^ img2).pop()

        env_img = D.images[new_img]
        env_img.name = hdri_name

        wrl_env_img.image = env_img

        # Set up projection
        proj = nodes.new('OctaneSpherical')
        proj.location = \
            tuple(map(sub,
                      wrl_env_img.location,
                      (space_x + proj.width, 0)))

        # Set up transform
        tfn = nodes.new('OctaneRotation')
        tfn.location = \
            tuple(map(sub,
                      proj.location,
                      (space_x + tfn.width, 0)))

        tfn.inputs['Angles'].default_value = (0.0, 130.0, 0.0)

        # -------
        # Vis Env
        vis_env.inputs['Texture'].default_value = (0.005, 0.005, 0.005)
        vis_env.inputs['Backplate'].default_value = True

        # Link things together now

        node_links = [
            (wrl_env.outputs['Environment out'], env_out),
            (vis_env.outputs['Environment out'], vis_env_out),
            (wrl_env_img.outputs['Texture out'], wrl_env.inputs['Texture']),
            (proj.outputs['Projection out'], wrl_env_img.inputs['Projection']),
            (tfn.outputs['Transform out'],
             proj.inputs['Sphere transformation']),
        ]

        for source_socket, dest_socket in node_links:
            links.new(source_socket, dest_socket)

        self.report({'INFO'}, f'Created ref environment {wrl.name}')

        return {'FINISHED'}

#


classes = [
    # SCRIPT_surimi_make_ref_environment,
]


def register():
    logger.info('register operators')

    for cls in classes:
        logger.info(' - operator: %s', cls.__name__)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
