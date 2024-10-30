import logging
import bpy
import bpy.types as T
import bpy.props as P
from pprint import pprint

from ..util.lookup import WEIGHT_LOOKUP
from ..declarations import Operators as Ot

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


class OBJECT_OT_surimi_set_subdiv_display(T.Operator):
    bl_idname = Ot.SET_SUBDIV_DISPLAY
    bl_label = 'Optimal display'
    bl_description = 'Enables or disables the `Optimal Display` property of the selected ' \
        'objects\' subdivision surface modifiers'
    bl_options = {'REGISTER', 'UNDO'}

    set_value: P.BoolProperty(
        name="Enable"
    )

    def execute(self, ctx: T.Context):
        objs: list[T.Object] = [
            o for o in ctx.selected_objects if o.type == 'MESH']

        if not len(objs):
            return {'CANCELLED'}

        for obj in objs:
            subdivs: list[T.SubsurfModifier] = [
                m for m in obj.modifiers if m.type == 'SUBSURF']
            for m in subdivs:
                m.show_only_control_edges = self.set_value

        return {'FINISHED'}


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
    FIXME: This doesn't work on 4.1 or later due to `use_auto_smooth` not being a thing
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

        # data: T.Mesh = obj.data
        # data.use_auto_smooth = False

        bevel: T.BevelModifier = obj.modifiers.new(name='Bevel', type='BEVEL')
        bevel.show_in_editmode = False
        bevel.limit_method = 'WEIGHT'
        bevel.segments = 2
        bevel.width = 0.01
        bevel.show_expanded = False

        subdiv: T.SubsurfModifier = obj.modifiers.new(
            name='Subdiv', type='SUBSURF')
        subdiv.boundary_smooth = 'PRESERVE_CORNERS'
        subdiv.show_in_editmode = False
        subdiv.show_expanded = False

        return {'FINISHED'}


#
class OBJECT_OT_surimi_toggle_bone_collection(T.Operator):
    bl_idname = Ot.TOGGLE_BONE_COLLECTION
    bl_label = 'Toggle Bone Collection'
    bl_description = 'Toggles the visibility of a bone collection'
    bl_options = {'REGISTER', 'UNDO'}

    bone_collection: P.StringProperty(name='Bone Collection')

    def execute(self, ctx: T.Context):
        if not ctx.active_object.type == 'ARMATURE':
            self.report({'ERROR'},
                        'Operator can only be called on armatures',
                        )
            return {'CANCELLED'}

        if not self.bone_collection:
            self.report({'ERROR'},
                        'Operator requires a bone collection name',
                        )
            return {'CANCELLED'}

        obj = ctx.active_object
        d: T.Armature = obj.data
        colls = d.collections

        coll = colls[self.bone_collection]
        coll.is_visible = not coll.is_visible

        return {'FINISHED'}


class OBJECT_OT_surimi_remove_empty_vertex_groups(T.Operator):
    bl_idname = Ot.EXPERIMENTAL_REMOVE_EMPTY_VERTEX_GROUPS
    bl_label = 'Remove empty vertex groups (EXPERIMENTAL)'
    bl_description = 'Removes empty vertex groups from the selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def collect_weights(self, obj: T.Object):
        max_w = {}

        for k, g in obj.vertex_groups.items():
            max_w[g.index] = 0

        mesh: T.Mesh = obj.data
        for v in mesh.vertices:
            vert: T.MeshVertex = v
            for g in vert.groups:
                vg: T.VertexGroupElement = g
                vgn = vg.group
                w = obj.vertex_groups[vgn].weight(vert.index)

                if max_w.get(vgn) is None or w > max_w[vgn]:
                    max_w[vgn] = w

        return max_w

    def execute(self, ctx: T.Context):
        if bpy.context.mode != 'OBJECT':
            self.report(
                {'ERROR'}, 'This operator can only be used in object mode')
            return {'CANCELLED'}

        tot_objs = 0
        tot_groups = 0
        removed_groups = 0

        for o in ctx.selected_objects:
            tot_objs += 1

            obj: T.Object = o
            if obj.type != 'MESH':
                logger.warning('`%s` is not a mesh, skipping', obj.name)
                continue

            logger.info('Processing `%s`', obj.name)

            ws = self.collect_weights(obj)

            group_indices = []
            group_indices.extend(ws.keys())
            group_indices.sort(key=lambda gn: -gn)
            tot_groups += len(group_indices)

            for i in group_indices:
                if ws[i] <= 0:
                    vg: T.VertexGroup = obj.vertex_groups[i]
                    logger.info(
                        ' - remove empty vertex group %s -> %s', obj.name, vg.name)
                    obj.vertex_groups.remove(vg)
                    removed_groups += 1

            logger.info('- Processed %s', obj.name)

        logger.info('Cleaned up %s selected object(s) - %s groups, %s removed',
                    tot_objs, tot_groups, removed_groups)

        return {'FINISHED'}


#

classes = [
    OBJECT_OT_surimi_rename_weights,
    OBJECT_OT_surimi_toggle_pose_position,
    OBJECT_OT_surimi_create_character_props,
    OBJECT_OT_surimi_add_usual_modifiers,
    # OBJECT_OT_surimi_toggle_bone_collection,
    OBJECT_OT_surimi_set_subdiv_display,
    OBJECT_OT_surimi_remove_empty_vertex_groups,
]


def register():
    logger.info('register operators')

    for cls in classes:
        logger.info(' - operator: %s', cls.__name__)
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
