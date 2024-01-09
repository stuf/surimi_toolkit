import logging
import bpy
import bpy.types as T

from .util.lookup import WEIGHT_LOOKUP

logger = logging.getLogger(__name__)


class OBJECT_OT_surimi_toggle_pose_position(T.Operator):
    bl_idname = 'surimi.toggle_pose_position'
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
    bl_idname = 'surimi.rename_weights'
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


classes = [
    OBJECT_OT_surimi_rename_weights,
    OBJECT_OT_surimi_toggle_pose_position,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
