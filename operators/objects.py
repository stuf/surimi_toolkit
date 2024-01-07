import logging

import bpy
import bpy.types as T
from bpy import data as D

from ..lookup import WEIGHT_LOOKUP

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

        armature.pose_position = 'REST' if armature.pose_position == 'POSE' else 'POSE'

        return {'FINISHED'}


class OBJECT_OT_surimi_rename_weights(T.Operator):
    bl_idname = 'surimi.rename_weights'
    bl_label = 'Rename Weights'
    bl_description = 'Rename weights to matching Rigify ones if they exist'
    bl_options = {'REGISTER', 'UNDO'}

    def rename_weights(self, obj: T.Object) -> (bool, int):
        logger.info('Rename weights for object %s', obj.name)
        if obj.type != 'MESH':
            return False, 0

        groups: list[str] = obj.vertex_groups

        try:
            renamed = 0

            for g in groups:
                if g.name in WEIGHT_LOOKUP:
                    g.name = WEIGHT_LOOKUP[g.name]
                    renamed += 1

            print(f'Renamed groups; {obj.name=} {renamed=}')
            return True, renamed

        except Exception:
            return False, 0

    def execute(self, ctx: T.Context):
        print(f'RENAME WEIGHTS on {len(ctx.selected_objects)}')
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
            self.report(
                {'INFO'},
                'Did not rename any weights for the selected object(s).'
            )

            return {'CANCELLED'}

        self.report(
            {'INFO'},
            f'Renamed: {done_objs=} {done_groups=}'
        )

        return {'FINISHED'}
