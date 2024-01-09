import bpy
import bpy.types as T

from ..util.helpers import is_in_pose_position
from ..operators import (OBJECT_OT_surimi_rename_weights,
                         OBJECT_OT_surimi_toggle_pose_position)


class SURIMI_PT_panel_base(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'


class SURIMI_PT_panel_main(SURIMI_PT_panel_base):
    bl_idname = 'SURIMI_PT_panel_main'
    bl_label = 'Surimi Toolkit'

    def draw(self, ctx):
        pass


class SURIMI_PT_panel_render(SURIMI_PT_panel_base):
    bl_label = 'Render'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        row = layout.column()
        row.prop(scene.cycles, 'preview_samples', text='Preview')
        row.prop(scene.cycles, 'samples', text='Render')

        layout.separator()

        row = layout.column()
        row.prop(scene.render, 'preview_pixel_size')


class SURIMI_PT_panel_viewport(SURIMI_PT_panel_base):
    bl_label = 'Viewport'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    def draw(self, ctx: T.Context):
        layout = self.layout
        scene = ctx.scene

        layout.use_property_split = True
        layout.use_property_decorate = True

        row = layout.column()
        row.prop(scene.render, 'use_simplify')

        row = layout.column()
        row.enabled = scene.render.use_simplify
        row.prop(scene.render, 'simplify_subdivision')


class SURIMI_PT_panel_armature(SURIMI_PT_panel_base):
    bl_label = 'Armature'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        try:
            return ctx.active_object.type == 'ARMATURE'
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, ctx: T.Context):
        layout = self.layout

        obj = ctx.active_object
        armature: T.Armature = obj.data

        in_pose_position = is_in_pose_position(armature)

        layout = self.layout

        row = layout.column()
        row.operator(OBJECT_OT_surimi_toggle_pose_position.bl_idname,
                     text='Pose mode', depress=in_pose_position)


class SURIMI_PT_panel_object(SURIMI_PT_panel_base):
    bl_idname = 'SURIMI_PT_panel_object'
    bl_label = 'Object'
    bl_parent_id = SURIMI_PT_panel_main.bl_idname

    @classmethod
    def poll(cls, ctx: T.Context):
        return any(x.type == 'MESH' for x in ctx.selected_objects)

    def draw(self, ctx: T.Context):
        layout = self.layout
        obj = ctx.active_object

        row = layout.column()
        row.operator(OBJECT_OT_surimi_rename_weights.bl_idname)

#


classes = [
    SURIMI_PT_panel_main,
    SURIMI_PT_panel_viewport,
    SURIMI_PT_panel_render,
    SURIMI_PT_panel_object,
    SURIMI_PT_panel_armature,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
