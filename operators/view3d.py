import logging
import bpy
import bpy.types as T
import bpy.props as P
from typing import Tuple

from ..util.lookup import WEIGHT_LOOKUP
from ..declarations import Operators as Ot
from ..properties import CharacterProps

logger = logging.getLogger(__name__)


class OBJECT_OT_surimi_toggle_pose_position(T.Operator):
    bl_idname = Ot.TOGGLE_POSE_POSITION
    bl_label = 'Toggle Pose Position'
    bl_description = 'Toggles pose position for the selected armature'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object
        mode = ctx.mode
        armature: T.Armature = obj.data
        logger.info('Toggle pose mode for armature "%s"', armature.name)

        armature.pose_position = 'REST' if armature.pose_position == 'POSE' else 'POSE'

        return {'FINISHED'}


class OBJECT_OT_surimi_rename_weights(T.Operator):
    bl_idname = Ot.RENAME_WEIGHTS
    bl_label = 'Rename Weights'
    bl_description = 'Rename weights on selected meshes' \
        'to matching Rigify ones if they exist'
    bl_options = {'REGISTER', 'UNDO'}

    def rename_weights(self, obj: T.Object) -> (bool, int):
        logger.info('Rename weights for object %s', obj.name)

        if obj.type != 'MESH':
            logger.warn('')

            return False, 0

        groups: list[str] = obj.vertex_groups

        try:
            renamed = 0

            for g in groups:
                if g.name in WEIGHT_LOOKUP:
                    g.name = WEIGHT_LOOKUP[g.name]
                    renamed += 1

            logger.info('Renamed groups; object=%s count=%s',
                        obj.name, renamed)

            return True, renamed

        except Exception as e:
            logger.warn('Exception while ')

            return False, 0

    def execute(self, ctx: T.Context):
        logger.info('Rename weights on object %s', ctx)

        done_objs = 0
        done_groups = 0

        meshes: list[T.Object] = [
            obj for obj in ctx.selected_objects if obj.type == 'MESH']

        for mesh in meshes:
            res, gs = self.rename_weights(mesh)
            if res:
                done_objs += 1
                done_groups += gs

        if not done_groups:
            logger.info(
                'Did not renamed any weights for the selected object(s).')

            self.report(
                {'INFO'},
                'Did not rename any weights for the selected object(s).'
            )

            return {'CANCELLED'}

        logger.info(
            'Renamed weights on object(s): objects=%s weights=%s', done_objs, done_groups)

        self.report(
            {'INFO'},
            f'Renamed: {done_objs} object(s), {done_groups} group(s)'
        )

        return {'FINISHED'}

#


class OBJECT_OT_surimi_create_character_props(T.Operator):
    bl_idname = Ot.CREATE_CHARACTER_PROPS
    bl_label = 'Create Character Props'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        return {'CANCELLED'}

#


class OBJECT_OT_surimi_add_usual_modifiers(T.Operator):
    """Adds a bunch of the usual suspects on the selected object if it's a mesh.

    Does the following:
    - Turns off mesh auto smoothing
    - Adds a bevel modifier, with predefined segments (2) and amount (0.01m),
      limit method 'weight'
    - Adds a subdivision modifier

    TODO: Maybe put modifiers in the correct order in the modifier stack
    TODO: Allow configuration of settings from preferences
    """
    bl_idname = Ot.ADD_USUAL_MODIFIERS
    bl_label = 'Add Usual Modifiers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, ctx: T.Context):
        obj = ctx.active_object

        if obj.type != 'MESH':
            self.report(
                {'INFO'}, f'Selected object is not a mesh, doing nothing.')

            return {'CANCELLED'}

        data: T.Mesh = obj.data
        data.use_auto_smooth = False

        bevel: T.BevelModifier = obj.modifiers.new(name='Bevel', type='BEVEL')
        bevel.show_in_editmode = False
        bevel.limit_method = 'WEIGHT'
        bevel.segments = 2
        bevel.width = 0.01
        bevel.show_expanded = False

        subdiv: T.SubsurfModifier = obj.modifiers.new(
            name='Subdiv', type='SUBSURF')
        subdiv.show_in_editmode = False
        subdiv.show_expanded = False

        return {'FINISHED'}


#


classes = [
    OBJECT_OT_surimi_rename_weights,
    OBJECT_OT_surimi_toggle_pose_position,
    OBJECT_OT_surimi_create_character_props,
    OBJECT_OT_surimi_add_usual_modifiers,
]


def register():
    ot_names = [ot.bl_idname for ot in classes]
    logger.info('register operators: %s', ot_names)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
